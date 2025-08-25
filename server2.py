# server.py
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Dict
from typing import Optional
import json
import sqlite3
import uvicorn
from db import init_db, insert_plan, update_plan, delete_all_plans
from services.perplexity_tool import perplexity_tool_prompt, call_perplexity_tool
from services.open_ai_tool import call_openai_tool, selected_strategy_expansion
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from tools.twilio_messenger import send_whatsapp
from graph.sms_pipeline import main as sms_main
from graph.whatsapp_pipeline import main as whatsapp_main
from tools.email_tool import send_bulk_email
import re


DB_PATH = "marketing.db"

app = FastAPI(title="Marketing Plan Generator MSME")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔹 Initializing database...")
    init_db()
    yield
    print("🔹 Shutting down...")

class BusinessInfo(BaseModel):
    business_name: str
    business_type: str
    location: str
    website_link: str
    business_goals: str
    marketing_budget: float
    target_audience: str
    current_marketing_assets: str
    brand_voice: str

class Message(BaseModel):
    message: str

class TwilioMessageInfo(BaseModel):
    type: str                 
    sender_number: str
    sms_message: str
    sending_period: str       
    time: Optional[str] = None

class EmailMessageInfo(BaseModel):
    sender_email: str
    subject: str
    body: str
    app_password: str


@app.get("/")
async def root():
    return {"message": "Welcome to Marketing API"}

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

@app.get("/delete_all_plans")
async def delete_all_plans_route():
    delete_all_plans()
    return {"message": "All plans deleted"}

@app.post("/user_basic_input")
def user_basic_input(data: BusinessInfo):
    plan_id = insert_plan(json.dumps(data.model_dump()))
    return {"plan_id": plan_id, "message": "Business info stored"}

@app.post("/call_perplexity/{plan_id}")
def call_perplexity(plan_id: int, data: BusinessInfo):
    try:
        prompt = perplexity_tool_prompt(data.website_link)
        output = call_perplexity_tool(prompt)
        update_plan(plan_id, perplexity_data=json.dumps(output))
        return {"plan_id": plan_id, "perplexity_data": output, "message": "Perplexity output stored"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get_missing_info/{plan_id}")
def get_missing_info(plan_id: int, user_filled_data: Dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT perplexity_data FROM plans WHERE id = ?", (plan_id,))
    row = cur.fetchone()
    conn.close()

    if not row or not row[0]:
        raise HTTPException(status_code=404, detail="Perplexity data not found")

    # ---- Helper: Decode nested JSON strings into Python objects ----
    def decode_nested_json(obj):
        """
        Recursively parse any string that is itself JSON into a Python dict/list.
        """
        if isinstance(obj, str):
            try:
                parsed = json.loads(obj)
                return decode_nested_json(parsed)
            except (ValueError, TypeError):
                return obj
        elif isinstance(obj, dict):
            return {k: decode_nested_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [decode_nested_json(i) for i in obj]
        return obj

    # ---- Helper: Merge dictionaries safely ----
    def merge_dicts(original, updates):
        """
        Recursively merge two dicts without assuming `.get()` works on strings.
        """
        if not isinstance(original, dict) or not isinstance(updates, dict):
            return updates  # if either is not a dict, replace entirely

        for k, v in updates.items():
            if k in original and isinstance(original[k], dict) and isinstance(v, dict):
                original[k] = merge_dicts(original[k], v)
            else:
                original[k] = v
        return original

    # Decode stored Perplexity data (in case it has JSON strings inside)
    stored_data = decode_nested_json(json.loads(row[0]))

    # Merge user-filled missing data into decoded Perplexity data
    updated_data = merge_dicts(stored_data, user_filled_data)

    # Save updated data back to DB
    update_plan(plan_id, perplexity_data=json.dumps(updated_data))

    return {
        "plan_id": plan_id,
        "updated_perplexity_data": updated_data,
        "message": "Perplexity data updated with missing info"
    }



@app.post("/generate_marketing_plan/{plan_id}")
def generate_marketing_plan(plan_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT business_info, perplexity_data FROM plans WHERE id = ?", (plan_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Plan not found")

    business_info_str, perplexity_data_str = row
    if not business_info_str or not perplexity_data_str:
        raise HTTPException(status_code=400, detail="Business info or Perplexity data missing")

    try:
        form_data = json.loads(business_info_str)
        perplexity_data = json.loads(perplexity_data_str)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON stored in DB")

    marketing_plan_raw = call_openai_tool(form_data, perplexity_data)

    json_match = re.search(r"```json(.*?)```", marketing_plan_raw, re.DOTALL)
    plan_json = None
    if json_match:
        try:
            plan_json = json.loads(json_match.group(1).strip())
        except json.JSONDecodeError:
            plan_json = None

    # Remove JSON block from the text → gives you sections 1–7 only
    plan_text = re.sub(r"```json.*?```", "", marketing_plan_raw, flags=re.DOTALL).strip()

    # Save only text plan in DB (optional)
    update_plan(plan_id, marketing_plan=plan_text)

    return {
        "plan_id": plan_id,
        "plan_text": plan_text,   
        "plan_json": plan_json,   
        "message": "Marketing plan generated and stored"
    }

@app.post("/generate_expanded_strategy/{plan_id}")
def generate_expanded_strategy(plan_id: int, user_input: Message):

    user_message = user_input.message

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT business_info, perplexity_data, marketing_plan FROM plans WHERE id = ?", (plan_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Plan not found")

    business_info_str, perplexity_data_str, current_plan = row

    if not business_info_str or not perplexity_data_str or not current_plan:
        raise HTTPException(status_code=400, detail="Business info, Perplexity data, or Marketing plan missing")

    try:
        form_data = json.loads(business_info_str)
        perplexity_data = json.loads(perplexity_data_str)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON stored in DB")

    expanded_plan = selected_strategy_expansion(form_data, perplexity_data, current_plan, user_message)

    update_plan(plan_id, marketing_plan=expanded_plan)

    return {
        "plan_id": plan_id,
        "expanded_plan": expanded_plan,
        "message": "Agent response generated and stored"
    }

@app.post("/twilio_messenger")
async def twilio_messenger(
    data: TwilioMessageInfo = Depends(),
    file: UploadFile = File(...)
):
    try:
        sending_period_clean = (data.sending_period or "").strip().lower()
        if sending_period_clean not in ("instant", "scheduled"):
            raise HTTPException(status_code=400, detail="Invalid sending_period. Must be 'instant' or 'scheduled'")

        csv_bytes = await file.read()

        if data.type.lower() == "whatsapp":
            result = whatsapp_main(
                message_text=data.sms_message,
                sender_number=data.sender_number,
                csv_bytes=csv_bytes,
                sending_period=sending_period_clean,
                scheduled_time=data.time
            )
            return {"status": "Whatsapp message sent successfully", "sid": result}

        elif data.type.lower() == "sms":
            result = sms_main(
                message_text=data.sms_message,
                sender_number=data.sender_number,
                csv_bytes=csv_bytes,
                sending_period=sending_period_clean,
                scheduled_time=data.time
            )
            return {"status": "SMS processed", "details": result}

        else:
            raise HTTPException(status_code=400, detail="Invalid message type")

    except Exception as e:
        print(f"Twilio error: {e}")
        raise HTTPException(status_code=500, detail=f"Twilio error: {e}")


@app.post("/send_email")
async def send_email(
    data: EmailMessageInfo = Depends(),
    file: UploadFile = File(...)
):
    try:

        csv_content = await file.read()
        decoded_csv = csv_content.decode('utf-8')
        reader = csv.reader(StringIO(decoded_csv))

        recipients = [row[0].strip() for row in reader if row and row[0].strip()]

        if not recipients:
            raise HTTPException(status_code=400, detail="No valid recipient emails found in CSV.")


        result = send_bulk_email(
            sender_email=data.sender_email,
            app_password=data.app_password,
            recipients=recipients,
            subject=data.subject,
            html_message=data.body
        )

        if result.get("status") == "failed":
            raise HTTPException(status_code=500, detail=result["error"])

        return {
            "status": "Emails sent successfully",
            "total_recipients": len(recipients),
            "recipients": recipients
        }

    except Exception as e:
        print(f"Email sending error: {e}")
        raise HTTPException(status_code=500, detail=f"Email sending failed: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6969)
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
# from graph.graph_1 import prospect_graph
from tools.twilio_messenger import send_whatsapp
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from graph.sms_pipeline import main as sms_main
from graph.whatsapp_pipeline import main as whatsapp_main

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Input from frontend for pipeline =====
class ProspectingInput(BaseModel):
    user_input: str
    agent_name: str


@app.get("/")
async def root():
    return {"message": "Welcome to Prospecting API"}

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

# @app.post("/prospecting_node")
# async def prospecting_node(input_data: ProspectingInput):
#     try:
#         graph_input = {
#             "agent_input": input_data.user_input,
#             "agent_output": "",
#             "current_agent": input_data.agent_name,
#             "status": "",
#             "prev_output": ""
#         }
#         result = prospect_graph.invoke(graph_input)
#         return {
#             "status": "success",
#             "current_agent": input_data.agent_name,
#             "agent_output": result.get("agent_output", ""),
#             "full_state": result
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.post("/twilio_messenger")
async def twilio_messenger(
    type: str = Form(...),
    sender_number: str = Form(...),
    sms_message: str = Form(...),
    sending_period: str = Form(...),
    time: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    try:
        if type.lower() == "whatsapp":
            sending_period_clean = (sending_period or "").strip().lower()
            if sending_period_clean not in ("instant", "scheduled"):
                raise HTTPException(status_code=400, detail="Invalid sending_period. Must be 'instant' or 'scheduled'")
            csv_bytes = await file.read()
            result = whatsapp_main(
                message_text=sms_message,
                sender_number=sender_number,
                csv_bytes=csv_bytes,
                sending_period=sending_period_clean,
                scheduled_time=time
            )
            return {"status": "Whatsapp message sent successfully", "sid": result}
        elif type.lower() == "sms":
            sending_period_clean = (sending_period or "").strip().lower()
            if sending_period_clean not in ("instant", "scheduled"):
                raise HTTPException(status_code=400, detail="Invalid sending_period. Must be 'instant' or 'scheduled'")
            csv_bytes = await file.read()
            result = sms_main(
                message_text=sms_message,
                sender_number=sender_number,
                csv_bytes=csv_bytes,
                sending_period=sending_period_clean,
                scheduled_time=time
            )
            return {"status": "SMS processed", "details": result}
        else:
            raise HTTPException(status_code=400, detail="Invalid message type")
    except Exception as e:
        print(f"Twilio error: {e}")
        raise HTTPException(status_code=500, detail=f"Twilio error: {e}")

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

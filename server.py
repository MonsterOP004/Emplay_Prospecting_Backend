from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph.graph_1 import prospect_graph
from tools.twilio_messenger import send_sms, send_whatsapp
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from graph.sms_pipeline import main

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class productInput(BaseModel):
    product: str
    description: str = ""
    pricing: str = ""
    sales: str = ""

class twilioInput(BaseModel):
    type: str
    company_name: str
    product_name: str
    mode: str
    file: str = "" 
    to: str

@app.get("/")
async def root():
    return {"message": "Welcome to Prospecting API"}

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

@app.post("/prospecting_node")
async def prospecting_node(input_data: productInput):
    try:
        result = prospect_graph(
            input_data.product,
            input_data.description,
            input_data.pricing,
            input_data.sales
        )
        return {
            "customer_strategy": result["customer_strategy"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/twilio_messenger")
async def twilio_messenger(input_data: twilioInput):
    try:
        if input_data.type == "whatsapp":
            sid = send_whatsapp(input_data.message, input_data.to)
            return {"status": "Whatsapp Message sent successfully", "sid": sid}
        elif input_data.type == "sms":
            sid = main(input_data.message, input_data.to)
            return {"status": "SMS Message sent successfully", "sid": sid}
        else:
            raise HTTPException(status_code=400, detail="Invalid message type")
    except Exception as e:
        print(f"Twilio error: {e}")
        raise HTTPException(status_code=500, detail=f"Twilio error: {e}")



if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

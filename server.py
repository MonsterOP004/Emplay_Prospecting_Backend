from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph.graph_1 import competitor_graph
from tools.twilio_messenger import send_sms, send_whatsapp
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

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

class twilioInput(BaseModel):
    type: str
    to: str
    message: str

@app.get("/")
async def root():
    return {"message": "Welcome to Prospecting API"}

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

@app.post("/competitor_node")
async def competitor_node(input_data: productInput):
    try:
        result = competitor_graph(input_data.product)
        return {
            "refined_product": result["refined_product"],
            "analysis": result["analysis"]
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
            sid = send_sms(input_data.message, input_data.to)
            return {"status": "SMS Message sent successfully", "sid": sid}
        else:
            raise HTTPException(status_code=400, detail="Invalid message type")
    except Exception as e:
        print(f"Twilio error: {e}")
        raise HTTPException(status_code=500, detail=f"Twilio error: {e}")

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = FastAPI()

templates = Jinja2Templates(directory="templates")

model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return templates.TemplateResponse("credentials.html")

@app.post("/chatbot")
async def chatbot(request: Request):
    data = await request.json()
    question = data.get("question")
    
    inputs = tokenizer.encode(question, return_tensors="pt")
    outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {"response": response}

@app.get("/conversation")
def conversation(request: Request):
    return templates.TemplateResponse("conversation.html", {"request": request})
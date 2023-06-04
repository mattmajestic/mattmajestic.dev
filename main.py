from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("credentials.html", {"request": request})

@app.get("/ai_chat")
async def bot_conversation(request: Request):
    return templates.TemplateResponse("conversation.html", {"request": request})

@app.get("/favicon.ico")
async def favicon():
    return app.send_static_file("favicon.ico")
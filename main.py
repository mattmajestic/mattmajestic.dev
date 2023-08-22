from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# import torch
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
import stripe
import json
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/credentials")
def credentials(request: Request):
    return templates.TemplateResponse("credentials.html", {"request": request})

# @app.get("/signin")
# def signin(request: Request):
#     return templates.TemplateResponse("signin.html", {"request": request})

# @app.post("/chatbot")
# async def chatbot(request: Request):
#     data = await request.json()
#     question = data.get("question")
#     model = GPT2LMHeadModel.from_pretrained("gpt2")
#     tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
#     inputs = tokenizer.encode(question, return_tensors="pt")
#     outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return {"response": response}

# @app.get("/conversation")
# async def conversation(request: Request):
#     return templates.TemplateResponse("conversation.html", {"request": request})

@app.get("/download-resume-pdf")
async def download_resume():
    resume_file_path = "static/Matt J Majestic Resume.pdf"
    return FileResponse(resume_file_path, filename="Matt J Majestic Resume.pdf")
    
@app.get("/donate")
async def donate(request: Request):
    return templates.TemplateResponse("stripe.html", {"request": request})

@app.get("/chat_h2o")
async def chat_h2o(request: Request):
    return templates.TemplateResponse("h2ogpt.html", {"request": request})

@app.get("/analytics")
async def analytics(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})

@app.get("/blog")
async def get_blog_posts(request: Request):
    try:
        # Read the blog.json file
        with open(os.path.join("static", "blog-posts.json")) as file:
            blog_posts = json.load(file)

        return templates.TemplateResponse("blog.html", {"request": request, "blog_posts": blog_posts})
    except FileNotFoundError:
        return templates.TemplateResponse("blog.html", {"request": request, "blog_posts": []})
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error_message": str(e)})

@app.get("/blog-posts")
async def get_blog_posts():
    try:
        with open("static/blog-posts.json") as file:
            blog_posts = json.load(file)
            return blog_posts
    except FileNotFoundError:
        return []
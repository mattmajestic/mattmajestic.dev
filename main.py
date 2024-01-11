from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
# import torch
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
import stripe
import json
import os
import httpx
import markdown2
from jinja2 import Environment, FileSystemLoader
import requests

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",  # Add your frontend URL(s) here
    "https://mattmajestic.dev",
]

# Add CORS middleware with the configured origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],    
    allow_headers=["*"],    
)

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
    resume_file_path = "static/Matt Majestic Dev Resume.pdf"
    return FileResponse(resume_file_path, filename="Matt Majestic Dev Resume.pdf")
    
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

@app.get("/readme")
async def get_readme(request: Request):
    return templates.TemplateResponse("readme.html", {"request": request})

@app.get("/projects")
async def projects(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request})

@app.get("/youtube-metrics")
async def get_youtube_metrics():
    API_KEY = os.environ.get("YT_API_KEY")
    if API_KEY is None:
        return {"error": "YouTube API key not found"}

    CHANNEL_ID = "UCjTavL86-CW6j58fsVIjTig"
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=id&maxResults=100"
    response = requests.get(url)
    data = response.json()
    video_ids = [item["id"]["videoId"] for item in data.get("items", []) if "id" in item and "videoId" in item["id"]]
    video_data = []

    # Loop through each video ID and fetch metrics
    for video_id in video_ids:
        url = f"https://www.googleapis.com/youtube/v3/videos?key={API_KEY}&id={video_id}&part=statistics"
        response = requests.get(url)
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            statistics = data["items"][0]["statistics"]

            # Extract video metrics
            video_views = statistics.get("viewCount", 0)
            video_likes = statistics.get("likeCount", 0)
            video_comments = statistics.get("commentCount", 0)

            video_metrics = {
                "Video ID": video_id,
                "Views": video_views,
                "Likes": video_likes,
                "Comments": video_comments
            }

            video_data.append(video_metrics)
        else:
            print(f"Statistics data not available for video with ID: {video_id}")

    return video_data
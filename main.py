from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils.mashup import search_videos, download_video, convert_video_to_audio, merge_audio_files, zip_files, send_email, delete_folder
from model.form import Form
import random

random.seed(5)

app = FastAPI()

app.mount("/static", StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@app.route("/", methods=["GET", "POST"])
def main(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/submitform")
def util(data:Form):
    name = data.name
    email = data.email
    num_videos = data.num_videos
    duration= data.duration
    print(name, email, num_videos, duration)
    temp_folder = f"fold{random.randint(10000000, 99999999)}/"
    video_links = search_videos(name)
    download_video(video_links, f'{temp_folder}video/', num_videos)
    print("Videos Downloaded")
    convert_video_to_audio(f'{temp_folder}video/',f'{temp_folder}audio/',duration)
    print("Conversion Done")
    merge_audio_files(temp_folder, f'{temp_folder}audio/')
    print("merging done")
    zip_files(f'{temp_folder}merged-audio.zip', f'{temp_folder}merged.mp3')
    print("zipping done")
    send_email(email, "Your Mashup song is ready", "Enjoy your song", f'{temp_folder}merged-audio.zip')
    print("mail sent")
    delete_folder(temp_folder)
    print("folder deleted")
    return {"Message": "Success"}
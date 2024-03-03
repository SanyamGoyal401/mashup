import os
import urllib.request
from urllib.parse import quote
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from zipfile import ZipFile
from pytube import YouTube
import re
import shutil
import traceback
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

load_dotenv()
HOST = os.environ.get("MAIL_HOST")
USERNAME = os.environ.get("MAIL_USERNAME")
PASSWORD = os.environ.get("MAIL_PASSWORD")
PORT = os.environ.get("MAIL_PORT")

def search_videos(search_term: str):
  encoded_query = quote(search_term)
  # print(encoded_query)
  html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + encoded_query)
  video_ids = list(set(re.findall(r"watch\?v=(\S{11})", html.read().decode())))
  video_links = []
  for id in video_ids:
    video_links.append("https://www.youtube.com/watch?v=" + id)
  return video_links

def clean_string(input_string: str):
    # Define the regular expression pattern
    pattern = r'[#@$%^&*()]+|\s+'
    
    # Use re.sub() to replace the matched characters with an empty string
    cleaned_string = re.sub(pattern, '', input_string)
    return cleaned_string

def download_video(video_url, output_path, num):
    try:
      count = 0
      for link in video_url:
          try:
            # Create a YouTube object
            yt = YouTube(link)

            # Get the highest resolution stream
            video_stream = yt.streams.first()
        
            filename = clean_string(yt.title)
            filename = f"{filename}.mp4"

            # Set the output path for the downloaded video
            output_path = output_path.rstrip("/")

            # Download the video
            video_stream.download(output_path, filename=filename)
            print(f"Download complete! Saved to: {output_path}")
            count += 1
            if count == num: 
              break
          except Exception as ex:
            print(f"An error occured: {str(ex)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()

def convert_video_to_audio(video_path, audio_path, duration):
  try:
    for filename in os.listdir(video_path):
      file_path = os.path.join(video_path, filename)
      if os.path.isfile(file_path):
        clip = VideoFileClip(file_path)
        clip = clip.subclip(0, duration)
        audio = clip.audio
        filename = os.path.join(audio_path, f"{filename.split('.')[0]}.mp3")
        if not os.path.exists(audio_path):
          os.makedirs(audio_path)
        audio.write_audiofile(filename)
  except Exception as e:
    print(f"An error occurred: {str(e)}")
    traceback.print_exc()

def merge_audio_files(output_path, audio_paths):
    try:
      print(output_path)
      print(audio_paths)
      combined = AudioSegment.silent(duration=0)
      for filename in os.listdir(audio_paths):
        file_path = os.path.join(audio_paths, filename)
        print(file_path)
        if os.path.isfile(file_path):
          sound = AudioSegment.from_mp3(file_path)
          combined += sound
      combined.export(f'{output_path}merged.mp3', format="mp3")
    except Exception as e:
      print(f"An error occurred: {str(e)}")
      traceback.print_exc()

def zip_files(zip_filename, file):
  with ZipFile(zip_filename, 'w') as zip:
    zip.write(file)

def send_email(email, subject, body, attachment_path):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = USERNAME
    msg['To'] = email
    msg['Subject'] = subject

    # Attach the text body
    msg.attach(MIMEText(body, 'plain'))

    # Attach the file
    with open(attachment_path, 'rb') as file:
        attachment = MIMEApplication(file.read(), Name="attachment")
        attachment['Content-Disposition'] = f'attachment; filename={attachment_path}'
        msg.attach(attachment)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(HOST, PORT) as server:
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, email, msg.as_string())


def delete_folder(folder_path):
  try:
    # Iterate over the contents of the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # If it's a file, delete it
        if os.path.isfile(item_path):
            os.remove(item_path)
            print(f"File '{item_path}' has been deleted.")

        # If it's a folder, recursively delete its contents
        elif os.path.isdir(item_path):
            delete_folder(item_path)

    # After deleting all subfiles and subfolders, delete the folder itself
    shutil.rmtree(folder_path)
    print(f"The folder '{folder_path}' and its contents have been deleted.")
  except OSError as e:
      print(f"Error: {e}")
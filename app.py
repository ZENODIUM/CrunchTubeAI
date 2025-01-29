from flask import Flask, request, render_template
from yt_dlp import YoutubeDL
import google.generativeai as genai
import time
import os
import re
import json
from crop_image import extract_and_save_frame
from cheat import generate_pdf
from gtts import gTTS
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

genai.configure(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))

if not os.path.exists("videos"):
    os.makedirs("videos")

ydl_opts = {
    'format': 'best',
    'writesubtitles': True,
    'subtitleslangs': ['en'],
    'writeautomaticsub': False,
    'outtmpl': 'static/videos/%(title)s.%(ext)s',
}

ydl_opts_sub = {
    'format': 'best',
    'writesubtitles': True,
    'subtitleslangs': ['en'],
    'writeautomaticsub': True,
    'outtmpl': 'subs/%(title)s.%(ext)s',
    'skip_download': True,
}

def fetch_youtube_comments(video_id):
    api_key = os.getenv("YOUTUBE_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=20,
        order='relevance'
    )
    response = request.execute()
    comments = [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in response['items']]
    return comments

def text_to_speech_gtts(text, filename="output.mp3", language="en", slow=False):
    try:
        audio_dir = "static/audio/"
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
        full_path = os.path.join(audio_dir, filename)
        tts = gTTS(text=text, lang=language, slow=slow)
        tts.save(full_path)
    except Exception as e:
        print(f"Error: {e}")

def process_data_dict(data_dict, video_path):
    output_paths = []
    for topic in data_dict:
        for subtopic in topic['Subtopics']:
            if subtopic['Coordinates']:
                timestamp = subtopic['TimestampImage']
                coordinates = subtopic['Coordinates']
                try:
                    output_path = extract_and_save_frame(video_path, timestamp, coordinates)
                    output_paths.append(output_path)
                    subtopic['cropped_path'] = output_path
                except Exception as e:
                    print(f"Error processing {subtopic['Subtopic']}: {e}")
    return output_paths

def get_youtube_id(url):
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_video():
    youtube_link = request.form['youtube_link']
    video_id = get_youtube_id(youtube_link)

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_link])
        info_dict = ydl.extract_info(youtube_link, download=False)
        video_file_path = ydl.prepare_filename(info_dict)

    with YoutubeDL(ydl_opts_sub) as ydl:
        ydl.download([youtube_link])
        info_dict_sub = ydl.extract_info(youtube_link, download=False)
        sub_file_path = ydl.prepare_filename(info_dict_sub).replace('.mp4', '.en.vtt')

    video_file = genai.upload_file(path=video_file_path)
    
    while video_file.state.name == "PROCESSING":
        time.sleep(10)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError(video_file.state.name)

    prompt_summary = '''
Analyze the provided lecture video and summarize its content by identifying the main topics, subtopics...
'''
    
    model_summary = genai.GenerativeModel(model_name="gemini-1.5-pro")
    
    response_summary = model_summary.generate_content([video_file, prompt_summary], request_options={"timeout": 1000})
    
    content_summary = response_summary.text.strip("``````").strip()
    
    try:
        data_dict = json.loads(content_summary)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        data_dict = None

    result_string = ""
    for topic in data_dict:
        for subtopic in topic['Subtopics']:
            result_string += subtopic['Subtopic'] + " " + subtopic['Content'] + "\n"

    text_to_speech_gtts(result_string, filename="output.mp3")
    
    output_paths = process_data_dict(data_dict, video_file_path)

    with open(sub_file_path, 'r', encoding='utf-8') as file:
        vtt_content = file.read()

    prompt_cheat_sheet = '''
Analyze the topics in this Educational video Subtitles and give a cheat sheet...
'''
    
    model_cheat_sheet = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
    
    response_cheat_sheet = model_cheat_sheet.generate_content([vtt_content, prompt_cheat_sheet], request_options={"timeout": 600})
    
    content_cheat_sheet= response_cheat_sheet.text.strip().split(',')
    
    sections_cheat_sheet = []
    
    for line in content_cheat_sheet:
        if line.strip():
            try:
                topic, content = line.split(':', 1)
                sections_cheat_sheet.append((topic.strip(), content.strip()))
            except ValueError:
                print(f"Skipping improperly formatted line: {line.strip()}")

    generate_pdf(sections_cheat_sheet, title="Cheat Sheet", output_file="static/pdfs/cheat_sheet.pdf")

    additional_materials_prompt = '''
Provide 10 additional study materials with links related to this educational lecture...
'''
    
    response_additional_materials = model_cheat_sheet.generate_content([vtt_content, additional_materials_prompt], request_options={"timeout": 600})
    
    additional_materials_content= response_additional_materials.text
    
    materials_list = []
    
    for section in additional_materials_content.split('Content:'):
        if 'Link:' in section:
            parts = section.split('Link:')
            title, link = parts[0].strip(), parts[1].strip()
            materials_list.append({'title': title, 'link': link})

    comments_data_list= fetch_youtube_comments(video_id)

    comments_analysis_prompt = '''
Analyze the given comments for a YouTube video and provide a short summary...
'''
    
    response_comments_analysis= model_cheat_sheet.generate_content([" ".join(comments_data_list), comments_analysis_prompt], request_options={"timeout": 1000})
    
    comments_analysis_content= response_comments_analysis.text
    
    summary_part, caveats_part = comments_analysis_content.split('Caveats', 1)
    
    return render_template(
        'result.html',
        data=data_dict,
        video_path=video_file_path.replace("\\", "/"),
        content_list=materials_list,
        content_comment=summary_part.strip(),
        caveats=f"Caveats{caveats_part.strip()}"
)

if __name__ == '__main__':
    app.run(debug=True)

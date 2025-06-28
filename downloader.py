import os
import re
import yt_dlp
import requests
from bs4 import BeautifulSoup
from instaloader import Instaloader, Post
from telegram import Update
from telegram.ext import ContextTypes

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str):
    chat_id = update.message.chat_id
    try:
        # حدد الموقع
        if "youtube.com" in url or "youtu.be" in url:
            await download_youtube(update, context, url)
        elif "instagram.com" in url:
            await download_instagram(update, context, url)
        elif "tiktok.com" in url:
            await download_tiktok(update, context, url)
        elif "twitter.com" in url:
            await download_twitter(update, context, url)
        elif "facebook.com" in url:
            await download_facebook(update, context, url)
        elif "pinterest.com" in url:
            await download_pinterest(update, context, url)
        else:
            await update.message.reply_text("رابط غير مدعوم حالياً.")
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء التحميل: {e}")

async def download_youtube(update, context, url):
    chat_id = update.message.chat_id
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'noplaylist': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    with open(filename, 'rb') as f:
        await update.message.reply_video(f)
    os.remove(filename)

async def download_instagram(update, context, url):
    chat_id = update.message.chat_id
    L = Instaloader()
    shortcode = url.split("/")[-2]
    post = Post.from_shortcode(L.context, shortcode)
    filename = f"downloads/{shortcode}.mp4"
    L.download_post(post, target="downloads")
    # إرسال الملف
    await update.message.reply_video(open(filename, 'rb'))
    os.remove(filename)

async def download_tiktok(update, context, url):
    # لتنفيذ تحميل تيك توك من yt-dlp
    chat_id = update.message.chat_id
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'noplaylist': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    with open(filename, 'rb') as f:
        await update.message.reply_video(f)
    os.remove(filename)

async def download_twitter(update, context, url):
    chat_id = update.message.chat_id
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'noplaylist': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    with open(filename, 'rb') as f:
        await update.message.reply_video(f)
    os.remove(filename)

async def download_facebook(update, context, url):
    # نفس طريقة تويتر ويوتيوب باستخدام yt-dlp
    chat_id = update.message.chat_id
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'noplaylist': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    with open(filename, 'rb') as f:
        await update.message.reply_video(f)
    os.remove(filename)

async def download_pinterest(update, context, url):
    chat_id = update.message.chat_id
    # استخراج رابط الصورة أو الفيديو من صفحة بينترست
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    media_url = None
    # نبحث عن روابط الصور أو الفيديوهات داخل الميتا
    meta = soup.find("meta", property="og:video")
    if meta:
        media_url = meta.attrs.get("content")
    else:
        meta = soup.find("meta", property="og:image")
        if meta:
            media_url = meta.attrs.get("content")

    if not media_url:
        await update.message.reply_text("تعذر العثور على محتوى لتحميله من الرابط.")
        return

    # تحميل الملف مؤقتًا
    filename = media_url.split("/")[-1].split("?")[0]
    filepath = f"downloads/{filename}"
    with requests.get(media_url, stream=True) as r:
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # إرسال الملف
    ext = filepath.split(".")[-1].lower()
    with open(filepath, 'rb') as f:
        if ext in ['mp4', 'mov', 'avi', 'mkv']:
            await update.message.reply_video(f)
        else:
            await update.message.reply_photo(f)
    os.remove(filepath)

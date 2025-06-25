import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# OMDb API URL এবং API কী
OMDB_API_URL = 'http://www.omdbapi.com/'
OMDB_API_KEY = 'YOUR_OMDB_API_KEY'  # আপনার OMDb API কী এখানে দিন

# ফাইল সংরক্ষণের জন্য ডিরেক্টরি
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

# /movie কমান্ডের জন্য ফাংশন
def movie(update: Update, context: CallbackContext) -> None:
    if context.args:
        movie_name = ' '.join(context.args)
        response = requests.get(OMDB_API_URL, params={'t': movie_name, 'apikey': OMDB_API_KEY})
        data = response.json()
        
        if data['Response'] == 'True':
            reply_text = f"**Title:** {data['Title']}\n" 
                         f"**Year:** {data['Year']}\n" 
                         f"**Genre:** {data['Genre']}\n" 
                         f"**Director:** {data['Director']}\n" 
                         f"**Plot:** {data['Plot']}\n" 
                         f"**IMDb Rating:** {data['imdbRating']}\n"
            update.message.reply_text(reply_text, parse_mode='Markdown')
        else:
            update.message.reply_text("মুভিটি পাওয়া যায়নি।")
    else:
        update.message.reply_text("দয়া করে মুভির নাম দিন।")

# ভিডিও ফাইল গ্রহণের জন্য ফাংশন
def handle_video(update: Update, context: CallbackContext) -> None:
    video_file = update.message.video

    if video_file:
        file_id = video_file.file_id
        new_file = context.bot.getFile(file_id)
        
        # ফাইল সংরক্ষণ করুন
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}.mp4")
        new_file.download(file_path)
        
        update.message.reply_text("ভিডিও সফলভাবে আপলোড হয়েছে!")
    else:
        update.message.reply_text("দয়া করে একটি ভিডিও ফাইল পাঠান।")

def main():
    # আপনার টোকেন এখানে দিন
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")

    # Dispatcher ব্যবহার করে হ্যান্ডলার যোগ করুন
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("movie", movie))
    dispatcher.add_handler(MessageHandler(Filters.video, handle_video))

    # বট শুরু করুন
    updater.start_polling()

    # বট বন্ধ না হওয়া পর্যন্ত অপেক্ষা করুন
    updater.idle()

if __name__ == '__main__':
    main()

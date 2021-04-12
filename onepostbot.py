import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import facebook
import tweepy
import json
import requests

# OPENING CREDENTIALS FILE FOR THE DATA REQUIRED
with open('credentials.json', 'r') as cd:
    cdjson = json.load(cd)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
bstatus = 1


def fb(image, caption):
    # INITIALIZING PAGE ACCESS TOKEN
    graph = facebook.GraphAPI(cdjson["facebook_page_access_token"])
    bstatus = 2

    # PUBLISHING THE IMAGE WITH CAPTION ON TO THE FACEBOOK PAGE
    graph.put_photo(image=open(image, "rb").read(), caption=caption)
    bstatus = 3
    return bstatus


def insta(image, caption):
    # INITIALIZING IMAGE AND CAPTION OBJECT TO THE FACEBOOK SERVER
    initurl = "https://graph.facebook.com/" + cdjson[
        "instagram_business_id"] + "/media?image_url=" + image + "&caption=" + caption + "&access_token=" + \
              cdjson[
                  "facebook_page_access_token"]

    creation = requests.request(method="post", url=initurl)
    creation_id = "" + creation.json()["id"]
    bstatus = 2

    # PUBLISHING THE OBJECT CREATED ON THE FACEBOOK SERVER
    finalurl = "https://graph.facebook.com/" + cdjson["instagram_business_id"] + "/media_publish?creation_id=" + \
               creation_id + "&access_token=" + cdjson[
                   "facebook_page_access_token"]

    creation = requests.request(method="post", url=finalurl)
    bstatus = 3
    return bstatus


def tweewt(image, caption):
    auth = tweepy.OAuthHandler(cdjson["twitter_consumer_key"], cdjson["twitter_consumer_secret"])
    auth.set_access_token(cdjson["twitter_access_token"], cdjson["twitter_access_token_secret"])
    api = tweepy.API(auth)

    # INITIALIZING THE IMAGE ON THE SERVER
    media = api.media_upload(image)
    bstatus = 2

    # PUBLISHING THE CHANGES ON THE FINAL SERVER
    post_result = api.update_status(status=caption, media_ids=[media.media_id])
    bstatus = 3
    return bstatus


def botcon(image, caption):
    urlgenerator = 'http://vyd2999.pythonanywhere.com/'

    with open(image, 'rb') as f:
        r = requests.post(urlgenerator, files={'image': f})
        imageurl = r.json()["url"]

    fb(image=image, caption=caption)

    mbstatus = 2

    insta(image=imageurl, caption=caption)

    mbstatus = 3

    tweewt(image=image, caption=caption)

    mbstatus = 5
    return mbstatus


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Hi! KEEP SENDING MEMES BUT MAKE SURE YOU HAVE THE RIGHT TO SHARE AND IF WE HSHARE ON '
        'OUR SOCIAL HANDLE WE ARE NOT RESPONSIBLE FOR ANY COPYRIGHT INFRINGEMENTS... '
        'SO ONLY SHARE MEMES YOU OWN AND DO NOT MIND US POSTING THEN KEEP SENDING')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echotext(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text("Sirf caption leke kya karu me pic bhejna yaar")


def echonikal(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text("jisne ye bot banaya vohi meme bhejega tu pehli fursat me nikal")


def echoimage(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text("Abey bina caption ke post kardu isko me?")


def photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    caption_text = update.message.caption
    filename = "temp/" + str(photo_file.file_id) + ".jpg"
    photo_file.download(filename)
    botcon(image=filename, caption=caption_text)

    update.message.reply_text('NOICE MEME KEEP SENDING...')
    print(user.username + " sent " + photo_file.file_id)


def andar():
    """Start the bot."""
    print("telegram bot working")
    # Create the Updater and pass it your bot's token.
    updater = Updater(cdjson["telegram_token"])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(
        MessageHandler(Filters.chat(username=cdjson["telegram_username"]) & Filters.text & ~Filters.command, echotext))
    dispatcher.add_handler(MessageHandler(
        Filters.chat(username=cdjson["telegram_username"]) & Filters.photo & Filters.caption & ~Filters.command, photo))
    dispatcher.add_handler(
        MessageHandler(Filters.chat(username=cdjson["telegram_username"]) & Filters.photo & ~Filters.command,
                       echoimage))
    dispatcher.add_handler(MessageHandler(~Filters.command, echonikal))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    andar()

botcon(image="https://drive.google.com/thumbnail?id=1PMrBo42GXpToOfdkrbTVgIz9MyqRGOiA", caption="hello world")

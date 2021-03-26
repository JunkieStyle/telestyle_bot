from telegram.ext import Updater, CommandHandler
import requests
import logging
from urllib.parse import urljoin

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger()


def get_meme_url(subreddit=None):
    url = "https://meme-api.herokuapp.com/gimme"
    if subreddit:
        url = urljoin(url + "/", subreddit)

    logger.info("Url %s" % url)
    r = requests.get(url).json()
    logger.info("Got json response: %s" % r)
    return r["url"]


def send_meme(update, context):
    logger.info("Got update: %s" % update)
    logger.info("Got args: %s" % context.args)
    url = get_meme_url(*context.args)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)


def main():
    with open("token.txt") as f:
        token = f.read()

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('meme', send_meme, pass_args=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

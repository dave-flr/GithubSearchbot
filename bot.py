import sys
import os
import time
import requests
import json

import telebot
from telebot import types
from flask import Flask, request

TOKEN = '1120016734:AAGZihZbB5Il7kbxYaGKsroMACH3CIVjhDA'

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.inline_handler(lambda query: True)
def query_text(inline_query):
    try:
        print(inline_query.query)
        params = {'q': inline_query.query}

        response = requests.get('https://api.github.com/search/repositories', params=params)
        data = json.loads(response.text)

        results = []
        for repo in data['items']:
            item = types.InlineQueryResultArticle(id=repo['id'],
                                                  title=repo['name'],
                                                  input_message_content=types.InputTextMessageContent(repo['html_url']),
                                                  description=repo['description'],
                                                  thumb_url=repo['owner']['avatar_url'])
            results.append(item)

        bot.answer_inline_query(inline_query.id, results)
    except Exception as e:
        print(e)


# def main_loop():
#     bot.polling(True)
#     while 1:
#         time.sleep(3)

# if __name__ == '__main__':
#     try:
#         main_loop()
#     except KeyboardInterrupt:
#         print('\nExiting by user request.\n')
#         sys.exit(0)


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://frozen-castle-20396.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

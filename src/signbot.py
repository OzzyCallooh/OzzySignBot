import logging
import random
import os
from io import BytesIO
from uuid import uuid4

from telegram import  InlineQueryResultArticle, ParseMode, InputTextMessageContent,  InlineQueryResultCachedSticker
from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from telegram.error import TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError

from config import config
from sign import create_sign_sticker

TOKEN = config['telegram']['token']
CHAT_ID = config['telegram']['chat_id']

def start(bot, update):
	update.message.reply_text('Hi! Type /sign followed by some text.')

def auto_line_break(sign_text):
	if '\n' in sign_text:
		return sign_text
	words = sign_text.strip().split()
	lines = []
	line = ''
	#print('max chars per line: ' + str(config['signgen']['geometry']['max_chars_per_line']))
	for word in words:
		sz = len(word)
		#print('word: ' + repr(word) + ' (' + str(sz) + ')')
		if len(line) == 0 or len(line) + sz <= config['signgen']['geometry']['max_chars_per_line']:
			#print('add to line: ' + repr(word))
			line += (' ' if len(line) > 0 else '') + word
		else:
			#print('next line: ' + repr(word))
			lines.append(line)
			line = word
	lines.append(line)
	#print(repr(lines))
	return '\n'.join(lines[:5])

def sign(bot, update, args):
	sign_text = update.message.text[6:]
	sign_text = auto_line_break(sign_text)

	# Create a temporary buffer to hold the sticker
	fp = BytesIO()

	create_sign_sticker(sign_text, fp)

	# Seek to the beginning to be ready for reading
	fp.seek(0)

	update.message.reply_sticker(fp)

def inlinequery(bot, update):
	query = update.inline_query.query
	if len(query) == 0:
		update.inline_query.answer([])
		return

	sign_text = query
	sign_text = auto_line_break(sign_text)

	# Create a temporary buffer to hold the sticker
	fp = BytesIO()

	create_sign_sticker(sign_text, fp)

	# Seek to the beginning to be ready for reading
	fp.seek(0)

	msg = None
	try:
		msg = bot.send_sticker(CHAT_ID, fp)
	except Exception as e:
		logging.exception(e, exc_info=True)

	if not msg:
		update.inline_query.answer([])

	file_id = msg.sticker.file_id

	if file_id:
		update.inline_query.answer([
			InlineQueryResultCachedSticker(
				id=uuid4(), sticker_file_id=file_id
			)
		])
	else:
		update.inline_query.answer([])

def error_callback(bot, update, error):
	try:
		raise error
	except Unauthorized:
		# remove update.message.chat_id from conversation list
		logging.exception(error, exc_info=True)
	except BadRequest:
		# handle malformed requests - read more below!
		logging.exception(error, exc_info=True)
	except TimedOut:
		# handle slow connection problems
		logging.exception(error, exc_info=True)
	except NetworkError:
		# handle other connection problems
		logging.exception(error, exc_info=True)
	except ChatMigrated:
		# the chat_id of a group has changed, use e.new_chat_id instead
		logging.exception(error, exc_info=True)
	except TelegramError:
		# handle all other telegram related errors
		logging.exception(error, exc_info=True)

def main():
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	                    level=logging.INFO)

	updater = Updater(TOKEN)
	updater.dispatcher.add_handler(CommandHandler('start', start))
	updater.dispatcher.add_handler(CommandHandler('sign', sign, pass_args=True))
	updater.dispatcher.add_handler(InlineQueryHandler(inlinequery))
	updater.dispatcher.add_error_handler(error_callback)

	logging.debug('Sign Bot running')
	if config['telegram']['use_webhook']:
		logging.debug('Using webhook')
		updater.start_webhook(
			listen='127.0.0.1',
			port=config['telegram']['webhook']['internal_port'],
			url_path=config['telegram']['token']
		)
		updater.bot.set_webhook(
			url='https://' + config['telegram']['webhook']['host'] + \
			    '/' + config['telegram']['token'],
			certificate=open(config['telegram']['webhook']['cert'], 'rb')
		)
	else:
		logging.debug('Start polling')
		updater.start_polling()
	updater.idle()

	logging.debug('Bot exiting')

if __name__ == '__main__':
	main()

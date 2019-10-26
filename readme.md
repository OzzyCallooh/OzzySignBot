# OzzySignBot

<img align="right" src="resources/botpic-sm.png">

> This Telegram bot can make stickers of Ozzy holding signs with whatever you want on them!

## How to Use

This bot works inline, in any chat on Telegram! Just type [@OzzySignBot](https://t.me/OzzySignBot) then your sign text to generate a sticker. Or, you can message the bot directly: type `/sign` followed by your sign text.

If you don't put any new lines in your sign text, the bot will try to break lines of text for you. You can have up to 5 lines of text, though sometimes text appears underneath the paws. Just play around with word length or add new lines manually if it doesn't work.

## Sticker Artist

The artist that created the original template sticker is [@LoboWupp](https://t.me/lobowupp) ([Twitter](https://twitter.com/LoboWupp), [FurAffinity](https://www.furaffinity.net/user/Lobowupp)). He does fantastic work and I highly recommend his art! :) You can install the [original sticker pack here](https://t.me/addstickers/OzzyCalloohHyena).

## How it Works

It uses [Python-Telegram-Bot](https://python-telegram-bot.org/), [Pillow](https://pillow.readthedocs.io/) and [werkzeug](https://palletsprojects.com/p/werkzeug/). It first renders text on an image, then squeezes it, rotates it, and composes it onto a [template](resources/template.png) using a [mask](resources/template-mask.png). For inline queries, it sends the sticker to a chat (in config, `telegram.chat_id`) in order to upload it before replying to the inline query.

## Dependencies

This bot runs on Python 3.4+ and requires the following libraries:

*	[Pillow](https://pillow.readthedocs.io/) for creating sticker images
*	[Python-Telegram-Bot](https://python-telegram-bot.org/) to interface with the [Telegram bot API](https://core.telegram.org/bots/api)
*	[werkzeug](https://palletsprojects.com/p/werkzeug/) for `werkzeug.secure_filename`

You can install all the dependencies using [pip](https://pypi.org/project/pip/) and the provided [requirements.txt](requirements.txt) file.

```bash
pip3 install -r requirements.txt
```

## How to Run

The bot uses configuration files which are provided via command line arguments. A sample config file can be found at [config/sample.config.json](config/sample.config.json).

```bash
python3 src/signbot.py config/sample.config.json
```

The bot also supports webhooks. See the sample configuration for more information.

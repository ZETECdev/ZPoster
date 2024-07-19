from instagrapi import Client as IGClient
from tweepy import Client
from tweepy import API, OAuthHandler
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from PIL.Image import new, open
from PIL.ImageFont import truetype
from PIL.ImageDraw import Draw
from textwrap import wrap
from os.path import dirname, abspath
from random import choice

path = dirname(abspath(__file__))

class ZPoster:
    class Telegram:
        def __init__(self, tg_token: str, chat: int, thread=None):
            self.tg = AsyncTeleBot(tg_token, 'HTML')
            self.chat = chat
            self.thread = thread

        async def msg(self, text: str, picture=None, buttons=None):
            if picture:
                await self.tg.send_photo(self.chat, open(picture, 'rb'), text,
                    message_thread_id=self.thread, reply_markup=buttons)
            else:
                await self.tg.send_message(self.chat, text,
                    message_thread_id=self.thread, reply_markup=buttons)

        async def one_button(self, text, callback_data: str, url=None):
            return InlineKeyboardMarkup().add(InlineKeyboardButton(text, url, callback_data=callback_data))


    class X:
        def __init__(self, x_login: tuple):
            self.x = Client(x_login[0], x_login[1], x_login[2], x_login[3], x_login[4])
            self.x_api = API(OAuthHandler(x_login[1], x_login[2], x_login[3], x_login[4]))

        def post(self, text: str, media=None):
            if media:
                media_ids = []
                [media_ids.append(self.x_api.media_upload(file).media_id) for file in media]
            self.x.create_tweet(text=text, media_ids=media_ids if media else None)

    class Instagram:
        def __init__(self, ig_login: tuple):
            self.instagram = IGClient()
            self.instagram.login(ig_login[0], ig_login[1])

        def post(self, picture: str, text: str):
            self.instagram.photo_upload(picture, text)

        def reel(self, picture: str, text: str, track: str):
            self.instagram.clip_upload_as_reel_with_music(picture, text, track)

        def music_search(self, music_query: str):
            random_track = choice(self.instagram.search_music(music_query))
            return random_track

    class Utils:
        def text_to_image(text: str, background_img: str):
            image = new('RGB', (1000, 1000), color='black')
            background = open(background_img)
            image.paste(background, (0, 0))
            draw = Draw(image)
            max_width, max_height = 1700, 700
            font_size_max = 100
            font_size = font_size_max
            font = truetype('seguiemj.ttf', size=font_size)
            wrapped_text = wrap(text, width=max_width)
            total_text_height = sum(font.getbbox(line)[3]-font.getbbox(line)[1] for line in wrapped_text)
            while total_text_height > max_height or any(font.getbbox(line)[2]-font.getbbox(line)[0] > max_width for line in wrapped_text):
                font_size -= 1
                font = truetype('seguiemj.ttf', size=font_size)
                wrapped_text = wrap(text, width=max_width // font_size)
                total_text_height = sum(font.getbbox(line)[3]-font.getbbox(line)[1] for line in wrapped_text)
            x, y = (1000 - max_width) / 2, (1000 - total_text_height) / 2
            for line in wrapped_text:
                line_width, line_height = font.getbbox(line)[2]-font.getbbox(line)[0], font.getbbox(line)[3]-font.getbbox(line)[1]
                draw.text((x + (max_width - line_width) / 2, y), text=line, font=font, fill='white')
                y += line_height
            image.save('/Data/texttoimage.jpg')
            return path + '/Data/texttoimage.jpg'

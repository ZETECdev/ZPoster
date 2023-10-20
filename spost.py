from instagrapi import Client as IGClient
from tweepy import Client as TWClient
from tweepy import API, OAuthHandler
from PIL.Image import new, open
from PIL.ImageFont import truetype
from PIL.ImageDraw import Draw
from textwrap import wrap
from os.path import dirname, abspath
from random import choice

class SPost:
    def __init__(self):
        self.twitter = self.Twitter()
        self.instagram = self.Instagram()

    class Twitter():
        def __init__(self, tw_login):
            try:
                self.twitter = TWClient(tw_login[0], tw_login[1], tw_login[2], tw_login[3], tw_login[4])
                oauth = OAuthHandler(tw_login[1], tw_login[2], tw_login[3], tw_login[4])
                self.upload = API(oauth)
            except Exception as e:
                print(f'Cant login on TW. Error: {e}')
                pass

        def tweet(self, tweet, files=None):
            if files:
                media_ids = []
                for file in files:
                    media = self.upload.media_upload(filename=file)
                    media_ids.append(media.media_id)
                self.twitter.create_tweet(text=tweet, media_ids=media_ids)     
            else:
                self.twitter.create_tweet(text=tweet)
            print('Tweet sent')

    class Instagram():
        def __init__(self, ig_login):
            try:
                self.instagram = IGClient()
                self.instagram.login(ig_login[0], ig_login[1])
            except Exception as e:
                print(f'Cant login on IG. Error: {e}')
                pass
        def post(self, picture, caption):
            self.instagram.photo_upload(picture, caption)
            print('IG post sent')   
        def reel(self, caption, picture, track):
            self.instagram.clip_upload_as_reel_with_music(picture, caption, track)
        def music_search(self, music_query):
            random_track = choice(self.instagram.search_music(music_query))
            return random_track
        
    class Utils():
        def text_to_image(text, background_img):
            this_path = dirname(abspath(__file__))
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
            x = (1000 - max_width) / 2
            y = (1000 - total_text_height) / 2
            for line in wrapped_text:
                line_width, line_height = font.getbbox(line)[2]-font.getbbox(line)[0], font.getbbox(line)[3]-font.getbbox(line)[1]
                draw.text((x + (max_width - line_width) / 2, y), text=line, font=font, fill='white')
                y += line_height
            image.save(this_path + '/texttoimage.jpg')
            text_image = this_path + '/texttoimage.jpg'
            print('Text printed on image')
            return text_image

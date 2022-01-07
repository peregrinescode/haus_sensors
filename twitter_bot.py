import twitter
import os
from dotenv import load_dotenv

load_dotenv()


consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token_key = os.environ.get("ACCESS_TOKEN_KEY")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

api = twitter.Api(consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    access_token_key=access_token_key,
                    access_token_secret=access_token_secret)


# print(api.VerifyCredentials())
# users = api.GetFriends()
# print([u.name for u in users])

# Upload image
# image = api.UploadMediaSimple('temp_AND_humidity.png')
# print(image)
status = api.PostUpdate('', media='temp_AND_humidity.png')
# print(status.text)
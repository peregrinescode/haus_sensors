import twitter
import os
import pandas as pd
from dotenv import load_dotenv


def sensorData():
    '''Read in and average the last hour of data.'''
    df = pd.read_csv('data.csv', index_col=0)

    # Specify date/time format
    df.index = pd.to_datetime(df.index)

    # Cut range
    last24h = df.last('1h')

    # Resample over a period and take mean
    averaged = last24h.resample('1H').mean()


    text2tweet =f"""{averaged.index[-1]} Sensor readings:

Temperature (C)\t: {averaged['T(off-chip)'][-1]:.1f}
Pressure (Pa)\t: {averaged['P(Pa)'][-1]:.1f}
Rel. humidity (%)\t: {averaged['H(rel%)'][-1]:.1f}
Brightness (lux)\t: {averaged['L(lux)'][-1]:.1f}"""

    return text2tweet


def tweet(text2tweet):
    '''Tweet measurements.'''

    ### Post to twitter

    load_dotenv() # keys, tokens and secrets

    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    access_token_key = os.environ.get("ACCESS_TOKEN_KEY")
    access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

    api = twitter.Api(consumer_key=consumer_key,
                        consumer_secret=consumer_secret,
                        access_token_key=access_token_key,
                        access_token_secret=access_token_secret)


    status = api.PostUpdate(text2tweet)
    
    return


if __name__ == "__main__":
    text2tweet = sensorData()
    tweet(text2tweet)
import twitter
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
sns.set_style("ticks")
sns.set_context("talk")

from dotenv import load_dotenv


def sensorData():
    '''Create graphs'''

    # Read in data from file
    df = pd.read_csv('data.csv', index_col=0)

    # Specify date/time format
    df.index = pd.to_datetime(df.index)
    last24h = df.last('38h')

    # Resample over a period and take mean
    averaged = last24h.resample('1H').mean()

    # Plot for last 6 hours
    fig, ax = plt.subplots(2,2)

    ax[0,0].plot(last24h.index, last24h['T(off-chip)'], '-')
    ax[0,1].plot(last24h.index, last24h['P(Pa)'], '-')
    ax[1,0].plot(averaged.index, averaged['H(rel%)'], '-')
    ax[1,1].plot(averaged.index, averaged['L(lux)'], '-')

    # formatter = mdates.DateFormatter('%H:%M:%S')

    for axis in ax:
        axis.xaxis.set_major_formatter(
            mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
        plt.setp(axis.get_xticklabels(), rotation = 45)

    ax[0,0].set_ylabel(u'Temperature (℃)')
    ax[0,1].set_ylabel('Pressure (Pa)')
    ax[1,0].set_ylabel('Rel. humidity %')
    ax[1,1].set_ylabel('Light intensity (lux)')

    # sns.despine()
    plt.tight_layout()
    # plt.show()
    fig.savefig('graphs.png', dpi=600, pad_inches=0.05, bbox_inches='tight')



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
    # tweet(text2tweet)
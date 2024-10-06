import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
sns.set_style("ticks")
sns.set_context("paper")

#from dotenv import load_dotenv

def sensorData():
    '''Create graphs'''

    # Read in data from file
    df = pd.read_csv('/home/ross/git/haus_sensors/data.csv', index_col=0)

    df.index = pd.to_datetime(df.index)
    
    # Get all data from todays date
    today = pd.Timestamp.today().date()
    todaysData = df[df.index.date == today]

    
    # Resample over a period and take mean
    averaged = todaysData.resample('15min').mean()

    # Plot for last 6 hours
    fig, axs = plt.subplots(3,2)

    axs[0,0].plot(averaged.index, averaged['T(off-chip)'], 'C0-')
    axs[0,1].plot(averaged.index, averaged['P(Pa)'], 'C1-')
    axs[1,0].plot(averaged.index, averaged['H(rel%)'], 'C2-')
    axs[1,1].plot(averaged.index, averaged['L(lux)'], 'C3-')
    axs[2,0].plot(averaged.index, averaged['PM2.5'], 'C4-')
    axs[2,1].plot(averaged.index, averaged['PM10'], 'C5-')

    formatter = mdates.DateFormatter('%H:%M')

    for ax in axs.reshape(-1):
        ax.xaxis.set_major_formatter(formatter)
        plt.setp(ax.get_xticklabels(), rotation = 45)

    axs[0,0].set_ylabel(u'Temperature (℃)')
    axs[0,1].set_ylabel('Pressure (Pa)')
    axs[1,0].set_ylabel('Rel. humidity %')
    axs[1,1].set_ylabel('Light intensity (lux)')
    axs[2,0].set_ylabel('PM2.5 μg/m^3')
    axs[2,1].set_ylabel('PM10 μg/m^3')

    fig.suptitle(today)

    # sns.despine()
    plt.tight_layout()
    plt.show()
    fig.savefig('graphs.png', dpi=600, pad_inches=0.05, bbox_inches='tight')
    return


def tweet():
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


    status = api.PostUpdate('Wow, the data over 24 hours. Nice!', media='graphs.png')
    
    return


if __name__ == "__main__":
    sensorData()
    # tweet()

'''
Plots temp AND humidity 
'''

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
sns.set_style("ticks")
sns.set_context("talk")

# Read in data from file
df = pd.read_csv('data.csv', index_col=0)

# Specify date/time format
df.index = pd.to_datetime(df.index)

# Cut range
last24h = df.last('38h')

# Resample over a period and take mean
averaged = last24h.resample('1H').mean()

# Plot for last 6 hours
fig, ax = plt.subplots()
ax2=ax.twinx()

# ax.plot(last24h.index, last24h['H(rel%)'], '-')
ax.plot(averaged.index, averaged['H(rel%)'], '-')
ax2.plot(averaged.index, averaged['T(off-chip)'], '-C3')

ax.xaxis.set_major_formatter(
    mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))

ax.set_ylabel('Rel. humidity %')
ax2.set_ylabel(u'Temperature (\u00B0)')

ax.tick_params(axis='y', colors='C0')
ax.yaxis.label.set_color('C0')

ax2.tick_params(axis='y', colors='C3')
ax2.yaxis.label.set_color('C3')


# sns.despine()
plt.tight_layout()
# plt.show()
fig.savefig('temp_AND_humidity.png', dpi=300, pad_inches=0.05, bbox_inches='tight')

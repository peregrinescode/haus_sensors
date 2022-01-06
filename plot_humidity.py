'''
Plots humidity over four time scales:
1) last 6hours
2) 24 hour period
3) 7 days
4) all time
'''

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
sns.set_style("ticks")
sns.set_context("paper")

# Read in data from file
df = pd.read_csv('~/git/haus_sensors/data.csv', index_col=0)

# Specify date/time format
df.index = pd.to_datetime(df.index)

# Cut ranges
last6h = df.last('6h')
last24h = df.last('7d')

print(last6h)

# Plot for last 6 hours
fig, ax = plt.subplots()

ax.plot(last24h.index, last24h['H(rel%)'], '.')

ax.xaxis.set_major_formatter(
    mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))

ax.set_ylabel('Rel. humidity %')

sns.despine()
plt.tight_layout()
plt.show()
fig.savefig('~/git/haus_sensors/humidity.png', dpi=300, pad_inches=0.05, bbox_inches='tight')

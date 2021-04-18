import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('data.csv')

fig, ax = plt.subplots()

ax.plot(df['Date'], df['P(Pa)'] / 100)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))

plt.show()
fig.savefig('pressure.png', dpi=300)

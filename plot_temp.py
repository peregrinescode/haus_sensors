import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv')

df['Date'] = pd.to_datetime(df['Date'])

fig, ax = plt.subplots()

ax.plot(df['Date'], df['T(off-chip)'], 'o')

fig.savefig('temperture.png', dpi=300)
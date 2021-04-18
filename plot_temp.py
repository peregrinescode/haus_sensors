import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv')

fig, ax = plt.subplots()

ax.plot(df['Date'], df['T(off-chip)'])

fig.savefig('temperture.png', dpi=300)
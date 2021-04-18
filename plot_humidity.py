import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv')

fig, ax = plt.subplots()

ax.plot(df['Date'], df['H(rel%)'])

plt.show()
fig.savefig('humidity.png', dpi=300)

from datetime import datetime
import matplotlib.pyplot as plt
import datetime
import numpy as np
import pandas as pd

df = pd.read_csv("../data/tsa_data.csv")
plt.figure()
ax = df.plot("Date", "Numbers", legend=False, title="TSA traffic since 2019")
ax.set_ylabel("TSA passengers processed (millions)")
plt.show()

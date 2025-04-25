#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("log.csv")
df[['prot','method','setting','iteration','nonce']] = df['query'].str.split('-',expand=True)

df['group'] = df['prot'] + '-' + df['method'] + '-' + df['setting']
df['time'] = pd.to_numeric(df['time'], errors='coerce')

plt.figure(figsize=(10, 6))
sns.boxplot(y='group', x='time', data=df)
plt.xticks(rotation=45)
plt.title('Query Time by Protocol and Setting')
plt.xlabel('Query Time (ms)')
plt.ylabel('Protocol-Setting')
plt.tight_layout()
plt.show()


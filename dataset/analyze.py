#!/usr/bin/env python3

import os
import time
import pandas as pd
import datetime
import matplotlib.pyplot as plt

def t():
    return datetime.datetime.now()


when = "feb23"
fname = f"{when}/baseline_13x1M.csv"
cols = ["TIME", "RCODE", "DOMAIN", "RRTYPE", "LATENCY"]
print(t(), "Loading datasets")
if not os.path.exists(f"{when}/processed-"+fname):
    df = pd.read_csv(fname, names=cols, nrows=10000000)
    tranco = pd.read_csv(f"{when}/tranco_663NX.csv", names=["RANK", "DOMAIN"])
    print(t(), "Merging and transforming datasets")
    df = pd.merge(df, tranco, on="DOMAIN", how="left")
    df = df[df["RANK"].notna()]
    df["DATAPOINTS"] = df.groupby("DOMAIN")["RCODE"].transform(lambda x: (x=="NOERROR").sum())
    df.to_csv(f"{when}/processed-"+fname, index=False)
else:
    df = pd.read_csv(f"{when}/processed-"+fname, header=0) 

print(df, "\n")

counts = df["RCODE"].value_counts()
percs = df["RCODE"].value_counts(normalize=True) * 100
print(pd.concat([counts,percs], axis=1, keys=['count', 'percentage']), "\n")

print(t(), "Mean LATENCY for NOERROR:", df[df["RCODE"] == "NOERROR"]["LATENCY"].mean(), "\n")
print(t(), "Median LATENCY for NOERROR:", df[df["RCODE"] == "NOERROR"]["LATENCY"].median(), "\n")
print(t(), "Mean LATENCY groupby TIME\n", 
        df.groupby("TIME", as_index=False).agg({"LATENCY": "mean"}), "\n")
print(t(), "Median LATENCY groupby TIME\n", 
        df.groupby("TIME", as_index=False).agg({"LATENCY": "median"}), "\n")

df = df[df["RCODE"] == "NOERROR"]

print(t(), "Plot LATENCY in query order:")
df["LATENCY"].plot()
plt.show()

print(t(), "Plot sorted LATENCY:")
df["LATENCY"].sort_values(ascending=True).plot(use_index=False)
plt.show()

group = df.groupby("DOMAIN", as_index=False).agg({
    "LATENCY": "mean",
    "RANK": "first",
    "DATAPOINTS": "first"
})
print(t(), "Mean LATENCY groupby DOMAIN sortby RANK:")
byrank = group.sort_values(by=["RANK"]).reset_index(drop=True)
print(byrank, "\n")

print(t(), "Plot mean LATENCY groupby DOMAIN sortby RANK:")
byrank["LATENCY"].plot()
plt.show()

#!/usr/bin/env python3

import os
import time
import pandas as pd
import datetime
import matplotlib.pyplot as plt

def t():
    return datetime.datetime.now()


when = "mar15"
locations = ["eu", "us"]
datasets = {}
tranco = "PN2YJ"

for location in locations:
    fname = f"{location}.csv"
    cols = ["TIME", "RCODE", "DOMAIN", "RRTYPE", "LATENCY"]
    print(t(), "Loading datasets")
    if not os.path.exists(f"{when}/processed-"+fname):
        df = pd.read_csv(f"{when}/{fname}", names=cols, nrows=3000000)
        tranco = pd.read_csv(f"{when}/tranco_{tranco}.csv", names=["RANK", "DOMAIN"])
        print(t(), "Merging and transforming datasets")
        df = pd.merge(df, tranco, on="DOMAIN", how="left")
        df = df[df["RANK"].notna()]
        df["DATAPOINTS"] = df.groupby("DOMAIN")["RCODE"].transform(lambda x: (x=="NOERROR").sum())
        df.to_csv(f"{when}/processed-"+fname, index=False)
    else:
        df = pd.read_csv(f"{when}/processed-"+fname, header=0) 
    datasets[location] = df


for loc in datasets.keys():
    df = datasets[loc]
    counts = df["RCODE"].value_counts()
    percs = df["RCODE"].value_counts(normalize=True) * 100
    print(f"{loc}\n", pd.concat([counts,percs], axis=1, keys=['count', 'percentage']), "\n")
    print(t(), "Mean LATENCY for NOERROR:", df[df["RCODE"] == "NOERROR"]["LATENCY"].mean(), "\n")
    print(t(), "Median LATENCY for NOERROR:", df[df["RCODE"] == "NOERROR"]["LATENCY"].median(), "\n")
    print(t(), "Mean LATENCY groupby TIME\n", df.groupby("TIME", as_index=False).agg({"LATENCY": "mean"}), "\n")
    print(t(), "Median LATENCY groupby TIME\n", df.groupby("TIME", as_index=False).agg({"LATENCY": "median"}), "\n")

print(t(), "Plot LATENCY in query order:")
for loc in datasets.keys():
    df = datasets[loc]
    df = df[df["RCODE"] == "NOERROR"]
    df["LATENCY"].plot(label=loc)
plt.legend(loc='best')
plt.show()

print(t(), "Plot sorted LATENCY:")
for loc in datasets.keys():
    df = datasets[loc]
    df = df[df["RCODE"] == "NOERROR"]
    df["LATENCY"].sort_values(ascending=True).plot(use_index=False, label=loc)
plt.legend(loc='best')
plt.show()

print(t(), "Plot mean LATENCY groupby DOMAIN sortby RANK:")
for loc in datasets.keys():
    df = datasets[loc]
    df = df[df["RCODE"] == "NOERROR"]
    group = df.groupby("DOMAIN", as_index=False).agg({
        "LATENCY": "mean",
        "RANK": "first",
        "DATAPOINTS": "first"
    })
    byrank = group.sort_values(by=["RANK"]).reset_index(drop=True)
    byrank["LATENCY"].plot(label=loc)
plt.legend(loc='best')
plt.show()


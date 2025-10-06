#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
plt.rcParams.update({'font.size': 14})

height = 6
width = 8
scale = 0.8

TO_LATEX = False

def plot_one(dframe):
    # torrc vs carml+stem
    settings_order = ['any2any2any', 'se2any2any', 'se2any2se']
    methods_order = ['torrc', 'carml+stem']

    df = dframe.copy()
    df[['method', 'setting']] = df['group'].str.split('\n', n=1, expand=True)

    df['pair'] = df['setting'] + '||' + df['method']

    pair_order = [
        f"{setting}||{method}"
        for setting in settings_order
        for method in methods_order
    ]

    ticklabels = [m for _ in settings_order for m in methods_order]

    plt.figure(figsize=(width, height*scale))
    ax = sns.boxplot(
        y='pair', x='time', data=df,
        showfliers=False, order=pair_order
    )

    ax.set_yticklabels(ticklabels)

    middle_index = 2  
    rect = patches.Rectangle(
        (ax.get_xlim()[0], middle_index - 0.5),
        width=ax.get_xlim()[1] - ax.get_xlim()[0],
        height=len(methods_order),  
        color='gray', alpha=0.1, zorder=0
    )
    ax.add_patch(rect)

    for i, setting in enumerate(settings_order):
        y_center = i * len(methods_order) + (len(methods_order) - 1) / 2.0
        ax.text(
            1.01, y_center, setting,
            va='center', ha='left', transform=ax.get_yaxis_transform()
        )

    plt.subplots_adjust(right=0.85)
    plt.xticks(rotation=45)
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Method')
    plt.tight_layout()
    if TO_LATEX: plt.savefig('../latex/img/p1.pdf')
    plt.savefig('p1.png')
    # plt.show()

def plot_one_old(dframe):
    settings_order = ['any2any2any', 'se2any2any', 'se2any2se']
    methods_order = ['torrc', 'carml+stem']
    group_order = [
        f"{method}\n{setting}"
        for setting in settings_order
        for method in methods_order
    ]

    plt.figure(figsize=(width, height))
    ax = sns.boxplot(
        y='group', x='time', data=dframe, 
        showfliers=False, order=group_order
    )

    middle_index = 2  
    rect = patches.Rectangle(
        (ax.get_xlim()[0], middle_index - 0.5),  
        width=ax.get_xlim()[1] - ax.get_xlim()[0],
        height=2,  
        color='gray',
        alpha=0.1,
        zorder=0
    )
    ax.add_patch(rect)

    plt.xticks(rotation=45)
    #plt.title('Query Time by Configuration (torrc vs carml+stem)')
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Configuration')
    plt.tight_layout()
    if TO_LATEX: plt.savefig('../latex/img/p1.pdf')
    plt.savefig('p1.png')
    #plt.show()


def plot_two(dframe):
    # Sweden Middle
    plt.figure(figsize=(width, (height-1)*scale))
    sns.boxplot(y='setting', x='time', data=dframe, showfliers=False)
    plt.xticks(rotation=45)
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Circuit')
    plt.tight_layout()
    if TO_LATEX: plt.savefig('../latex/img/p2.pdf')
    plt.savefig('p2.png')
    #plt.show()


def plot_three(dframe):
    # Two-Hop
    plt.figure(figsize=(width, (height-2)*scale))
    sns.boxplot(y='setting', x='time', data=dframe, showfliers=False)
    plt.xticks(rotation=45)
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Circuit')
    plt.tight_layout()
    if TO_LATEX: plt.savefig('../latex/img/p3.pdf')
    plt.savefig('p3.png')
    #plt.show()

def plot_four(dframe):
    # DoTor
    plt.figure(figsize=(width, (height-2)*scale))
    sns.boxplot(y='setting', x='time', data=dframe, showfliers=False)
    plt.xticks(rotation=45)
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Circuit')
    plt.tight_layout()
    if TO_LATEX: plt.savefig('../latex/img/p4.pdf')
    plt.savefig('p4.png')
    #plt.show()

def plot_five(dframe):
    # DoHoT vs Optimised vs ODoH 
    dframe['ylabel'] = df['prot'] + '\n' + df['setting']
    plt.figure(figsize=(width, (height-1.5)*scale))
    ax = sns.boxplot(y='ylabel', x='time', data=dframe, showfliers=False)
    ax.set_yticklabels(["DoHoT\ndefault", "DoHoT\nse2se", "DoTor\nse2se", "ODoH\nse"])
    plt.xticks(rotation=45)
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Approach')
    plt.tight_layout()
    if TO_LATEX: plt.savefig('../latex/img/p5.pdf')
    plt.savefig('p5.png')
    #plt.show()



df = pd.read_csv("log.csv")
df[['prot','method','setting','iteration','nonce']] = df['query'].str.split('-',expand=True)
df['method'] = df['method'].str.replace('carml','carml+stem')
df['group'] = df['method'] + '\n' + df['setting']
df['all'] = df['prot'] +'-'+ df['method'] +'-'+ df['setting']
df['time'] = pd.to_numeric(df['time'], errors='coerce')
print(df)



# First plot: torrc vs carml+stem
tmp = df[
        (df['prot'] == "dohot") & 
        (df['setting'] == "any2any2any")]
tmp = pd.concat([tmp, df[
        (df['prot'] == "dohot") & 
        (df['setting'] == "se2any2any")]], sort=False)
tmp = pd.concat([tmp, df[
        (df['prot'] == "dohot") & 
        (df['setting'] == "se2any2se")]], sort=False)
print(tmp)
plot_one(tmp)

# Second plot: middle relay
tmp = df[
        (df['prot'] == "dohot") & 
        (df['method'] == "carml+stem") & 
        (df['setting'] == "se2any2se")] # for comparison
tmp = pd.concat([tmp, df[
        (df['prot'] == "dohot") & 
        (df['setting'] == "any2se2any")]], sort=False)
tmp = pd.concat([tmp, df[
        (df['prot'] == "dohot") & 
        (df['setting'] == "any2se2se")]], sort=False)
tmp = pd.concat([tmp, df[
        (df['prot'] == "dohot") & 
        (df['setting'] == "se2se2any")]], sort=False)
tmp = pd.concat([tmp, df[
        (df['prot'] == "dohot") & 
        (df['setting'] == "se2se2se")]], sort=False)
print(tmp)
plot_two(tmp)

# Third plot: two-hops
tmp = df[
        (df['prot'] == "dohot") & 
        (df['setting'] == "any2any")]
tmp = pd.concat([tmp, df[
        (df['prot'] == "dohot") & 
        (df['setting'] == "any2se")]], sort=False)
tmp = pd.concat([tmp, df[
        (df['prot'] == "dohot") & 
        (df['setting'] == "se2any")]], sort=False)
tmp = pd.concat([tmp, df[
        (df['prot'] == "dohot") & 
        (df['setting'] == "se2se")]], sort=False)
print(tmp)
plot_three(tmp)

# Fourth plot: DoTor
tmp = df[
        (df['prot'] == "dotor") & 
        (df['method'] == "carml+stem") & 
        (df['setting'] == "any2any2any")]
tmp = pd.concat([tmp, df[
        (df['prot'] == "dotor") & 
        (df['method'] == "carml+stem") & 
        (df['setting'] == "se2se2se")]], sort=False)
tmp = pd.concat([tmp, df[
        (df['prot'] == "dotor") & 
        (df['method'] == "carml+stem") & 
        (df['setting'] == "se2se")]], sort=False)
print(tmp)
plot_four(tmp)

# Fifth plot: old dohot, new dohot, odoh
tmp = df[
        (df['prot'] == "dohot") & 
        (df['method'] == "torrc") & 
        (df['setting'] == "any2any2any")] # old dohot
tmp = pd.concat([tmp, df[
        (df['prot'] == "dohot") & 
        (df['method'] == "carml+stem") & 
        (df['setting'] == "se2se")]], sort=False) # new dohot
tmp = pd.concat([tmp, df[
        (df['prot'] == "dotor") & 
        (df['method'] == "carml+stem") & 
        (df['setting'] == "se2se")]], sort=False) # new dotor
tmp = pd.concat([tmp, df[df['prot'] == "odoh"]], sort=False) # odoh
print(tmp)
plot_five(tmp)

group_stats_df = df.groupby('all', as_index=False).agg(
    mean_time=('time', 'mean'),
    median_time=('time', 'median'),
    std_time=('time', 'std')
)
group_stats_df['rel_std_pct'] = (group_stats_df['std_time'] / group_stats_df['mean_time']) * 100
print(group_stats_df)


#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
plt.rcParams.update({'font.size': 14})

height = 5
width = 8

def plot_one(dframe):
    settings_order = ['any2any2any', 'se2any2any', 'se2any2se']
    methods_order = ['torrc', 'carml+stem']

    # Parse original "method\nsetting" column into separate cols
    df = dframe.copy()
    df[['method', 'setting']] = df['group'].str.split('\n', n=1, expand=True)

    # Make a y-category that distinguishes all 6 rows (3 settings × 2 methods)
    df['pair'] = df['setting'] + '||' + df['method']

    # Full plotting order: for each setting, both methods
    pair_order = [
        f"{setting}||{method}"
        for setting in settings_order
        for method in methods_order
    ]

    # What we want to show on the ticks: just the method (repeats every row-pair)
    ticklabels = [m for _ in settings_order for m in methods_order]

    plt.figure(figsize=(width, height-0.5))
    ax = sns.boxplot(
        y='pair', x='time', data=df,
        showfliers=False, order=pair_order
    )

    # Replace y tick labels with just the method names
    ax.set_yticklabels(ticklabels)

    # Light highlight behind the middle setting (rows 2 and 3; 0-based)
    middle_index = 2  # start index of the middle pair
    rect = patches.Rectangle(
        (ax.get_xlim()[0], middle_index - 0.5),
        width=ax.get_xlim()[1] - ax.get_xlim()[0],
        height=len(methods_order),  # span exactly the 2 rows of that setting
        color='gray', alpha=0.1, zorder=0
    )
    ax.add_patch(rect)

    # Add setting labels on the right, centered over each pair of method rows
    # Use axis-fraction for x so labels sit just outside the right spine.
    for i, setting in enumerate(settings_order):
        y_center = i * len(methods_order) + (len(methods_order) - 1) / 2.0
        ax.text(
            1.01, y_center, setting,
            va='center', ha='left', transform=ax.get_yaxis_transform()
        )

    # Make a bit of room on the right for those labels
    plt.subplots_adjust(right=0.85)

    plt.xticks(rotation=45)
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Method')
    plt.tight_layout()
    plt.savefig('../latex/img/p1.pdf')
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
    plt.savefig('../latex/img/p1.pdf')
    plt.savefig('p1.png')
    #plt.show()


def plot_two(dframe):
    plt.figure(figsize=(width, height-0.7))
    sns.boxplot(y='setting', x='time', data=dframe, showfliers=False)
    plt.xticks(rotation=45)
    #plt.title('Query Time by Configuration (Sweden Middle)')
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Circuit')
    plt.tight_layout()
    plt.savefig('../latex/img/p2.pdf')
    plt.savefig('p2.png')
    #plt.show()


def plot_three(dframe):
    plt.figure(figsize=(width, height-1))
    sns.boxplot(y='setting', x='time', data=dframe, showfliers=False)
    plt.xticks(rotation=45)
    #plt.title('Query Time by Configuration (Two-Hop)')
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Circuit')
    plt.tight_layout()
    plt.savefig('../latex/img/p3.pdf')
    plt.savefig('p3.png')
    #plt.show()

def plot_four(dframe):
    dframe['ylabel'] = df['prot'] + '\n' + df['setting']
    plt.figure(figsize=(width, height-1.5))
    ax = sns.boxplot(y='ylabel', x='time', data=dframe, showfliers=False)
    ax.set_yticklabels(["DoHoT", "se2se", "ODoH"])
    plt.xticks(rotation=45)
    #plt.title('Query Time by Configuration (DoHoT vs Optimised vs ODoH)')
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Approach')
    plt.tight_layout()
    plt.savefig('../latex/img/p4.pdf')
    plt.savefig('p4.png')
    #plt.show()



df = pd.read_csv("log.csv")
df[['prot','method','setting','iteration','nonce']] = df['query'].str.split('-',expand=True)
df['method'] = df['method'].str.replace('carml','carml+stem')
df['group'] = df['method'] + '\n' + df['setting']
df['time'] = pd.to_numeric(df['time'], errors='coerce')
print(df)

group_avg_df = df.groupby('group', as_index=False)['time'].mean()
print(group_avg_df)


# First plot: torrc vs carml+stem
tmp = df[df['setting'] == "any2any2any"]
tmp = pd.concat([tmp, df[df['setting'] == "se2any2any"]], sort=False)
tmp = pd.concat([tmp, df[df['setting'] == "se2any2se"]], sort=False)
print(tmp)
plot_one(tmp)

# Second plot: middle relay
tmp = df[(df['method'] == "carml+stem") & (df['setting'] == "se2any2se")] # for comparison
tmp = pd.concat([tmp, df[df['setting'] == "any2se2any"]], sort=False)
tmp = pd.concat([tmp, df[df['setting'] == "any2se2se"]], sort=False)
tmp = pd.concat([tmp, df[df['setting'] == "se2se2any"]], sort=False)
tmp = pd.concat([tmp, df[df['setting'] == "se2se2se"]], sort=False)
print(tmp)
plot_two(tmp)

# Third plot: two-hops
tmp = df[df['setting'] == "any2any"]
tmp = pd.concat([tmp, df[df['setting'] == "any2se"]], sort=False)
tmp = pd.concat([tmp, df[df['setting'] == "se2any"]], sort=False)
tmp = pd.concat([tmp, df[df['setting'] == "se2se"]], sort=False)
print(tmp)
plot_three(tmp)

# Fourth plot: old dohot, new dohot, odoh
tmp = df[(df['method'] == "torrc") & (df['setting'] == "any2any2any")] # old dohot
#tmp = pd.concat([tmp, df[df['setting'] == "au2se2au"]], sort=False) # worst circuit
tmp = pd.concat([tmp, df[(df['method'] == "carml+stem") & (df['setting'] == "se2se")]], sort=False) # new dohot
tmp = pd.concat([tmp, df[df['prot'] == "odoh"]], sort=False) # odoh
print(tmp)
plot_four(tmp)




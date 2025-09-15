#!/usr/bin/env python3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
plt.rcParams.update({'font.size': 16})

height = 5
width = 8

def plot_one(dframe):
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
    #plt.savefig('../latex/img/p1.pdf')
    plt.savefig('p1.png')
    plt.show()


def plot_two(dframe):
    plt.figure(figsize=(width, height+1))
    sns.boxplot(y='setting', x='time', data=dframe, showfliers=False)
    plt.xticks(rotation=45)
    #plt.title('Query Time by Configuration (Sweden Middle)')
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Configuration')
    plt.tight_layout()
    #plt.savefig('../latex/img/p2.pdf')
    plt.savefig('p2.png')
    plt.show()


def plot_three(dframe):
    plt.figure(figsize=(width, height))
    sns.boxplot(y='setting', x='time', data=dframe, showfliers=False)
    plt.xticks(rotation=45)
    #plt.title('Query Time by Configuration (Two-Hop)')
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Configuration')
    plt.tight_layout()
    #plt.savefig('../latex/img/p3.pdf')
    plt.savefig('p3.png')
    plt.show()

def plot_four(dframe):
    dframe['ylabel'] = df['prot'] + '\n' + df['setting']
    plt.figure(figsize=(width, height-1))
    sns.boxplot(y='ylabel', x='time', data=dframe, showfliers=False)
    plt.xticks(rotation=45)
    #plt.title('Query Time by Configuration (DoHoT vs Optimised vs ODoH)')
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Configuration')
    plt.tight_layout()
    #plt.savefig('../latex/img/p4.pdf')
    plt.savefig('p4.png')
    plt.show()



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




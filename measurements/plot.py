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

ANONYMIZE = False
def _anon(s: str) -> str:
    return s.replace('se', 'xx') if ANONYMIZE else s


def plot_one(dframe, xmax=None):
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
    if xmax:
        ax.set_xlim(0, xmax)
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
            1.01, y_center, _anon(setting), # added _anon()
            va='center', ha='left', transform=ax.get_yaxis_transform()
        )

    plt.subplots_adjust(right=0.85)
    plt.xticks(rotation=45)
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Method')
    plt.tight_layout()
    if TO_LATEX: plt.savefig('../latex/img/p1.pdf')
    plt.savefig('p1.png')
    plt.savefig('pdfs/p1.pdf')
    # plt.show()

def plot_one_old(dframe, xmax=None):
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

    if xmax:
        ax.set_xlim(0, xmax)
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
    plt.savefig('pdfs/p1.pdf')
    #plt.show()


def plot_two(dframe, xmax=None):
    # Sweden Middle
    plt.figure(figsize=(width, (height-1)*scale))
    ax = sns.boxplot(y='setting', x='time', data=dframe, showfliers=False)
    if xmax: ax.set_xlim(0, xmax)
    ax.set_yticklabels([_anon(t.get_text()) for t in ax.get_yticklabels()]) # new
    plt.xticks(rotation=45)
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Circuit')
    plt.tight_layout()
    if TO_LATEX: plt.savefig('../latex/img/p2.pdf')
    plt.savefig('p2.png')
    plt.savefig('pdfs/p2.pdf')
    #plt.show()


def plot_three(dframe, xmax=None):
    # Two-Hop
    plt.figure(figsize=(width, (height-2)*scale))
    ax = sns.boxplot(y='setting', x='time', data=dframe, showfliers=False)
    if xmax: ax.set_xlim(0, xmax)
    ax.set_yticklabels([_anon(t.get_text()) for t in ax.get_yticklabels()]) # new
    plt.xticks(rotation=45)
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Circuit')
    plt.tight_layout()
    if TO_LATEX: plt.savefig('../latex/img/p3.pdf')
    plt.savefig('p3.png')
    plt.savefig('pdfs/p3.pdf')
    #plt.show()

def plot_four(dframe, xmax=None):
    # DoTor
    plt.figure(figsize=(width, (height-2)*scale))
    ax = sns.boxplot(y='setting', x='time', data=dframe, showfliers=False)
    if xmax: ax.set_xlim(0, xmax)
    ax.set_yticklabels([_anon(t.get_text()) for t in ax.get_yticklabels()]) # new
    plt.xticks(rotation=45)
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Circuit')
    plt.tight_layout()
    if TO_LATEX: plt.savefig('../latex/img/p4.pdf')
    plt.savefig('p4.png')
    plt.savefig('pdfs/p4.pdf')
    #plt.show()

def plot_five(dframe, xmax=None):
    # DoHoT vs Optimised vs ODoH 
    # dframe['ylabel'] = df['prot'] + '\n' + df['setting']
    dframe['ylabel'] = dframe['prot'] + '\n' + dframe['setting']
    plt.figure(figsize=(width, (height-0.5)*scale))
    ax = sns.boxplot(y='ylabel', x='time', data=dframe, showfliers=False)
    if xmax: ax.set_xlim(0, xmax)
    # new replacement
    ax.set_yticklabels([_anon(s) for s in [
        "DoHoT\ndefault", "DoHoT\nse2se", "DoTor\ndefault", "DoTor\nse2se", "ODoH\nse"
    ]])
    #ax.set_yticklabels(["DoHoT\ndefault", "DoHoT\nse2se", "DoTor\ndefault", "DoTor\nse2se", "ODoH\nse"])
    plt.xticks(rotation=45)
    plt.xlabel('Query Time (ms)')
    plt.ylabel('Approach')
    plt.tight_layout()
    if TO_LATEX: plt.savefig('../latex/img/p5.pdf')
    plt.savefig('p5.png')
    plt.savefig('pdfs/p5.pdf')
    #plt.show()

def print_percentiles(dframe):
    def pct(series):
        return series.quantile([0.05, 0.50, 0.95])

    # Default DoHoT
    default_dohot = dframe[
        (dframe['prot'] == 'dohot') &
        (dframe['method'] == 'torrc') &
        (dframe['setting'] == 'any2any2any')
    ]['time']

    # Optimized DoHoT
    optimized_dohot = dframe[
        (dframe['prot'] == 'dohot') &
        (dframe['method'] == 'carml+stem') &
        (dframe['setting'] == 'se2se')
    ]['time']

    # Default DoTor
    default_dotor = dframe[
        (dframe['prot'] == 'dotor') &
        (dframe['method'] == 'torrc') &
        (dframe['setting'] == 'any2any2any')
    ]['time']

    # Optimized DoTor
    optimized_dotor = dframe[
        (dframe['prot'] == 'dotor') &
        (dframe['method'] == 'carml+stem') &
        (dframe['setting'] == 'se2se')
    ]['time']

    # ODoH
    odoh = dframe[(dframe['prot'] == 'odoh')]['time']

    print("\nLatency Percentiles (ms)")
    print("--------------------------------")

    for label, series in [
        ("Default DoHoT (torrc, any2any2any)", default_dohot),
        ("Optimized DoHoT (carml+stem, se2se)", optimized_dohot),
        ("Default DoTor (torrc, any2any2any)", default_dotor),
        ("Optimized DoTor (carml+stem, se2se)", optimized_dotor),
        ("ODoH (se)", odoh)
    ]:
        if series.empty:
            print(f"{label}: no data")
            continue

        p = pct(series)
        print(
            f"{label:30s} "
            f"5/50/95 = "
            f"{p.loc[0.05]:.1f} / "
            f"{p.loc[0.50]:.1f} / "
            f"{p.loc[0.95]:.1f} ms"
        )


# Main ==============================================


df = pd.read_csv("log.csv")
df[['prot','method','setting','iteration','nonce']] = df['query'].str.split('-',expand=True)
df['method'] = df['method'].str.replace('carml','carml+stem')
df['group'] = df['method'] + '\n' + df['setting']
df['all'] = df['prot'] +'-'+ df['method'] +'-'+ df['setting']
df['time'] = pd.to_numeric(df['time'], errors='coerce')
#xmax = df['time'].max()
xmax = df['time'].quantile(0.98)
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
plot_one(tmp, xmax)

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
plot_two(tmp, xmax)

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
plot_three(tmp, xmax)

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
plot_four(tmp, xmax)

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
        (df['method'] == "torrc") & 
        (df['setting'] == "any2any2any")]], sort=False) # old dotor
tmp = pd.concat([tmp, df[
        (df['prot'] == "dotor") & 
        (df['method'] == "carml+stem") & 
        (df['setting'] == "se2se")]], sort=False) # new dotor
tmp = pd.concat([tmp, df[df['prot'] == "odoh"]], sort=False) # odoh
print(tmp)
plot_five(tmp, xmax)

group_stats_df = df.groupby('all', as_index=False).agg(
    mean_time=('time', 'mean'),
    median_time=('time', 'median'),
    std_time=('time', 'std')
)
group_stats_df['rel_std_pct'] = (group_stats_df['std_time'] / group_stats_df['mean_time']) * 100
print(group_stats_df)


print_percentiles(df)

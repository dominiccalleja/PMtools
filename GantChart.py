
"""
Gant chart tooling
"""
import pandas as pd 
import numpy as np
from datetime import date, timedelta
import matplotlib.pyplot as plt

def plot_interval(y, s0, s1, ax):
    if (s1-s0).days == 1:
        ax.plot([s0, s1], [y,y], c='green', linewidth = 5)
    else:
        ax.plot([s0, s1], [y,y], c='k', linewidth = 5)
    if s0 == s1:
        ax.scatter(s0, y, c='k', s=100, marker='+')
    # ax.plot(s, s+x1, c='k', linewidth = 1)
    return ax

def plot_dependence(y0, y1, s0, s1, ax):
    ax.arrow(s0, y0, 0, y1-y0, head_width=1, head_length=1, length_includes_head=True, color='red')
    ax.plot([s0,s1],[y1,y1], c='r')
    # ax.plot([s0, s1], [y1,y1], c='r')
    # if not s0 == s1:
    #     ax.arrow(s0, y1, (s0-s1).days, 0, head_width=.5,
    #              head_length=.5, length_includes_head=True)
    #     # ax.arrow(s0, y1, s1-s0, 0, c='r')
    return ax

def compute_dependency_date(df, start_date ):
    dep = {}
    for i in df.index:
        d = str(df.loc[i, 'PreReq'])
        dep[df.loc[i, 'Task No.']] = (d.split(','))

    for i in df.index:
        # if i == df.index[-1]:
        #     break
        # else:
        idT = df.loc[i, 'Task No.']

        print(idT)

        D = dep[idT]
        if not D[0] == 'nan':
            start = max([df.loc[df['Task No.']==d, 'endDate'].values[0] for d in D])
        else:
            start = start_date    
    
        df.loc[i, 'startDate'] = start
        if not np.isnan(df.loc[i, 'Duration L']):
            df.loc[i, 'endDate'] = start + \
                timedelta(days=int(max(df.loc[i, 'Duration L'], df.loc[i, 'Duration U'])))
        else:
            df.loc[i, 'endDate'] = df.loc[i, 'startDate']
        #TODO: Modify to compute tree based on both lower and upper bounds 
    return df, dep

def plot_gant(df, figsize = (60,30), save_address = None, labelsize='20'):

    H = df.index[-1]
    fig, ax = plt.subplots(1,1, figsize=figsize, tight_layout=True)
    for i in df.index:

        # x0 = timedelta(days=df.loc[i, 'Duration L'])
        # x1 = timedelta(days=df.loc[i, 'Duration U'])
        ax = plot_interval(
            H - i, df.loc[i, 'startDate'], df.loc[i, 'endDate'], ax)

        for d in dependency[df.loc[i, 'Task No.']]:
            if d == 'nan':
                continue
            i0 = df.index[df.loc[:, 'Task No.']==d][0]
            y0 = H - i0
            y1 = H - i 
            ax = plot_dependence(y0, y1, df.loc[i0, 'endDate'], df.loc[i, 'startDate'], ax)

    ax.set_yticks(df.index[-1]-df.index.values, ['{} - {}'.format(df.loc[i, 'Task No.'], df.loc[i, 'Label']) for i in df.index])
    ax.tick_params(axis='both', labelsize=labelsize)
    ax.xaxis.set_ticks_position('top')
    if isinstance(save_address, str):
        plt.savefig(save_address, tight_layout=True, transparent=False, facecolor=fig.get_facecolor(), edgecolor='white')
    plt.show()




## Pre processing
# pd0 = pd.read_excel('/Users/DCLJ/DB/working_dir/GCP onboarding - Tracker.xlsx', sheet_name='dbTPRM')
# labels = pd0['RR'].iloc[1:57].values

# Labs = {}
# for l in labels:
#     if isinstance(l, str):
#         Labs[l.split(' ')[0]] =' '.join(l.split(' ')[1:])

# missing_labels = []
# for i in gant.index:
#     try:
#         gant.loc[i, 'Label'] = Labs[str(gant.loc[i,'Task No.'])]
#     except:
#         missing_labels.append(str(gant.loc[i,'Task No.']))
#         print(str(gant.loc[i,'Task No.']) + ' not in list availiable')


# gant['Status'] = ''
# gant.to_excel('/Users/DCLJ/Documents/PMTools/example/gant_chart_example_v1.xlsx')
## Quick clean


if __name__=='__main__':
    
    gant = pd.read_excel('example/gant_chart_example_v2.xlsx', index_col=[0])
    gant.loc[np.isnan(gant['Duration L']),'Duration L'] = 1 
    gant = gant.reset_index(drop=True)

    gant.to_excel(
        'example/GCP-onboarding-ActivitiesPlan.xlsx')

    start_date = date.today()
    df, dependency = compute_dependency_date(gant, start_date)
    plot_gant(df, figsize=(
        60, 30), save_address='example/GCP-gantchart-integrationplan-v1-reduced.png')

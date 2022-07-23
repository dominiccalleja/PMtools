
from datetime import date, timedelta
import pandas as pd
import numpy as np 

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def props(cls):
  return [i for i in cls.__dict__.keys() if i[:1] != '_']


def is_workday(date_in):
    if date_in.weekday() > 4:
        return False
    return True


def is_weekend(date_in):
    return not is_workday(date_in)


def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days


def recursive_weekend_check(start, end):
    DC = date_range(start, end)
    c = sum([is_weekend(i) for i in DC])
    while c > 0:
        end0 = end
        end = end+timedelta(days=c)
        DC = date_range(end0, end)
        c = sum([is_weekend(i) for i in DC])
    return end


def compute_dependency_date(df, start_date, upper_bound=True):
    dep = {}
    for i in df.index:
        d = str(df.loc[i, 'prerequisites'])
        dep[df.loc[i, 'id']] = (d.split(','))

    for i in df.index:
        idT = df.loc[i, 'id']

        D = dep[idT]
        if not D[0] == 'nan':
            start = max(
                [df.loc[df['id'] == d, 'end_date'].values[0] for d in D])
        else:
            start = start_date

        df.loc[i, 'start_date'] = start
        if not np.isnan(df.loc[i, 'duration']):
            if upper_bound:
                endDate = start + timedelta(
                        days=int(max(df.loc[i, 'duration'], df.loc[i, 'duration_u'])))
            else:
                endDate = start + timedelta(
                        days=int(df.loc[i, 'duration']))

            endDate = recursive_weekend_check(start, endDate)
        else:
            endDate = df.loc[i, 'start_date']
        
        df.loc[i, 'end_date'] = endDate
    return df, dep


def plot_interval(y, s0, s1, ax):
    if (s1-s0).days == 1:
        ax.plot([s0, s1], [y, y], c='green', linewidth=5)
    else:
        ax.plot([s0, s1], [y, y], c='k', linewidth=5)
    if s0 == s1:
        ax.scatter(s0, y, c='k', s=100, marker='+')
    # ax.plot(s, s+x1, c='k', linewidth = 1)
    return ax


def plot_milestone(y, s0, s1, ax):
    ax.plot([s0, s1], [y, y], c='green', linewidth=5)
    ax.scatter(s1, y, marker = "D", s = 200, c='green')
    # if (s1-s0).days == 1:
    #     ax.plot([s0, s1], [y, y], c='green', linewidth=5)
    # else:
    #     ax.plot([s0, s1], [y, y], c='k', linewidth=5)
    # if s0 == s1:
    #     ax.scatter(s0, y, c='k', s=100, marker='+')
    # ax.plot(s, s+x1, c='k', linewidth = 1)
    return ax


def plot_dependence(y0, y1, s0, s1, ax):
    ax.arrow(s0, y0, 0, y1-y0, head_width=1, head_length=1,
             length_includes_head=True, color='red')
    ax.plot([s0, s1], [y1, y1], c='r')
    # ax.plot([s0, s1], [y1,y1], c='r')
    # if not s0 == s1:
    #     ax.arrow(s0, y1, (s0-s1).days, 0, head_width=.5,
    #              head_length=.5, length_includes_head=True)
    #     # ax.arrow(s0, y1, s1-s0, 0, c='r')
    return ax


def plot_gant(df, dependency, figsize=(60, 30), save_address=None, labelsize='32'):

    H = df.index[-1]
    fig, ax = plt.subplots(1, 1, figsize=figsize, tight_layout=True)

    DC = date_range(df.loc[0, 'start_date'],  df.loc[df.index[-1], 'end_date'])
    
    c = 0
    for d in DC:
        if is_weekend(d):
            ax.fill_betweenx([0, len(df.index)], x1 = d-timedelta(days=.5),
                             x2=d+timedelta(days=0.5), color='grey', alpha=0.4)
        c+=1

    for i in df.index:
        # x0 = timedelta(days=df.loc[i, 'Duration L'])
        # x1 = timedelta(days=df.loc[i, 'Duration U'])
        if any(['A' in df.loc[i, 'id'],'R' in df.loc[i, 'id']]):
            ax = plot_milestone(
                H - i, df.loc[i, 'start_date'], df.loc[i, 'end_date'], ax)
        else:
            ax = plot_interval(
                H - i, df.loc[i, 'start_date'], df.loc[i, 'end_date'], ax)

        for d in dependency[df.loc[i, 'id']]:
            if d == 'nan':
                continue
            i0 = df.index[df.loc[:, 'id'] == d][0]
            y0 = H - i0
            y1 = H - i
            ax = plot_dependence(
                y0, y1, df.loc[i0, 'end_date'], df.loc[i, 'start_date'], ax)

    ax.set_yticks(df.index[-1]-df.index.values, ['{} - {}'.format(
        df.loc[i, 'id'], df.loc[i, 'label']) for i in df.index])
    ax.tick_params(axis='both', labelsize=labelsize)
    ax.xaxis.set_ticks_position('top')
    ax.plot([date.today(), date.today()],
            [-1, len(df.index)], c='gold', linewidth=5)
    ax.text(date.today(),1, 'Today',fontsize=54, color='gold')
    ax.set_ylim([-1, len(df.index)])
    ax.set_xlim(df.loc[0, 'start_date'],  df.loc[df.index[-1], 'end_date'])
    ax.xaxis.set_major_locator(mdates.DayLocator([1,7,14,21,28]))   #to get a tick every 15 minutes
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%D%M'))  
    if isinstance(save_address, str):
        plt.savefig(save_address, tight_layout=True, transparent=False,
                    facecolor=fig.get_facecolor(), edgecolor='white')
    
    plt.show()

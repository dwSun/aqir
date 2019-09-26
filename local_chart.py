#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import requests
import math

dust_label = ['dust0-3', 'dust0-5', 'dust1-0', 'dust2-5', 'dust5-0', 'dust10']
pm_label = ['pm1-0_std', 'pm1-0_atm', 'pm2-5_std',
            'pm2-5_atm', 'pm10_std', 'pm10_atm']

dust_color = {'dust0-5': 'green', 'dust0-3': 'yellow', 'dust10': 'blue',
              'dust2-5': 'red', 'dust1-0': 'orange', 'dust5-0': 'black'}
pm_color = {'pm10_atm': 'blue', 'pm10_std': 'blue', 'pm2-5_std': 'red',
            'pm2-5_atm': 'red', 'pm1-0_std': 'orange', 'pm1-0_atm': 'orange', }


dust_value = []
pm_value = []

hist_dust_value = {}
hist_pm_value = {}
hist_ts = []
hist_time = []
for dust in dust_label:
    if dust not in hist_dust_value:
        hist_dust_value[dust] = []

for pm in pm_label:
    if pm not in hist_pm_value:
        hist_pm_value[pm] = []


def get_data():
    rec = requests.get('http://192.168.2.199:5001/period').json()
    hist = requests.get('http://192.168.2.199:5001/last').json()

    dust_value.clear()
    pm_value.clear()

    dust_value.extend([rec[dust] for dust in dust_label])
    pm_value.extend([rec[pm] for pm in pm_label])

    hist_ts.clear()
    hist_time.clear()

    for dust in dust_label:
        hist_dust_value[dust] = []

    for pm in pm_label:
        hist_pm_value[pm] = []

    for rec in hist:
        for dust in dust_label:
            hist_dust_value[dust].append(rec[dust])

        for pm in pm_label:
            hist_pm_value[pm].append(rec[pm])

        hist_ts.append(rec['timestamp'])
        hist_time.append(rec['time'])


get_data()

dust_max = max([max(vs) for k, vs in hist_dust_value.items()])
pm_max = max([max(vs) for k, vs in hist_pm_value.items()])

ind_dust = np.arange(len(dust_label)) * 2  # the x locations for the groups
ind_pm = np.arange(len(pm_label)) * 2  # the x locations for the groups
width = 1       # the width of the bars

fig, axs = plt.subplots(2, 2)


ax_line_dust = axs[0][0]
ax_line_pm = axs[0][1]
ax_dust = axs[1][0]
ax_pm = axs[1][1]


x = range(len(hist_ts))

lines_dust = [ax_line_dust.plot(x, hist_dust_value[dust],
                                linewidth=width, color=dust_color[dust]) for dust in dust_label]

lines_pm = [ax_line_pm.plot(x, hist_pm_value[pm],
                            linewidth=width, color=pm_color[pm])for pm in pm_label]

rects_dust = [ax_dust.bar(ind_dust[i], dust_value[i], width,
                          color=dust_color[v]) for i, v in enumerate(dust_label)]

rects_pm = [ax_pm.bar(ind_pm[i], pm_value[i], width, color=pm_color[v])
            for i, v in enumerate(pm_label)]

# add some text for labels, title and axes ticks
ax_dust.set_ylabel('Dust count')
ax_pm.set_ylabel('pm index')
ax_line_dust.set_ylabel('Dust count')
ax_line_pm.set_ylabel('pm index')

ax_dust.set_title('Dust count')
ax_pm.set_title('pm index')
ax_line_dust.set_title('Dust count')
ax_line_pm.set_title('pm index')

ax_dust.set_xticks(ind_dust)

ax_pm.set_xticks(ind_pm)
ax_line_dust.set_xticks([x[0], x[500], x[-1]])
ax_line_pm.set_xticks([x[0], x[500], x[-1]])

ax_dust.set_xticklabels(dust_label)
ax_pm.set_xticklabels(pm_label)
ax_line_dust.set_xticklabels([hist_time[0], hist_time[500], hist_time[-1]])
ax_line_pm.set_xticklabels([hist_time[0], hist_time[500], hist_time[-1]])


texts = {}


def autolabel(rects, ax):
    """
    Attach a text label above each bar displaying its height
    """
    for r in rects:
        for rect in r:
            height = rect.get_height()
            text_x = rect.get_x() + rect.get_width() / 2.
            text_y = 1.05 * height

            if rect not in texts:
                text = ax.text(text_x, text_y, '%d' %
                               int(height), ha='center', va='bottom')

                texts[rect] = text
            else:
                texts[rect].set_x(text_x)
                texts[rect].set_y(text_y)
                texts[rect].set_text('%d' % int(height))


autolabel(rects_dust, ax_dust)
autolabel(rects_pm, ax_pm)


def animate(i):
    global dust_max
    global pm_max

    print("\r%s" % i, end='')
    sys.stdout.flush()
    get_data()

    dust_max = max(dust_max, max([max(vs[-5:-1])
                                  for k, vs in hist_dust_value.items()]))
    pm_max = max(pm_max,  max([max(vs[-5:-1])
                               for k, vs in hist_pm_value.items()]))

    artists = []
    for i, dust in enumerate(dust_label):
        lines_dust[i][0].set_ydata(hist_dust_value[dust])
        artists.append(lines_dust[i][0])

    for i, pm in enumerate(pm_label):
        lines_pm[i][0].set_ydata(hist_pm_value[pm])
        artists.append(lines_pm[i][0])

    ax_line_dust.set_xticklabels([hist_time[0], hist_time[500], hist_time[-1]])
    ax_line_pm.set_xticklabels([hist_time[0], hist_time[500], hist_time[-1]])

    for i, dust in enumerate(dust_label):
        rects_dust[i][0].set_height(dust_value[i])
        artists.append(rects_dust[i][0])

    for i, pm in enumerate(pm_label):
        rects_pm[i][0].set_height(pm_value[i])
        artists.append(rects_pm[i][0])

    autolabel(rects_dust, ax_dust)
    autolabel(rects_pm, ax_pm)

    ax_line_dust.set_ylim([0, 11 * math.ceil(dust_max / 10.0)])
    ax_line_pm.set_ylim([0, 11 * math.ceil(pm_max / 10.0)])
    ax_dust.set_ylim([0, 11 * math.ceil(max(dust_value) / 10.0)])
    ax_pm.set_ylim([0, 11 * math.ceil(max(pm_value) / 10.0)])

    return artists


def init():
    pass


ani = animation.FuncAnimation(fig, animate, interval=1000)

fig.set_label('aqir')
plt.show()

"""
Animation of the cumulative relative frequency of heads
in successive tosses of a fair coin.

Author:
    Anderson Ribeiro

Description:
    This animation illustrates the convergence of the cumulative
    relative frequency of heads to its expected value (1/2), as
    predicted by the Law of Large Numbers.

Repository:
    https://github.com/...

License:
    MIT
"""


import numpy as np
import random
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import PercentFormatter
import matplotlib.animation as animation
from matplotlib.widgets import Button


# user-selectable parameter
n_tosses = 1000                 # number of coin tosses - user's free choice


# parameters of simulation
FRAME_INTERVAL = 10             # animation frame interval (ms).
X_SIGMA = round(n_tosses / 3)   # position of sigmas annotate
X_MEAN = round(n_tosses / 6)    # position of mean annotate


# number of tosses
tosses = np.arange(1, n_tosses + 1)


def maximize_window():
    """Resize the Matplotlib window to nearly fill the screen."""

    manager = plt.get_current_fig_manager()
    manager.window.update_idletasks()
    screen_width = manager.window.winfo_screenwidth()
    screen_height = manager.window.winfo_screenheight()
    manager.window.geometry(f"{screen_width - 20}x{screen_height - 80}+0+0")


def simulate_relative_frequency(n_tosses):
    """Simulate successive coin tosses and return the cumulative relative frequency of heads."""

    count_heads = 0
    relative_frequency = []

    for i in range(n_tosses):

        if random.randint(0, 1) == 1:
            count_heads += 1
        current_frequency = count_heads / (i + 1)
        relative_frequency.append(current_frequency)

    return relative_frequency


relative_frequency = simulate_relative_frequency(n_tosses)

# theoretical ±1sigma bands for the relative frequency
upper_band_1sigma = 1 / 2 + 1 / (2 * np.sqrt(tosses))
lower_band_1sigma = 1 / 2 - 1 / (2 * np.sqrt(tosses))


# formatting
fig = plt.figure()
axs = fig.subplot_mosaic([["graphic", "deviation"]], width_ratios = [4.8, 2.2])
fig.subplots_adjust(
    left = 0.06,
    right = 0.96,
    wspace = 0.13
)

# formatting of the frequency graph
axs["graphic"].set_title(f'Relative frequency', font = "Latin Modern Roman", fontsize = 22, fontweight ='bold', color = "#282525")
axs["graphic"].plot([0, n_tosses], [0.5, 0.5], linewidth = '2.0', color = 'red')

frequency_curve, = axs["graphic"].plot([], [], linewidth = '2.0', color = 'blue')

upper_1sigma, = axs["graphic"].plot([], [], linewidth = '2.0', color = 'green', linestyle = '--')
lower_1sigma, = axs["graphic"].plot([], [], linewidth = '2.0', color = 'green',linestyle = '--')

toss_label = axs["graphic"].text(0.83, 0.55, " ", font = "Latin Modern Roman", fontsize = '18', fontweight = 'bold', transform = axs["graphic"].transAxes, color = '#000000')

note_upper_1sigma = axs["graphic"].annotate(r"$1/2$" r"$+\sigma(f)$", (X_SIGMA, upper_band_1sigma[X_SIGMA]), (X_SIGMA*1.15, upper_band_1sigma[X_SIGMA]+0.1), font =  "Latin Modern Roman", ha="center", size = "18", arrowprops=dict(arrowstyle = "->", color ="green", lw = "1.5"))
note_upper_1sigma.set_visible(False)

note_lower_1sigma = axs["graphic"].annotate("$1/2$" r"$-\sigma(f)$", (X_SIGMA, lower_band_1sigma[X_SIGMA]), (X_SIGMA*1.15, lower_band_1sigma[X_SIGMA]-0.1), font =  "Latin Modern Roman", ha="center", size = "18", arrowprops=dict(arrowstyle = "->", color ="green"))
note_lower_1sigma.set_visible(False)

note_mean = axs["graphic"].annotate(r"$E(f) = 1/2$", (X_MEAN, 0.5), (X_MEAN * 1.15, 0.6), font =  "Latin Modern Roman", ha="center", size = "18", arrowprops=dict(arrowstyle = "->", color ="red", lw = "1.5"))
note_mean.set_visible(False)

# formatting the x-axis of the frequency graph
axs["graphic"].set_xlim(1, n_tosses)
axs["graphic"].xaxis.set_major_locator(MultipleLocator(n_tosses/10))
axs["graphic"].xaxis.set_minor_locator(MultipleLocator(n_tosses/20))
axs["graphic"].tick_params(axis = 'x',
               which = 'major',
               direction = 'out',
               length = 5,
               width = 0.5,
               labelsize = 18,
               labelfontfamily = "Latin Modern Roman")
axs["graphic"].tick_params(axis ='x',
               which = 'minor',
               direction = 'out',
               length = 3,
               width = 0.5)

# formatting the y-axis of the frequency graph
axs["graphic"].yaxis.set_major_formatter(PercentFormatter(xmax=1))
axs["graphic"].set_ylim(0, 1)
axs["graphic"].yaxis.set_major_locator(MultipleLocator(0.1))
axs["graphic"].yaxis.set_minor_locator(MultipleLocator(0.05))
axs["graphic"].tick_params(axis = 'y',
               which = 'major',
               direction = 'out',
               length = 5,
               width = 0.5,
               labelsize = 18,
               labelfontfamily = "Latin Modern Roman")
axs["graphic"].tick_params(axis = 'y',
               which = 'minor',
               direction = 'out',
               length = 3,
               width = 0.5)


# Formatting the standard deviations
axs["deviation"].set_title(f'Standard deviations', font = "Latin Modern Roman", fontsize = '22', fontweight = 'bold', color = "#282525")

deviation_curve, = axs["deviation"].plot([], [], label = r'$\sigma(S_n) = \sqrt{n}$', linewidth = '2.0', linestyle = '--', color = "#C41111")


deviation_curve_label = axs["deviation"].text(0.59, 0.70, " ", font = "Latin Modern Roman", fontsize = '18', fontweight = 'bold', transform = axs["deviation"].transAxes, color = '#000000')

deviation_n_heads, = axs["deviation"].plot([], [], label = r'$\sigma(N_{caras}) = \sqrt{n}/2$', linewidth = '2.0', linestyle = '-.', color = "#7DE13F")

deviation_n_heads_label = axs["deviation"].text(0.52, 0.48, " ", font = "Latin Modern Roman", fontsize = '18', fontweight = 'bold', transform = axs["deviation"].transAxes, color = '#000000')

axs["deviation"].legend(handlelength = 4 , loc = "lower right", fontsize = '16')

# formatting the x-axis of the standard deviations
axs["deviation"].set_xlim(1, n_tosses)
axs["deviation"].xaxis.set_major_locator(MultipleLocator(n_tosses/5))
axs["deviation"].xaxis.set_minor_locator(MultipleLocator(n_tosses/10))
axs["deviation"].tick_params(axis = 'x',
               which = 'major',
               direction = 'out',
               length = 5,
               width = 0.5,
               labelsize = 18,
               labelfontfamily = "Latin Modern Roman")
axs["deviation"].tick_params(axis = 'x',
               which = 'minor',
               direction = 'out',
               length = 3,
               width = 0.5)

# formatting the y-axis of the standard deviations
axs["deviation"].set_ylim(1, math.sqrt(n_tosses))
axs["deviation"].yaxis.set_major_locator(MultipleLocator(5))
axs["deviation"].yaxis.set_minor_locator(MultipleLocator(2.5))
axs["deviation"].tick_params(axis = 'y',
               which = 'major',
               direction = 'out',
               length = 5,
               width = 0.5,
               labelsize = 16,
               labelfontfamily = "Latin Modern Roman")
axs["deviation"].tick_params(axis = 'y',
               which = 'minor',
               direction = 'out',
               length = 3,
               width = 0.5)


# creates the button to control pausing and resuming the animation
ax_start = plt.axes([0.53, 0.15, 0.08, 0.05])
button_start = Button(ax_start, "Start")
button_start.label.set_font("Latin Modern Roman")
button_start.label.set_fontweight('bold')
button_start.label.set_fontsize(14)


animation_started = False

def start(event):
    """Start the animation after the Start button is pressed."""

    global anim
    global animation_started

    if not animation_started:
        anim = animation.FuncAnimation(fig, animate, frames = n_tosses, interval = FRAME_INTERVAL , blit = True, repeat = False)
        animation_started = True
        ax_start.set_visible(False)


def animate(i):
    """Update all artists for animation frame i."""

    current_tosses = tosses[:i+1]
    frequency_curve.set_data(current_tosses, relative_frequency[:i+1])           # update the curve with the data available up to the current frame
    toss_label.set_text(f"n = {i+1}")
    upper_1sigma.set_data(current_tosses, upper_band_1sigma[:i+1])
    lower_1sigma.set_data(current_tosses, lower_band_1sigma[:i+1])
    deviation_curve.set_data(current_tosses, np.sqrt(current_tosses))
    deviation_curve_label.set_text(r"$\sigma(S_n)$" f" = {math.sqrt(tosses[i]):.2f}")
    deviation_n_heads.set_data(current_tosses, np.sqrt(current_tosses) / 2)
    deviation_n_heads_label.set_text(r"$\sigma(N_{caras})$" f" = {math.sqrt(tosses[i]) / 2:.2f}")


    if i == n_tosses - 1:
         note_upper_1sigma.set_visible(True)
         note_lower_1sigma.set_visible(True)
         note_mean.set_visible(True)

    return (
            frequency_curve,
            toss_label,
            upper_1sigma,
            lower_1sigma,
            deviation_curve,
            deviation_curve_label,
            deviation_n_heads,
            deviation_n_heads_label,
            note_upper_1sigma,
            note_lower_1sigma,
            note_mean,
            )


button_start.on_clicked(start)
maximize_window()


plt.show()

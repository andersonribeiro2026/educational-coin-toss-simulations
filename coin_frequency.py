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


# simulation parameters
n_tosses = 1000                 # number of coins tosses
FRAME_INTERVAL = 10             # animation frame interval (ms).


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

# calculation of the sum frequency deviation
upper_band_1sigma = 1 / 2 + 1 / (2 * np.sqrt(tosses))
lower_band_1sigma = 1 / 2 - 1 / (2 * np.sqrt(tosses))


# plots
fig = plt.figure()
axs = fig.subplot_mosaic([["graphic", "deviation"]], width_ratios = [5, 2])
fig.subplots_adjust(
    left = 0.06,
    right = 0.96,
    wspace = 0.13
)

# formatting of the frequency graph
axs["graphic"].set_title(f'Relative\n frequency', font = "Latin Modern Roman", fontsize = 22, fontweight ='bold', color = "#282525")
axs["graphic"].plot([0, n_tosses], [0.5, 0.5], linewidth = '2.0', color = 'red')

frequency_curve, = axs["graphic"].plot([], [], linewidth = '2.0', color = 'blue')

upper_1sigma, = axs["graphic"].plot([], [], linewidth = '2.0', color = 'green', linestyle = '--')
lower_1sigma, = axs["graphic"].plot([], [], linewidth = '2.0', color = 'green',linestyle = '--')

toss_label = axs["graphic"].text(0.83, 0.55, " ", font = "Latin Modern Roman", fontsize = '18', fontweight = 'bold', transform = axs["graphic"].transAxes, color = '#000000')

note_sigma_plus1 = axs["graphic"].annotate(r"$1/2$" r"$+\sigma(f)$", (round(n_tosses/3), upper_band_1sigma[round(n_tosses/3)]), (round(n_tosses/3)*1.15, upper_band_1sigma[round(n_tosses/3)]+0.1), font =  "Latin Modern Roman", ha="center", size = "18", arrowprops=dict(arrowstyle = "->", color ="green", lw = "1.5"))
note_sigma_plus1.set_visible(False)

note_sigma_plus2 = axs["graphic"].annotate("$1/2$" r"$-\sigma(f)$", (round(n_tosses/3), lower_band_1sigma[round(n_tosses/3)]), (round(n_tosses/3)*1.15, lower_band_1sigma[round(n_tosses/3)]-0.1), font =  "Latin Modern Roman", ha="center", size = "18", arrowprops=dict(arrowstyle = "->", color ="green"))
note_sigma_plus2.set_visible(False)

note_mean = axs["graphic"].annotate(r"$E(f) = 1/2$", (round(n_tosses/6), 0.5), (round(n_tosses/6)*1.15, 0.6), font =  "Latin Modern Roman", ha="center", size = "18", arrowprops=dict(arrowstyle = "->", color ="red", lw = "1.5"))
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


# Formatting the standard deviation of the sum graph
axs["deviation"].set_title(f'Standard deviation\n of the sum', font = "Latin Modern Roman", fontsize = '22', fontweight = 'bold', color = "#282525")
deviation_curve, = axs["deviation"].plot([], [], linewidth = '2.0', color = 'red')
deviation_label = axs["deviation"].text(0.50, 0.55, " ", font = "Latin Modern Roman", fontsize = '18', fontweight = 'bold', transform = axs["deviation"].transAxes, color = '#000000')

# formatting the x-axis of the standard deviation of the sum graph
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

# formatting the y-axis of the standard deviation of the sum graph
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
ax_start = plt.axes([0.55, 0.15, 0.08, 0.05])
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
        anim = animation.FuncAnimation(fig, animate, frames = n_tosses, interval = FRAME_INTERVAL, blit = True, repeat = False)
        animation_started = True
        ax_start.set_visible(False)


def animate(i):
    """Update all artists for animation frame i."""

    current_tosses = tosses[:i+1]
    frequency_curve.set_data(current_tosses, relative_frequency[:i+1])           # draws only a segment of two points
    toss_label.set_text(f"n = {i+1}")
    upper_1sigma.set_data(current_tosses, upper_band_1sigma[:i+1])
    lower_1sigma.set_data(current_tosses, lower_band_1sigma[:i+1])
    deviation_curve.set_data(current_tosses, np.sqrt(current_tosses))
    deviation_label.set_text(r"$\sigma(S_n)$" f" = {math.sqrt(tosses[i]):.2f}")

    if i == n_tosses - 1:
         note_sigma_plus1.set_visible(True)
         note_sigma_plus2.set_visible(True)
         note_mean.set_visible(True)

    return (
            frequency_curve,
            toss_label,
            upper_1sigma,
            lower_1sigma,
            deviation_curve,
            deviation_label,
            note_sigma_plus1,
            note_sigma_plus2,
            note_mean,
            )


button_start.on_clicked(start)
maximize_window()

plt.show()

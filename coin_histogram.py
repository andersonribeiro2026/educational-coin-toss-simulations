"""
Animation of the histogram of relative frequencies of heads obtained from successive sequences of fair-coin tosses.

Author:
    Anderson Ribeiro

Description:
    This animation illustrates the distribution of the relative frequency of heads over repeated sequences of fair-coin
    tosses and its convergence toward the normal approximation predicted by the Central Limit Theorem.

Repository:
    https://github.com/...

License:
    MIT
"""


import functools
import random
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.widgets import Button

import numpy as np

import matplotlib.animation as animation

# simulation parameters
n_tosses = 100                   # number of coin tosses
n_sequences = 100                # number of coin-toss sequences
FRAME_INTERVAL = 20              # animation frame interval (ms).


def simulate_relative_frequency(n_tosses, n_sequences):
    """Simulate repeated sequences of coin tosses and return the relative frequency of heads for each sequence."""

    relative_frequency = []

    for _ in range(n_sequences):

        count_heads = 0

        for _ in range(n_tosses):

            if random.randint(0, 1) == 1:
                count_heads += 1

        current_relative_frequency = count_heads / n_tosses
        relative_frequency.append(current_relative_frequency)

    return relative_frequency


def normal_distribution(x_coord, sigma, scale_factor):
    """Calculate the theoretical normal approximation."""

    max_amplitude = scale_factor / (sigma * math.sqrt(2 * math.pi))
    normal = max_amplitude * np.exp(-( ((x_coord - 0.5) / sigma)**2) / 2)

    return normal, max_amplitude


def maximize_window():
    """Resize the Matplotlib window to nearly fill the screen."""

    manager = plt.get_current_fig_manager()
    manager.window.update_idletasks()
    screen_width = manager.window.winfo_screenwidth()
    screen_height = manager.window.winfo_screenheight()
    manager.window.geometry(f"{screen_width-20}x{screen_height-80}+0+0")

# calculation of relative frequencies and histogram
relative_frequency = simulate_relative_frequency(n_tosses, n_sequences)

# Adapt the number of histogram bins for low values of n_tosses
# to avoid excessive empty bins caused by the discrete nature of
# the relative frequency.
if n_tosses <= 20:
    lim_bins = 10
elif n_tosses <= 50:
    lim_bins = 20
else:
    lim_bins = 50

hist_bins = np.linspace(0, 1, lim_bins)
histogram, _ = np.histogram(relative_frequency, hist_bins)


# normal approximation
x_coord = np.arange(0, 1, 0.001)
delta_x = hist_bins[1] - hist_bins[0]
scale_factor = n_sequences * delta_x
sigma = 1 / (2 * math.sqrt(n_tosses))
normal, max_amplitude = normal_distribution(x_coord, sigma, scale_factor)
y_lim_max = round(1.3 * max(histogram.max(), max_amplitude))


# animation parameters
histogram_aux, _ = np.histogram([], hist_bins)

def animate(count_frames, bar_container):

    global animation_running

    if not animation_running:
        return (
            bar_container.patches,
            sequences,
            normal_curve,
            axis_symmetry,
            normal_label
        )

    if count_frames < n_sequences:

        index = np.digitize(relative_frequency[count_frames], hist_bins, right=True)
        histogram_aux[index-1] += 1
        for count, rect in zip(histogram_aux, bar_container.patches):
            rect.set_height(count)
        sequences.set_text(f"{count_frames+1} sequences of {n_tosses} tosses")
        #sigma_label.set_text(r"$\sigma(f)$" f" = {1/(2*math.sqrt(n_tosses)):.3f}")
        count_frames += 1

    if count_frames == n_sequences:
        normal_curve.set_data(x_coord, normal)
        axis_symmetry.set_data([0.5, 0.5], [0, max(normal)])
        normal_label.set_visible(True)

        ani.event_source.stop()

    return (
            bar_container.patches,
            sequences,
            normal_curve,
            axis_symmetry,
            normal_label
            )


i53 = np.argmin(np.abs(x_coord - 0.53))                 # position to normal_label

# plots
fig, ax = plt.subplots()

# formatting of the frequency graph
ax.set_title("Histogram of relative frequencies", font = "Latin Modern Roman", fontsize = 22, fontweight = 'bold', color = "#282525")

normal_curve, = ax.plot([], [], linewidth = '2.0', color = "red")
#ax.plot([0.5, 0.5], [0, y_lim_max], color = "blue", lw = '2', ls = '--')

# axis of symmetry
axis_symmetry, = ax.plot([], [], color = "red", lw = '1.5', ls = '-.')

sequences = ax.text(0.70, 0.9, " ", font = "Latin Modern Roman", fontsize = '18', fontweight = 'bold', transform = ax.transAxes, color = '#000000')

# normal distribution notation
normal_label = ax.annotate(f"     Normal\n   approximation\n" r"   $\sigma(f)$" f" = {1/(2*math.sqrt(n_tosses)):.3f}", (0.55, normal[i53]), (0.7, normal[i53]), font = "Latin Modern Roman", color = "#9E1919", ha="center", size = "18", fontweight = 'bold', arrowprops=dict(arrowstyle = "->", color ="red", lw = "1.5", relpos=(0.3, 0.5)))
normal_label.set_visible(False)

# formatting the x-axis
ax.set_xlim(0, 1)
ax.set_xlabel('Relative Frequencies', fontsize = '20', font = "Latin Modern Roman")
ax.xaxis.set_major_locator(MultipleLocator(0.1))
ax.xaxis.set_minor_locator(MultipleLocator(0.05))
ax.tick_params(axis = 'x',
               which ='major',
               direction='out',
               length=5,
               width=0.5,
               labelsize=16,
               labelfontfamily = "Latin Modern Roman")
ax.tick_params(axis='x',
               which='minor',
               direction='out',
               length=3,
               width=0.5)

# formatting the y-axis
ax.set_ylim(0, y_lim_max)
#ax.set_ylabel('Counts', fontsize = '20', font = "Latin Modern Roman")
ax.yaxis.set_major_locator(MultipleLocator(y_lim_max/10))
ax.yaxis.set_minor_locator(MultipleLocator(y_lim_max/20))
ax.tick_params(axis='y',
               which='major',
               direction='out',
               length=5,
               width=0.5,
               labelsize=16,
               labelfontfamily = "Latin Modern Roman")
ax.tick_params(axis='y',
               which='minor',
               direction='out',
               length=3,
               width=0.5)


# creates the button to control pausing and resuming the animation
ax_start = plt.axes([0.795, 0.15, 0.08, 0.05])
button_start = Button(ax_start, "Start")
button_start.label.set_font("Latin Modern Roman")
button_start.label.set_fontweight('bold')
button_start.label.set_fontsize(14)

animation_running = False

def start(event):
    """Start the animation after the Start button is pressed."""

    global animation_running

    if not animation_running:

        animation_running = True
        ax_start.set_visible(False)


_, _, bar_container = ax.hist([], hist_bins, lw=1, ec="white", fc="#7982E4", alpha=0.5)
anim = functools.partial(animate, bar_container=bar_container)
ani = animation.FuncAnimation(fig, anim, frames = n_sequences, interval=FRAME_INTERVAL, repeat=False, blit=False, cache_frame_data=False)

button_start.on_clicked(start)
maximize_window()

plt.show()

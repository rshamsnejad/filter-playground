from re import I
from tokenize import group
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

def remove_phase_discontinuities(phase: list) -> list:
    """
    In a wrapped phase array, replaces the two points before and after
    each wrap with NaN. This is useful to prevent matplotlib from plotting
    vertical lines at the wrap locations

    Args:
        phase (list): phase points list

    Returns:
        list: input list with NaN before and after each wrap
    """

    # Get sign of each point
    # Negative  gives -1
    # Positive  gives 1
    # Zero      gives 0
    signs = np.sign(phase)

    # Split the list in adjacent pairs
    pairs = []
    for i in range(len(signs) - 1):
        pairs.append( (signs[i], signs[i + 1]) )

    # A pair of (-1, 1) indicates a wrap: find out the indexes of such pairs
    pairs_indexes = [index for index, element in enumerate(pairs) if element == (-1, 1) or element == (1, -1)]

    # Replace all points before the wraps with NaN
    phase_nan = phase.copy()
    phase_nan[pairs_indexes] = np.nan

    return phase_nan


pivot_frequency = 500

# b0 = pivot_frequency ** 2
# # b1 = 1 / (Fp)
# b1 = 0
# b2 = 1

# b = [b2, b1, b0]

# a0 = pivot_frequency ** 2
# a1 = 1/0.001#1 / (Fp)
# a2 = 1

# a = [a2, a1, a0]

alpha = 0.8

p_1   = np.array(range(1, 10, 9))
z_1   = p_1        + alpha
p_10  = p_1 * 10
z_10  = p_1 * 10   + alpha * 10
p_100 = p_1 * 100
z_100 = p_1 * 100  + alpha * 100
p_1k  = p_1 * 1e3
z_1k  = p_1 * 1e3  + alpha * 1e3
p_10k = p_1 * 10e3
z_10k = p_1 * 10e3 + alpha * 10e3

p = list(p_1) + list(p_10) + list(p_100) + list(p_1k) + list(p_10k)
z = list(z_1) + list(z_10) + list(z_100) + list(z_1k) + list(z_10k)

k = 1

b, a = signal.zpk2tf(z, p, k)

print(f"len(b) = {len(b)}")

#################################################################################################################

frequency_points = np.logspace(0, 5, 1000)
frequencies, magnitude = signal.freqs(b, a, worN=frequency_points)

mag_db = 20 * np.log10(abs(magnitude))
phase_deg = np.angle(magnitude, deg=True)
phase_deg_nan = remove_phase_discontinuities(phase_deg)

group_delay = -np.diff(np.unwrap(np.angle(magnitude))) / np.diff(2 * np.pi * frequencies)
group_delay_ms = group_delay * 1000

# plot_freq_range     = [20, 20e3]
plot_freq_range     = [0, 100e3]
plot_mag_range      = [-10, 10]
plot_phase_range    = [-200, 200]

fig, axs = plt.subplots(2, 1, sharex=False)
fig.suptitle(f"Tilt filter, order {len(a)}")

slope = 20

# y = mag_db
# y = abs(magnitude)
mag_log = slope * np.log10(frequencies / pivot_frequency)

# Magnitude
axs[0].semilogx(frequencies, mag_db)
# axs[0].set_xscale('log')
axs[0].set_xlim(plot_freq_range)
axs[0].set_ylabel('Gain [dB]')
# axs[0].set_ylim(plot_mag_range)
# axs[0].margins(0, 0.1)
axs[0].grid(which='both', axis='both')
# axs[0].axvline(pivot_frequency, color='red', linestyle='--')

# Phase
phase_plot = axs[1].semilogx(frequencies, phase_deg_nan)
# axs[1].set_xscale('log')
axs[1].set_xlabel('Frequency [Hz]')
axs[1].set_xlim(plot_freq_range)
axs[1].set_ylabel('Phase [°]')
axs[1].set_ylim(plot_phase_range)
axs[1].margins(0, 0.1)
axs[1].grid(which='both', axis='both')
# axs[1].axvline(f0, color='red', linestyle='--')
axs[1].tick_params(axis='y', colors='C0')
axs[1].yaxis.label.set_color('C0')

plt.show()

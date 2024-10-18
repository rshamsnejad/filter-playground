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


Fp = 1e3

b0 = 0
b1 = 1 / (Fp)
b2 = 0

b = [b2, b1, b0]

a0 = 1
a1 = 0#1 / (Fp)
a2 = 0

a = [a2, a1, a0]

#################################################################################################################

frequency_points = np.logspace(0, 5, 1000)
frequencies, magnitude = signal.freqs(b, a, worN=frequency_points)

mag_db = 20 * np.log10(abs(magnitude))
phase_deg = np.angle(magnitude, deg=True)
phase_deg_nan = remove_phase_discontinuities(phase_deg)

group_delay = -np.diff(np.unwrap(np.angle(magnitude))) / np.diff(2 * np.pi * frequencies)
group_delay_ms = group_delay * 1000

plot_freq_range     = [20, 20e3]
plot_mag_range      = [-30, 30]
plot_phase_range    = [-200, 200]

fig, axs = plt.subplots(2, 1, sharex=False)
fig.suptitle(f"Tilt filter")

y = mag_db
# y = abs(magnitude)
y = -20 * np.log10(frequencies / 1000)

# Magnitude
axs[0].plot(frequencies, y)
# axs[0].semilogx(frequencies, mag_db)
# axs[0].set_xscale('log')
axs[0].set_xlim(plot_freq_range)
axs[0].set_ylabel('Gain [dB]')
axs[0].set_ylim(plot_mag_range)
axs[0].margins(0, 0.1)
axs[0].grid(which='both', axis='both')
# axs[0].axvline(f0, color='red', linestyle='--')

axs[1].semilogx(frequencies, y)
axs[1].set_xscale('log')
axs[1].set_xlim(plot_freq_range)
axs[1].set_ylabel('Gain [dB]')
axs[1].set_ylim(plot_mag_range)
axs[1].margins(0, 0.1)
axs[1].grid(which='both', axis='both')

'''
# Phase
phase_plot = axs[1].plot(frequencies, phase_deg_nan)
# phase_plot = axs[1].semilogx(frequencies, phase_deg_nan)
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
'''

plt.show()

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


alpha = 0.5

pole_multiplier = 2
pole_spacing = np.log(pole_multiplier)
zero_spacing = -alpha * pole_spacing

poles = [9]

N = 13

for i in range(1, N):
    poles.append(poles[0] * pole_multiplier ** i)
# i = 1
# while True:
#     pole = poles[0] * pole_multiplier ** i
#     if pole >= 22050:
#     # if pole >= 96000:
#         break
#     else:
#         poles.append(pole)
#         i += 1

zeros = np.array(poles) * pole_multiplier ** (-alpha)

gain = 1

#################################################################################################################

frequency_points = np.logspace(-1, 6, 1000)
# frequencies, magnitude = signal.freqs(b, a, worN=frequency_points)
frequencies, magnitude = signal.freqs_zpk(zeros, poles, gain, worN=frequency_points)

mag_db = 20 * np.log10(abs(magnitude))
phase_deg = np.angle(magnitude, deg=True)
phase_deg_nan = remove_phase_discontinuities(phase_deg)

group_delay = -np.diff(np.unwrap(np.angle(magnitude))) / np.diff(2 * np.pi * frequencies)
group_delay_ms = group_delay * 1000

# plot_freq_range     = [20, 20e3]
plot_freq_range     = [0.1, 10e6]
plot_mag_range      = [-1, 1]
plot_phase_range    = [-200, 200]

fig, axs = plt.subplots(2, 1, sharex=False)
fig.suptitle(f"Analog tilt filter, order {len(poles)}")

# Magnitude
axs[0].semilogx(frequencies, mag_db)
# axs[0].set_xscale('log')
axs[0].set_xlim(plot_freq_range)
axs[0].set_ylabel('Gain [dB]')
# axs[0].set_ylim(plot_mag_range)
# axs[0].margins(0, 0.1)
axs[0].grid(which='both', axis='both')
axs[0].axvline(20, color='red', linestyle='--')
axs[0].axvline(20e3, color='red', linestyle='--')


import matplotlib.transforms as transforms
# Blended transformation to get X in data coordinates and Y in axes coordinates
trans = transforms.blended_transform_factory(axs[0].transData, axs[0].transAxes)

axs[0].plot(zeros, [0]*len(zeros), '.c', transform=trans, clip_on=False)
axs[0].plot(poles, [0]*len(poles), 'xr', transform=trans, clip_on=False)

# Phase
phase_plot = axs[1].semilogx(frequencies, phase_deg_nan)
# axs[1].set_xscale('log')
axs[1].set_xlabel('Frequency [Hz]')
axs[1].set_xlim(plot_freq_range)
axs[1].set_ylabel('Phase [°]')
axs[1].set_ylim(plot_phase_range)
axs[1].margins(0, 0.1)
axs[1].grid(which='both', axis='both')
axs[1].axvline(20, color='red', linestyle='--')
axs[1].axvline(20e3, color='red', linestyle='--')
axs[1].tick_params(axis='y', colors='C0')
axs[1].yaxis.label.set_color('C0')

plt.show()

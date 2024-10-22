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

fs = 192000
ts = 1/fs
alpha = 0

poles = np.logspace(0, 5, 10)

p_c = [pole for pole in poles if pole < fs/2]
p_d = p_c.copy()

for i in range(1, len(p_d)):
    p_d[i] = p_c[0] * ( np.tan(np.pi * p_d[i] * ts) ) / ( np.tan(np.pi * p_c[0] * ts) )

z = []
for i in range(len(p_d) - 1):
    z.append(np.sqrt(p_d[i] * p_d[i+1]))

k = 1
p = p_d

#################################################################################################################

frequency_points = np.logspace(0, 5, 1000)
# frequencies, magnitude = signal.freqs(b, a, worN=frequency_points)
frequencies, magnitude = signal.freqz_zpk(z, p, k, worN=frequency_points, fs=fs)

mag_db = 20 * np.log10(abs(magnitude))
phase_deg = np.angle(magnitude, deg=True)
phase_deg_nan = remove_phase_discontinuities(phase_deg)

group_delay = -np.diff(np.unwrap(np.angle(magnitude))) / np.diff(2 * np.pi * frequencies)
group_delay_ms = group_delay * 1000

plot_freq_range     = [20, 20e3]
# plot_freq_range     = [0, 100e3]
plot_mag_range      = [-1, 1]
plot_phase_range    = [-200, 200]

fig, axs = plt.subplots(2, 1, sharex=False)
fig.suptitle(f"Tilt filter, order {len(p)}")

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

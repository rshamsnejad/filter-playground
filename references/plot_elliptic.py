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

N = 4
f0 = 1000
fs = 48000

sos = signal.ellip(N, 0.5, 30, f0, 'high', analog=False, fs=fs, output='sos')
frequencies, magnitude = signal.sosfreqz(sos, worN=np.logspace(0, 5, 1000), fs=fs)

mag_db = 20 * np.log10(abs(magnitude))
phase_deg = np.angle(magnitude, deg=True)
phase_deg_nan = remove_phase_discontinuities(phase_deg)

plot_freq_range     = [20, 20e3]
plot_mag_range      = [-40, 10]
plot_phase_range    = [-200, 200]

fig, axs = plt.subplots(2, 1, sharex=True)
fig.suptitle(f"Butterworth highpass filter, order {N}, $f_0 = {f0}$ Hz")

# Magnitude
axs[0].semilogx(frequencies, mag_db)
axs[0].set_xscale('log')
axs[0].set_xlim(plot_freq_range)
axs[0].set_ylabel('Gain [dB]')
axs[0].set_ylim(plot_mag_range)
axs[0].margins(0, 0.1)
axs[0].grid(which='both', axis='both')
axs[0].axvline(f0, color='red')

# Phase
axs[1].semilogx(frequencies, phase_deg_nan)
axs[1].set_xlabel('Frequency [Hz]')
axs[1].set_xscale('log')
axs[1].set_xlim(plot_freq_range)
axs[1].set_ylabel('Phase [°]')
axs[1].set_ylim(plot_phase_range)
axs[1].margins(0, 0.1)
axs[1].grid(which='both', axis='both')
axs[1].axvline(f0, color='red')

plt.show()
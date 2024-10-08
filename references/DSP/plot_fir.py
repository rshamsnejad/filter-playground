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

f0 = 10000
fs = 48000
nyq = fs / 2
ft = f0 * 3 / 10
atten = 30
filtertype = "lowpass"

N, _ = signal.kaiserord(atten, ft/nyq)

if N % 2 == 0:
    N += 1

if filtertype == "highpass":
    bands = [0, f0 - ft, f0, nyq]
    gains = [0, 0, 1, 1]
else:
    bands = [0, f0, f0 + ft, nyq]
    gains = [1, 1, 0, 0]


taps = signal.firls(N, bands, gains, fs=fs)

sos = signal.tf2sos(taps, [1])

frequency_points = np.logspace(0, 5, 1000)

frequencies, magnitude = signal.sosfreqz(sos, worN=frequency_points, fs=fs)

mag_db = 20 * np.log10(abs(magnitude))
phase_deg = np.angle(magnitude, deg=True)
phase_deg_nan = remove_phase_discontinuities(phase_deg)

plot_freq_range     = [20, 20e3]
plot_mag_range      = [-100, 10]
plot_phase_range    = [-200, 200]

fig, axs = plt.subplots(2, 1, sharex=True)
fig.suptitle(f"FIR {filtertype} filter, {len(taps)} taps, $f_0 = {f0}$ Hz, $f_t = {ft}$ Hz")

# Magnitude
axs[0].semilogx(frequencies, mag_db)
# axs[0].plot(frequencies, mag_db)
axs[0].set_xscale('log')
axs[0].set_xlim(plot_freq_range)
axs[0].set_ylabel('Gain [dB]')
axs[0].set_ylim(plot_mag_range)
axs[0].margins(0, 0.1)
axs[0].grid(which='both', axis='both')
axs[0].axvline(f0, color='red')
axs[0].axvspan(fs / 2, frequency_points[-1], color='gray')
axs[0].text(
    (fs / 2) * 1.1,
    0,
    "Harry Nyquist\nis watching you",
    fontsize=12,
    fontweight='black',
    color='ivory',
    rotation='vertical',
    horizontalalignment='left',
    verticalalignment='center',
    clip_on=True
)

# Phase
axs[1].semilogx(frequencies, phase_deg)
# axs[1].plot(frequencies, phase_deg)
axs[1].set_xlabel('Frequency [Hz]')
axs[1].set_xscale('log')
axs[1].set_xlim(plot_freq_range)
axs[1].set_ylabel('Phase [°]')
axs[1].set_ylim(plot_phase_range)
axs[1].margins(0, 0.1)
axs[1].grid(which='both', axis='both')
axs[1].axvline(f0, color='red')
axs[1].axvspan(fs / 2, frequency_points[-1], color='gray')
axs[1].text(
    (fs / 2) * 1.1,
    0,
    "Harry Nyquist\nis watching you",
    fontsize=12,
    fontweight='black',
    color='ivory',
    rotation='vertical',
    horizontalalignment='center',
    verticalalignment='center',
    clip_on=True
)

plt.show()
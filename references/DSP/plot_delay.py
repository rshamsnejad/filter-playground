from tokenize import group
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

fs = 48000

impulse = signal.unit_impulse(300)
plt.plot(impulse, label='impulse')

sos_delay_1sample = [[0, 1, 0, 1, 0, 0]]
impulse_1sample_delayed = signal.sosfilt(sos_delay_1sample, impulse)
plt.plot(impulse_1sample_delayed, label='1-sample delay')

sos_delay_2samples = [[0, 0, 1, 1, 0, 0]]
impulse_2samples_delayed = signal.sosfilt(sos_delay_2samples, impulse)
plt.plot(impulse_2samples_delayed, label='2-sample delay')

delay_msec = 3

def msec_to_sample(msec: int) -> int:
    return int(msec * fs / 1000)

X_delay = msec_to_sample(delay_msec)
sos_delay_xsamples = list(sos_delay_1sample)

for i in range(X_delay - 1):
    sos_delay_xsamples.extend(sos_delay_1sample)

impulse_xsamples_delayed = signal.sosfilt(sos_delay_xsamples, impulse)
plt.plot(impulse_xsamples_delayed, label=f'{delay_msec} ms delay ({X_delay} samples at {int(fs/1000)} kHz)')

plt.legend(loc='best')
plt.show()

plot_freq_range     = [20, 20e3]
plot_mag_range      = [-40, 10]
plot_phase_range    = [-200, 200]

fig, axs = plt.subplots(2, 1, sharex=True)
fig.suptitle(f"Delays")

# Magnitude
axs[0].set_xscale('log')
axs[0].set_xlim(plot_freq_range)
axs[0].set_ylabel('Gain [dB]')
axs[0].set_ylim(plot_mag_range)
axs[0].margins(0, 0.1)
axs[0].grid(which='both', axis='both')

# Phase
axs[1].set_xlabel('Frequency [Hz]')
axs[1].set_xscale('log')
axs[1].set_xlim(plot_freq_range)
axs[1].set_ylabel('Phase [°]')
axs[1].set_ylim(plot_phase_range)
axs[1].margins(0, 0.1)
axs[1].grid(which='both', axis='both')
axs[1].tick_params(axis='y', colors='C0')
axs[1].yaxis.label.set_color('C0')


frequency_points = np.logspace(0, 5, 1000)

freq1, mag1 = signal.sosfreqz(sos_delay_1sample, worN=frequency_points, fs=fs)
mag1_db = 20 * np.log10(abs(mag1))
phase1_deg = np.angle(mag1, deg=True)
axs[0].semilogx(freq1, mag1_db)
axs[1].semilogx(freq1, phase1_deg, label='1-sample delay')

freq2, mag2 = signal.sosfreqz(sos_delay_2samples, worN=frequency_points, fs=fs)
mag2_db = 20 * np.log10(abs(mag1))
phase2_deg = np.angle(mag2, deg=True)
axs[0].semilogx(freq1, mag2_db)
axs[1].semilogx(freq1, phase2_deg, label='2-sample delay')

freqx, magx = signal.sosfreqz(sos_delay_xsamples, worN=frequency_points, fs=fs)
magx_db = 20 * np.log10(abs(magx))
phasex_deg = np.angle(magx, deg=True)
axs[0].semilogx(freqx, magx_db)
axs[1].semilogx(freqx, phasex_deg, label=f'{X_delay}-sample delay')



plt.legend(loc='best')
plt.show()
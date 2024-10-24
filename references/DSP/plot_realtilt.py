import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
from scipy import signal
import numpy as np

### Parameters
alpha = -0.5
N = 5
r = 2

### Poles, zeros and gain computation
pole_spacing = np.log(r)
zero_spacing = -alpha * pole_spacing

poles = [-1]

for i in range(1, N):
    poles.append( poles[0] * r ** i )

zeros = np.array(poles) * r ** (-alpha)

gain = 1

### Plot
frequencies, magnitude = signal.freqs_zpk(
    zeros, poles, gain,
    worN=np.logspace(-1, 3, 1000)
)

mag_db = 20 * np.log10(abs(magnitude))
phase_deg = np.angle(magnitude, deg=True)

plot_freq_range     = [0.1, 10e2]
plot_phase_range    = [-200, 200]

fig, axs = plt.subplots(2, 1, sharex=False)
fig.suptitle(f"Analog tilt filter, order {len(poles)}")

# Magnitude
axs[0].semilogx(frequencies, mag_db)
axs[0].set_xlim(plot_freq_range)
axs[0].set_ylabel('Gain [dB]')
axs[0].grid(which='both', axis='both')

# Poles and zeros
# Blended transformation to get X in data coordinates and Y in axes coordinates
trans = transforms.blended_transform_factory(axs[0].transData, axs[0].transAxes)
axs[0].plot(np.abs(zeros), [0]*len(zeros), 'oc', fillstyle='none', transform=trans, clip_on=False)
axs[0].plot(np.abs(poles), [0]*len(poles), 'xr', transform=trans, clip_on=False)

# Phase
phase_plot = axs[1].semilogx(frequencies, phase_deg)
axs[1].set_xlabel('Frequency [Hz]')
axs[1].set_xlim(plot_freq_range)
axs[1].set_ylabel('Phase [°]')
axs[1].set_ylim(plot_phase_range)
axs[1].grid(which='both', axis='both')

plt.show()

import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
from scipy import signal
import numpy as np


############################################################################################
#
# By Robin SHAMSNEJAD <rsham@free.fr>
# For my beloved EAEs
#
# Source: https://ccrma.stanford.edu/~jos/spectilt/spectilt.pdf
#
# Where I left off:
# * The filter's analog (s-plane) transfer function works perfectly
#   fine as can be seen on the left graph
# * However the digital (z-plane) transfer function warps when approaching
#   Nyquist as can be seen on the right graph
# * Warping is apparently an expected effect of the bilinear transform which
#   should be compensated by the "prewarping" method as described in the paper,
#   but for some reason it does not work
# * It can be worked around by increasing the sample rate, which is not ideal
#   because car radios likely only support 44100/48000 Hz
# * I'm pretty sure Fabfilter uses this method for their Pro-Q tilt filter,
#   either by oversampling or with some additional math magic to solve this warping thing
# * A potential magic formula can be found at the link below
#   https://ccrma.stanford.edu/~champ/files/DAFx20in21_paper_15.pdf
#
############################################################################################

### Parameters #############################################################################
# Sampling frequency
fs = 48000
# Number of poles and zeros
N = 10
# Slope
alpha = -0.2
# Bandwidth
fmin = 20
fmax = 20e3 # Try with fs / 2
############################################################################################

### Computation ############################################################################
r = (fmax / fmin) ** (1 / (N-1))
pole_spacing = np.log(r)
zero_spacing = -alpha * pole_spacing

# Analog poles, zeros and gain
a_poles = [-fmin]
for i in range(1, N):
    a_poles.append( a_poles[0] * r ** i )

a_zeros = np.array(a_poles) * (r ** (-alpha))

b, a = signal.zpk2tf(a_zeros, a_poles, 1)
a_gain = a[-1] / b[-1] # Gain scaling to get 0 dB at DC

# Digital poles, zeros and gain
a_prewarped_poles = np.array(
    a_poles[0] * np.tan( np.pi * np.array(a_poles) / fs ) / np.tan( np.pi * a_poles[0] / fs )
)
a_prewarped_zeros = np.array(a_prewarped_poles) * r ** (-alpha)

d_zeros, d_poles, d_gain = signal.bilinear_zpk(a_prewarped_zeros, a_prewarped_poles, a_gain, fs=fs)

# Cascaded biquads computation (SOS = Second-Order Sections)
sos = signal.zpk2sos(d_zeros, d_poles, d_gain)
############################################################################################

### Plot ###################################################################################
frequency_points = np.logspace(-1, 6, 1000)

a_frequencies, a_magnitude = signal.freqs_zpk(
    a_zeros, a_poles, a_gain,
    worN=frequency_points
)

a_mag_db = 20 * np.log10(abs(a_magnitude))
a_phase_deg = np.angle(a_magnitude, deg=True)

d_frequencies, d_magnitude = signal.sosfreqz(
    sos,
    worN=frequency_points,
    fs=fs
)

d_mag_db = 20 * np.log10(abs(d_magnitude))
d_phase_deg = np.angle(d_magnitude, deg=True)

plot_freq_range     = [0.1, 10e5]
plot_phase_range    = [-200, 200]

fig, axs = plt.subplots(2, 2, sharex=False)
fig.suptitle(f"Tilt filter, N={N}, $\\alpha$={alpha}, $F_s$={fs}")

# Analog magnitude
axs[0][0].set_title("Analog")
axs[0][0].semilogx(a_frequencies, a_mag_db)
axs[0][0].set_xlim(plot_freq_range)
axs[0][0].set_ylabel('Gain [dB]')
axs[0][0].grid(which='both', axis='both')
axs[0][0].axvline(20, color='green', linestyle='--')
axs[0][0].axvline(20e3, color='green', linestyle='--')
axs[0][0].axvline(fs / 2, color='red', linestyle='--')

# Axis markers for analog poles and zeros
# Blended transformation to get X in data coordinates and Y in axes coordinates
trans = transforms.blended_transform_factory(axs[0][0].transData, axs[0][0].transAxes)
axs[0][0].plot(np.abs(a_zeros), [0]*len(a_zeros), 'oc', fillstyle='none', transform=trans, clip_on=False)
axs[0][0].plot(np.abs(a_poles), [0]*len(a_poles), 'xr', transform=trans, clip_on=False)

# Analog phase
axs[1][0].semilogx(a_frequencies, a_phase_deg)
axs[1][0].set_xlabel('Frequency [Hz]')
axs[1][0].set_xlim(plot_freq_range)
axs[1][0].set_ylabel('Phase [°]')
axs[1][0].set_ylim(plot_phase_range)
axs[1][0].grid(which='both', axis='both')
axs[1][0].axvline(20, color='green', linestyle='--')
axs[1][0].axvline(20e3, color='green', linestyle='--')
axs[1][0].axvline(fs / 2, color='red', linestyle='--')

# Digital magnitude
axs[0][1].set_title(f"Digital ({len(sos)} biquads)")
axs[0][1].semilogx(d_frequencies, d_mag_db)
axs[0][1].set_xlim(plot_freq_range)
axs[0][1].grid(which='both', axis='both')
axs[0][1].axvline(20, color='green', linestyle='--')
axs[0][1].axvline(20e3, color='green', linestyle='--')
axs[0][1].axvline(fs / 2, color='red', linestyle='--')

# Digital phase
axs[1][1].semilogx(d_frequencies, d_phase_deg)
axs[1][1].set_xlabel('Frequency [Hz]')
axs[1][1].set_xlim(plot_freq_range)
axs[1][1].set_ylim(plot_phase_range)
axs[1][1].grid(which='both', axis='both')
axs[1][1].axvline(20, color='green', linestyle='--')
axs[1][1].axvline(20e3, color='green', linestyle='--')
axs[1][1].axvline(fs / 2, color='red', linestyle='--')

fig.tight_layout()
plt.show()

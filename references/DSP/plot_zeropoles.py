import matplotlib.pyplot as plt
import matplotlib.patches as patch
from scipy import signal
import numpy as np

N = 24
f0 = 1000
fs = 48000

b,a = signal.butter(N, f0, 'high', analog=False, fs=fs)
ba_z, ba_p, ba_k = signal.tf2zpk(b, a)
sos = signal.butter(N, f0, 'high', analog=False, fs=fs, output='sos')
sos_z, sos_p, sos_k = signal.sos2zpk(sos)

fig, axs = plt.subplots(1, 2)

fig.suptitle(f"Butterworth highpass filter Pole-Zero map, order {N}, $f_0={f0}$ Hz, $f_s={fs}$ Hz")

axs[0].set_title(f"Computation using output='ba'")
axs[0].grid(which='both', axis='both')
axs[0].set_xlim(-1.5, 1.5)
axs[0].set_xlabel("Real part")
axs[0].set_ylim(-1.5, 1.5)
axs[0].set_ylabel("Imaginary part")
axs[0].add_patch(patch.Circle([0,0], radius=1, fill=False, linestyle='--'))

axs[0].plot(np.real(ba_p), np.imag(ba_p), 'xr')
axs[0].plot(np.real(ba_z), np.imag(ba_z), '.b')

axs[1].set_title(f"Computation using output='sos'")
axs[1].grid(which='both', axis='both')
axs[1].set_xlim(-1.5, 1.5)
axs[1].set_xlabel("Real part")
axs[1].set_ylim(-1.5, 1.5)
axs[1].set_ylabel("Imaginary part")
axs[1].add_patch(patch.Circle([0,0], radius=1, fill=False, linestyle='--'))

axs[1].plot(np.real(sos_p), np.imag(sos_p), 'xr')
axs[1].plot(np.real(sos_z), np.imag(sos_z), '.b')

plt.show()
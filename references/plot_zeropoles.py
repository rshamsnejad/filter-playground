import matplotlib.pyplot as plt
import matplotlib.patches as patch
from scipy import signal
import numpy as np

N = 24
f0 = 1000
fs = 48000

b, a = signal.butter(N, f0, 'high', analog=False, fs=fs)

zeroes, poles, gain = signal.tf2zpk(b, a)

plt.title(f"Butterworth highpass filter poles, order {N}, $f_0={f0}$ Hz, $f_s={fs}$ Hz")
plt.grid(which='both', axis='both')
plt.xlim(-1.5, 1.5)
plt.xlabel("Real part")
plt.ylim(-1.5, 1.5)
plt.ylabel("Imaginary part")
plt.gca().add_patch(patch.Circle([0,0], radius=1, fill=False, linestyle='--'))

plt.scatter(np.real(poles), np.imag(poles), edgecolors='blue', facecolors='none')
plt.show()
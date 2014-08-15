import numpy as np
import random
from numpy.fft import rfft, irfft
import matplotlib.pyplot as plt
import time

N = 512
fs = 1000.0


def downsample(arr, length, N):
    out = np.zeros(length)
    out[:(length/N + ((length % N) > 0) * 1)] = arr[::N]
    return out


def filter1(signal):
    pass


t = np.linspace(0, (N-1)/fs, N)
y = sum([np.sin(20*2*np.pi*t),
         np.sin(40*2*np.pi*t),
         np.sin(60*2*np.pi*t),
        [random.random()-0.5 for ts in t]])

# TODO: Hier een highpass/band filter overheen
tic = time.time()
freqs = rfft(y)
r = irfft(freqs * np.conj(freqs))
r2 = downsample(r, N, 2)
r3 = downsample(r, N, 3)
r4 = downsample(r, N, 4)
r = r + r2 + r3 + r4
root = fs/(9 + np.argmax(r[10:]))
toc = time.time()
print("Elapsed time: {0} seconds".format(toc-tic))


print("Fundamental freq: {0}Hz".format(root))
plt.subplot(211)
plt.plot(t, y)
plt.subplot(212)
plt.plot(t, r)
plt.show()

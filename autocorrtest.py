import numpy as np
import matplotlib.pyplot as plt

N = 16
fs = 8

t = np.linspace(0, (N-1)/fs, N)

testsig = np.sin(2 * np.pi * t)  # + 0.5 * np.sin(100 * 2 * np.pi * t)

y = [sum([testsig[k]*testsig[k+n] for k in range(N/2)]) for n in range(N/2)]

plt.plot(np.linspace(0, (N-1)/(2*fs), N/2), y)
plt.show()

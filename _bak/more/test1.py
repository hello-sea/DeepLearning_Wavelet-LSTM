from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(1, 201, 200, endpoint=False)
sig  = np.cos(2 * np.pi * 7 * t) + signal.gausspulse(t - 0.4, fc=2)
widths = np.arange(1, 31)
cwtmatr = signal.cwt(sig, signal.ricker, widths)
plt.imshow(cwtmatr, extent=[1, 201, 31, 1], cmap='PRGn', aspect='auto',
          vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
plt.show()

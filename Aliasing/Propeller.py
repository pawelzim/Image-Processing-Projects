import matplotlib.pyplot as plt
import numpy as np
# FFMpegWriter do zapisywania pliku o rozszerzeniu .mp4
from matplotlib.animation import FFMpegWriter
# PillowWriter do zapisywania pliku o rozszerzeniu .gif
from matplotlib.animation import PillowWriter
plt.rcParams['animation.ffmpeg_path'] = 'C:\\PATH_Programs\\ffmpeg.exe'

m = -32

# liczba lopat
prop_nr = 3

f1 = plt.figure()

x_val = np.linspace(0, 2*np.pi, 1000)

data = dict(title='Video')
writer = FFMpegWriter(fps=16, metadata=data)

with writer.saving(f1, "prop2.mp4", 100):
    for M in range(400):
        plt.clf()
        m = M / 2
        y_val = np.sin(prop_nr * x_val + m * np.pi / 10)
        plt.polar(x_val, y_val)
        writer.grab_frame()
        plt.pause(0.0001)
quit()

# plt.show()

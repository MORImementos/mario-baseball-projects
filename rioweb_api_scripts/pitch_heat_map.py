import matplotlib.pyplot as plt
import numpy as np
from rioweb_api_scripts import rio_event_grabber

"""generate a heatmap graphic of pitch locations"""

x_pitch = []
z_pitch = []

for list_of_events in rio_event_grabber.pull2.values():
    for event in list_of_events:
        x_pitch.append(event["pitch_ball_x_pos"])
        z_pitch.append(event["pitch_ball_z_pos"])

Z = np.random.rand(6, 10)
x = np.arange(-0.5, 10, 1)  # len = 11
y = np.arange(4.5, 11, 1)  # len = 7

fig, ax = plt.subplots()
ax.pcolormesh(x, y, Z)


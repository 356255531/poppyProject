
# coding: utf-8

# Just make some demos

# In[1]:

from pypot.vrep import from_vrep
from poppy.creatures import PoppyTorso

poppy = PoppyTorso(simulator='vrep')# Display the Poppy in the simulator


# In[2]:

poppy.motors


# In[2]:

poppy.reset_simulation()
io = poppy._controllers[0].io
name = 'cube'
position = [0, -0.15, 0.8] # X, Y, Z
sizes = [0.1, 0.1, 0.1] # in meters
mass = 0.01 # in kg
io.add_cube(name, position, sizes, mass)



# In[3]:

import time

import math

amp = 30 # in degrees
freq = 0.5 # in Hz

t0 = time.time()

while True:
    t = time.time()

    # run for 10s
    if t - t0 > 10:
        break

    poppy.head_z.goal_position = amp * math.sin(2 * 3.14 * freq * t)

    time.sleep(0.04)


# In[4]:

poppy.l_arm_z.goal_position = -15
poppy.r_arm_z.goal_position = 15


# In[69]:

from IPython.display import VimeoVideo
VimeoVideo(127023576)


# In[ ]:




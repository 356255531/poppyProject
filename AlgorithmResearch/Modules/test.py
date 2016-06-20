import numpy as np
a=np.array([[1,0,0], [1,0,0], [0,0,1]])
x, y = a.nonzero()
print x, y
print x.mean(), y.mean()
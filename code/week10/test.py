import matplotlib.pyplot as plt
import numpy as np

xpoints = np.array([1, 8, 3])
ypoints = np.array([3, 10, 6])
zpoints = np.array([2, 5, 1])

#print(xpoints,ypoints)

#plt.plot(xpoints, ypoints,zpoints)

x = xpoints
x = np.expand_dims(x,axis=0)
y = ypoints
y = np.expand_dims(y,axis=0)
z = zpoints
z = np.expand_dims(z,axis=0)

fig=plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.plot_wireframe(x,y,z,rstride=10,cstride=10)
plt.show()
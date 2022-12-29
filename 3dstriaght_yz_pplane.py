import meep as mp
import matplotlib.pyplot as plt
from mayavi import mlab
from IPython.display import Video



resolution = 20
cell_size = mp.Vector3(14, 30, 30)
x = 20
y = 2
z = 3

pml_layer = [mp.PML(thickness=1)]

material_shape = mp.Block(size=mp.Vector3(x, y, z), center=mp.Vector3(), material=mp.Medium(epsilon=12))
geometry = [material_shape]

f_max = 0.02
f_min = 0.01
df = f_max - f_min
center_f = 0.5 * (f_max + f_min)
source1 = mp.Source(mp.GaussianSource(frequency=center_f, fwidth=df), center=mp.Vector3(), size=mp.Vector3(0.5, y, z),
                    component=mp.Ez)
sources = [source1]

######################  y-z plane
output_plane = mp.Volume(center=mp.Vector3(2,0, 0), size=mp.Vector3(0, y, z))

sim = mp.Simulation(cell_size=cell_size,
                    boundary_layers=pml_layer,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution
                    )
#ez_data = mp.get_array(componenet=mp.Ez)
sim.run(until=5)
#ez_data = sim.get_array(center=mp.Vector3(), size=cell_size, component=mp.Ez)
sim.plot2D(output_plane=output_plane, fields=mp.Ez)
plt.show()



###################### 2d animation of the y-z plane
animate = mp.Animate2D(sim, mp.Ez, normalize=True, realtime=True, output_plane=output_plane)
sim.run(mp.at_every(1, animate), until=20)
plt.show()
plt.close()
####################################################################################

############### video###################################
#filename="3d_yz_plane.mp4"
#animate.to_mp4(10, filename)
#Video(filename)


###############gif
filename="3d_yz_plane.gif"
animate.to_gif(10, filename)
#Video(filename)
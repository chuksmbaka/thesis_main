import meep as mp
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Video


a = 0.000001  # unit scale in meep
c = 299792458  # speed of light in a vacuum

def freq_to_mp(frequency_in_hz):
    meep_freq = (frequency_in_hz * a)/c
    return meep_freq

def meter_to_mp(length_in_meters):
    aa = 1                                   # aa = 1 micro meter
    meep_length = length_in_meters/aa
    return meep_length

def sec_to_mp(time_in_secs):
    meep_time = time_in_secs*c/a
    return meep_time


def func():
    resolution = 20
    cell_size = mp.Vector3(18, 14)
    pml_layers = [mp.PML(thickness=2)] # symmetries=[mp.Mirror(mp.Y, phase=-1)]

    rot_angle = np.radians(20)
    geometry = [
        mp.Block(
            center=mp.Vector3(),
            size=mp.Vector3(mp.inf, 1, mp.inf),
            e1=mp.Vector3(1, 0, 0),
            e2=mp.Vector3(0, 1, 0),
            material=mp.Medium(epsilon=12),
        )
    ]
    fsrc = freq_to_mp(45e12) # frequency of eigenmode or constant-amplitude source
    #fsrc = freq_to_mp(199.7904683)
    print("freq, ", fsrc)
    kx = 1  # initial wavevector guess in x direction of the eigenmode
    kpoint = mp.Vector3(x=kx)
    bnum = 1  # band number of the eigenmode

    sources = [
        mp.EigenModeSource(
            #src=mp.ContinuousSource(fsrc, fwidth=0.5 * fsrc),
            src=mp.ContinuousSource(fsrc),
            center=mp.Vector3(-7),
            size=mp.Vector3(y=2),
            direction=mp.NO_DIRECTION,
            eig_kpoint=kpoint,
            eig_band=bnum,
            # eig_parity=mp.EVEN_Y + mp.ODD_Z if rot_angle == 0 else mp.ODD_Z,
            eig_match_freq=True,
        )
    ]

    sim = mp.Simulation(
        cell_size=cell_size,
        resolution=resolution,
        boundary_layers=pml_layers,
        sources=sources,
        geometry=geometry,
        # symmetries=[mp.Mirror(mp.Y, phase=-1)]
    )

    # Define xy plane
    # output_plane = mp.Volume(center=mp.Vector3(), size=mp.Vector3(3, 1))
    # f = plt.figure(dpi=100)
    # animate = mp.Animate2D(sim, mp.Ez, f=f, normalize=True, output_plane=output_plane, realtime=True)
    # animate = mp.Animate2D(sim, mp.Ez, normalize=True, output_plane=output_plane, realtime=True)
    animate = mp.Animate2D(sim, mp.Ez, normalize=True, realtime=True)
    sim.run(mp.at_every(1, animate), until=100)
    # sim.plot2D(output_plane=output_plplotting mode profile using meeprmat('Ez_in_xy_plane'))
    plt.show()
    plt.close()


# filename = "2d_straigth_eigcw_9.mp4"
# animate.to_mp4(10, filename)
# Video(filename)

    filename = "2d_straigth_eigcw_9.gif"
    animate.to_gif(10, filename)


if __name__ == '__main__':
    func()



    

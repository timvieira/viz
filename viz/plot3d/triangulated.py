# Based on
# http://matplotlib.1069221.n5.nabble.com/Plotting-3D-Irregularly-Triangulated-Surfaces-An-Example-td9652.html

import numpy as np
import matplotlib.pyplot as pl
from matplotlib.delaunay import delaunay
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d.axes3d import Axes3D


def triangulated_surface(x,y,z):
    """
    3d surface plot of irregularly space samples. Surface is found by tessulating XY plane.
    """

    # Create a triangulation of our region.
    _, _, tri_points, _ = delaunay(x, y)

    data = np.array([x,y,z]).T

    # Construct the triangles for the surface.
    verts = np.array([[data[i], data[j], data[k]] for (i,j,k) in tri_points])

    # To get a coloured plot, we need to assign a value to each face that
    # dictates the colour.  In this case we'll just use the average z
    # co-ordinate of the three triangle vertices.  One of these values is
    # required for each face (triangle).
    z_color = np.array([(np.sum(v_p[:,2]) / 3.0) for v_p in verts])

    # Choiced for colour maps are :
    #   autumn bone cool copper flag gray hot hsv jet pink prism spring summer
    #   winter spectral
    cm = pl.cm.get_cmap("jet")

    # Our triangles are now turned into a collection of polygons using the
    # vertex array.  We assign the colour map here, which will figure out its
    # required ranges all by itself.
    triCol = Poly3DCollection(verts, cmap=cm)

    triCol.set_edgecolor('k')
    triCol.set_linewidth(0.1)

    # Set the value array associated with the polygons.
    triCol.set_array(z_color)

    # Create the plotting figure and the 3D axes.
    fig = pl.figure()
    ax = Axes3D(fig)

    # Add our two collections of 3D polygons directly.  The collections have all of
    # the point and color information.  We don't need the add_collection3d method,
    # since that method actually converts 2D polygons to 3D polygons.  We already
    # have 3D polygons.
    ax.add_collection(triCol)

    # Add a label, for interest
    #ax.text3D(0.0, 0.0, 2.1, "Peak/Trough")

    # If we don't bound the axes correctly the display will be off.
    ax.set_xlim3d(x.min(), x.max())
    ax.set_ylim3d(y.min(), y.max())
    ax.set_zlim3d(z.min(), z.max())

    # We could also print to a file here.
    pl.show()

    return ax

def mayavi_version(X,Y,Z):
    from mayavi import mlab

    # Define the points in 3D space
    # including color code based on Z coordinate.
    pts = mlab.points3d(X, Y, Z, Z)

    # Triangulate based on X, Y with Delaunay 2D algorithm.
    # Save resulting triangulation.
    mesh = mlab.pipeline.delaunay2d(pts)

    # Remove the point representation from the plot
    pts.remove()

    # Draw a surface based on the triangulation
    surf = mlab.pipeline.surface(mesh)

    # Simple plot.
    mlab.xlabel("x")
    mlab.ylabel("y")
    mlab.zlabel("z")
    mlab.show()


def main():
    """
    Demonstration of how to plot a triangulated surface.

    We randomly tesselate the (x,y) plane and compute a quadratic functions over
    those points. The plot displays the two surfaces, each coloured by the
    average z-value of the triangle.
    """

    # Generate 200 random points between -2.0 and 2.0.
    x = np.empty([204])
    y = np.empty([204])

    x[0:200] = np.random.uniform(-2.0, 2.0, [200])
    y[0:200] = np.random.uniform(-2.0, 2.0, [200])

    # Put corners on the range for interest
    x[200:204] = [-2.0, -2.0,  2.0, 2.0]
    y[200:204] = [-2.0, -2.0,  2.0, 2.0]

    # Compute the first function of (x,y)
    z = 2.0 - 1.0 * (x[:]**2 + y[:]**2) - 0.5*y[:]

    triangulated_surface(x,y,z)

#    mayavi_version(x,y,z)


if __name__ == '__main__':
    main()

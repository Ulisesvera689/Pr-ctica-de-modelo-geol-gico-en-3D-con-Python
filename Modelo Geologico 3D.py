# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 19:25:16 2020

@author: HernanV
"""

#Recreate a model of geotermal reservoir, Utah
from vtkplotter import Plotter, Mesh, Points, Line, Lines ,printc, exportWindow, embedWindow
from scipy.spatial import Delaunay
import pandas as pd

embedWindow(False) # or itkwidgets, False (for a popup)



#########################
# Load surfaces, import the file from pandas
#########################
printc("...loading data...", invert=1)
path(data="C:\Users\HernanV\Documents\Spyder (python) files\Modelamiento en 3D con Python\Example3DGeologicModelUsingVTKPlotter-master')
path(open(data, mode, encoding=str))

landSurfacePD = path_csv('landsurface_vertices.csv')
vertices_175CPD = pd.read_csv('175C_vertices.csv')
vertices_225CPD = pd.read_csv('225C_vertices.csv')
Negro_Mag_Fault_verticesPD = pd.read_csv('Negro_Mag_Fault_vertices.csv')
Opal_Mound_Fault_verticesPD = pd.read_csv('Opal_Mound_Fault_vertices.csv')
top_granitoid_verticesPD = pd.read_csv('top_granitoid_vertices.csv')
microseismic = pd.read_csv('Microseismic.csv')

# The well path and different logs for the well paths
well_5832_path = pd.read_csv('path5832.csv')
temp_well = pd.read_csv('temperature5832.csv')
nphi_well = pd.read_csv('nphi5832.csv')
pressure_well = pd.read_csv('pressure5832.csv')

# Since most of the wells in the area were just vertical, I split them into two files:
# One file with the top of the wells and the other with the bottom point of the wellbore
wellsmin = pd.read_csv('MinPointsWells.csv')
wellsmax = pd.read_csv('MaxPointsWells.csv')

# Project boundary area on the surface
border = pd.read_csv('FORGE_Border.csv')

landSurfacePD.heat()


# Create a plotter window
plt = Plotter(axes=dict(xtitle='km', ytitle=' ', ztitle='km*1.5', yzGrid=False),
              size=(1200,900))    # screen size

#############################################
## 1. land surface: a mesh with varying color
#############################################
printc("...analyzing...", invert=1)

# perform a 2D Delaunay triangulation to get the cells from the point cloud
tri = Delaunay(landSurfacePD.values[:, 0:2])

# create a mesh object for the land surface
landSurface = Mesh([landSurfacePD.values, tri.simplices])

# in order to color it by the elevation, we use the z values of the mesh
zvals = landSurface.points()[:, 2]
landSurface.pointColors(zvals, cmap="terrain", vmin=1000)
landSurface.name = "Land Surface" # give the object a name

#add landSurface to the plotter window
plt+=landSurface
plt.show(viewup="z")


## 2. Different meshes with constant colors
#############################################
# Mesh of 175 C isotherm
tri = Delaunay(vertices_175CPD.values[:, 0:2])
vertices_175C = Mesh([vertices_175CPD.values, tri.simplices]).c("orange").opacity(0.3)
vertices_175C.name = "175C temperature isosurface"
plt += vertices_175C.flag()

# Mesh of 225 C isotherm
tri = Delaunay(vertices_225CPD.values[:, 0:2])
vertices_225CT = Mesh([vertices_225CPD.values, tri.simplices]).c("red").opacity(0.4)
vertices_225CT.name = "225C temperature isosurface"
plt += vertices_225CT.flag()

# Negro fault
tri = Delaunay(Negro_Mag_Fault_verticesPD.values[:, 1:3])
Negro_Mag_Fault_vertices = Mesh([Negro_Mag_Fault_verticesPD.values, tri.simplices])
Negro_Mag_Fault_vertices.name = "Negro Fault"
plt += Negro_Mag_Fault_vertices.c("f").opacity(0.6).flag()

# Opal fault
tri = Delaunay(Opal_Mound_Fault_verticesPD.values[:, 1:3])
Opal_Mound_Fault_vertices = Mesh([Opal_Mound_Fault_verticesPD.values, tri.simplices])
Opal_Mound_Fault_vertices.name = "Opal Mound Fault"
plt += Opal_Mound_Fault_vertices.c("g").opacity(0.6).flag()

# Top Granite
xyz = top_granitoid_verticesPD.values
xyz[:, 2] = top_granitoid_verticesPD.values[:, 2] - 20
tri = Delaunay(top_granitoid_verticesPD.values[:, 0:2])
top_granitoid_vertices = Mesh([xyz, tri.simplices]).c("darkcyan")
top_granitoid_vertices.name = "Top of granite surface"
plt += top_granitoid_vertices.flag()

####################
## 3. Point objects
####################
printc("...plotting...", invert=1)

# Microseismic
microseismicxyz = microseismic[["xloc", "yloc", "zloc"]]
scals = microseismic[["mw"]]
microseismicPts = Points(microseismicxyz.values, r=4).pointColors(scals, cmap="jet")
microseismicPts.name = "Microseismic events"
plt += microseismicPts.flag()

####################
## 4. Line objects
####################
# FORGE Boundary. Since the boundary area did not have a Z column,
# I assigned a Z value for where I wanted it to appear
border["zcoord"] = 1650
borderxyz = border[["xcoord", "ycoord", "zcoord"]]
boundary = Line(borderxyz.values).extrude(zshift=120, cap=False).c("k")
boundary.name = "FORGE area boundary"
plt += boundary.flag()

# The path of well 58_32
xyz = well_5832_path[["X", "Y", "Z"]].values
Well = Line(xyz)
Well.name = "Well 58-32"
plt += Well.flag()

# A porosity log in the well
xyz = nphi_well[["X", "Y", "Z"]].values
porosity = nphi_well["Nphi"].values
Well = Line(xyz).pointColors(porosity, cmap="hot").c("gold").lw(2)
Well.name = "Porosity log well 58-32"
plt += Well.flag()

# This well data is actually represented by points since 
# as of right now line coloring can be problematic with k3d
xyz = pressure_well[["X", "Y", "Z"]].values
pressure = pressure_well["Pressure"].values
Well = Points(xyz, r=1).pointColors(pressure, cmap="cool")
Well.name = "Pressure log well 58-32"
plt += Well.flag()

# Temperatue log
xyz = temp_well[["X", "Y", "Z"]].values
temp = temp_well["Temperature"].values
Well = Points(xyz, r=1).pointColors(temp, cmap="seismic")
Well.name = "Temperature log well 58-32"
plt += Well.flag()

#########################
## 5. Multi-line objects
#########################
# defining the start and end of the lines that will be representing the wellbores
Wells = Lines(wellsmin[["x", "y", "z"]].values, # start points
              wellsmax[["x", "y", "z"]].values, # end points
              c="gray", alpha=1, lw=3)
Wells.name = "Pre-existing wellbores"
plt += Wells.flag()

for a in plt.actors:
    # change scale to kilometers in x and y, but expand z scale by 1.5!
    a.scale([0.001, 0.001, 0.0015])

#########################
## 6. Done. show the plot
#########################
plt += __doc__
plt.show(viewup="z")

#exportWindow("page.html") # k3d is the default
                                                                                            
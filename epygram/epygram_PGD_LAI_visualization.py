import epygram as epy
import matplotlib.pyplot as plt
import os
import math
import numpy as np
from cartopy import crs as ccrs

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
epy.init_env()

#A python program to visualize the LAI field of the PGD.fa
#Original author Panu Maalampi

#Input a file name
#PGD.fa is typically a link to Const.Clim.sfx
file_a="PGD.fa"

#PGD.fa input directory. Typically in scratch.
INPUT_DIR="/ec/res4/scratch/fibf/hm_home/dev46h1eg_cdnc_fog_ref2/climate/DKCOEXP/"

#List of time periods (365 days divided by 36 bins)
T= ["T01","T02","T03","T04","T05",
    "T06","T07","T08","T09","T10",
    "T11","T12","T13","T14","T15",
    "T16","T17","T18","T19","T20",
    "T21","T22","T23","T24","T25",
    "T26","T27","T28","T29","T30",
    "T31","T32","T33","T34","T35",
    "T36"]

#List of vegetation patch
V= ["V01","V02","V03","V04","V05",
    "V06","V07","V08","V09","V10",
    "V11","V12","V13","V14","V15",
    "V16","V17","V18","V19","V20"]

#Vegetation patches based on SURFEX v8.1 documentation
Patch=["no vegetation (smooth)", #0
       "no vegetation (rocks)", #1
       "permanent snow and ice", #2
       "temperate broadleaf cold-deciduous summergreen", #3
       "boreal needleleaf evergreen", #4
       "tropical broadleaf evergreen", #5
       "C3 cultures types", #6
       "C4 cultures types", #7
       "irrigated crops", #8
       "grassland (C3)", #9
       "tropical grassland (C4)", #10
       "peat bogs, parks and gardens (irrigated grass)", #11
       "tropical broadleaf deciduous", #12
       "temperate broadleaf evergreen", #13
       "temperate needleleaf evergreen", #14
       "boreal broadleaf cold-deciduous summergreen", #15
       "boreal needleleaf cold-deciduous summergreen", #16
       "boreal grass", #17
       "shrub"] #18

# Select the time period (in python indices, so e.g. 0= T01)
Time=17

# Select the vegetation patch (in python indices, so e.g.
# 0= V01 + "no vegetation (smooth)")
Vegetation_patch=4

LAI=T[Time] + V[Vegetation_patch]

#Compilation of chosen variable name from PGD.fa
init="SFX.D_LAI_"
variable=init + str(LAI)

#Epygram reads variable from the file PGD.fa
A=epy.formats.resource(os.path.join(INPUT_DIR, file_a), 'r')
var_a=A.readfield(variable)

# Choose your domain
#[W,E,S,N]
area_a={"lonmin":-7.5,"lonmax":27.5,"latmin":47.5,"latmax":64}

var_a=var_a.extract_zoom(zoom=area_a)

#Prepare the figure
fig = plt.figure(figsize=(7.8,6))

proj=var_a.geometry.default_cartopy_CRS()

ax_a = fig.add_subplot(1, 1, 1, projection=proj)

var_a.cartoplot(fig=fig, ax=ax_a,
                plot_method="contourf",
                subzone=area_a,
                colormap="RdYlBu",
                title='',
                colorbounds=[0,1,2,3,4,5,6,7,8,9,10,11,12,13],
                minmax_along_colorbar=False)


ax_a.set_title(str(LAI) + ": " + Patch[Vegetation_patch], fontsize=15)

fig.suptitle("LAI visualized",fontsize=15)

fig.set_tight_layout(True)
plt.tight_layout()

#Figure is saved to your $pwd
fig.savefig("LAI_" + str(LAI) + "_visualized.png", dpi=300)
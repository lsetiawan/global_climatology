#!/usr/bin/env python

# Import the necessary libraries
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import numpy as np
import xarray as xr
import cartopy
import cartopy.crs as ccrs
import shapely.geometry as sgeom
from cartopy.util import add_cyclic_point
import sys

class Glodap(object):
    def __init__(self, pth, ds_name, *args, **kwargs):
        self.pth = pth
        self.ds_name = ds_name
        self.new_path = ""
        self.names = []
        self.dataset = []
        self.depths = []
        self.my_cmap = None
        self.i = 0
        self.vmin = None
        self.vmax = None
        work_file = os.path.join(pth, '{}'.format(ds_name))

        print "Working on {}".format(work_file)
        self.ds = xr.open_dataset(work_file)

        if ds_name != 'SOCAT_tracks_gridded_decades_v3.nc':
            self.var_name = ds_name.split(".")
            print self.var_name
            self.data = self.ds[self.var_name[2]]
            self.pre = self.var_name[2]

    def get_dataset(self):
        if not os.path.exists("{}_climatology".format(self.pre)):
            os.mkdir("{}_climatology".format(self.pre))

        self.new_path = "./{}_climatology".format(self.pre)

        depth_list = np.array(self.ds.Depth).tolist()
        for l in depth_list:
            self.depths.append(int(l))

        fw = open("./{0}/{1}_min_max.txt".format(self.new_path,self.pre), 'w')

        for i in range(0, 33):
            # Get multiple depth 1972-2013 dataset
            self.dataset.append(self.data[i, :, :])
            self.names.append("{0}_{1}m".format(self.pre, self.depths[i]))
            fw.write("{0}m,{1},{2};".format(self.depths[i], self.data[i, :, :].min().values,
                                                self.data[i, :, :].max().values))
        fw.close()

    def create_cmap(self):
        if self.pre == "OmegaA":
            colors = [(8, 0, 5), (255, 0, 242), (91, 0, 234), (0, 255, 245), (0, 255, 124),
                      (244, 250, 97), (255, 122, 53), (255, 0, 25), (111, 8, 18)]
            position = [0, 0.19, 0.19, 0.38, 0.50, 0.62, 0.75, 0.9, 1]
            self.my_cmap = self.make_cmap(colors, position=position, bit=True)
            self.export_colormap('{}_colorbar'.format(self.pre))
            self.vmin = 0
            self.vmax = 5

        elif self.pre == "pHts25p0" or self.pre == "fco2_ave_weighted_decade" or self.pre == "fco2_ave_unwtd_decade":
            self.my_cmap = 'rainbow'
            self.export_colormap('{}_colorbar'.format(self.pre))
            if self.pre == "pHts25p0":
                self.vmin = 7.7
                self.vmax = 8.2
            else:
                self.vmin = 240
                self.vmax = 480
        elif self.pre == "TCO2":
            colors = [(38, 38, 38), (33, 45, 84), (40, 142, 132), (212, 219, 21), (219, 113, 15),
                      (173, 25, 18)]
            position = [0, 0.2, 0.4, 0.6, 0.8, 1]
            self.my_cmap = self.make_cmap(colors, position=position, bit=True)
            self.export_colormap('{}_colorbar'.format(self.pre))
            self.vmin = 1800
            self.vmax = 2200

    def export_colormap(self,name, *args, **kwargs):
        '''
        This function is used to export colormap to size of 1000px width and 1px height
        export_colormap takes a name of the output and the colormap desired to be saved as a png
        :param name: is the name of the output
        :param cmap: is the colormap
        :return: a png file with the colorbar name
        '''
        im = np.outer(np.ones(1), np.arange(1000))
        fig, ax = plt.subplots(1, figsize=(5, 10), subplot_kw=dict(xticks=[], yticks=[]))
        # fig.subplots_adjust(hspace=0.1)
        ax.imshow(im, cmap=self.my_cmap)
        ax.axis('off')
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(4.3115, 0.5)

        plt.savefig('./{0}/{1}.png'.format(self.new_path,name), bbox_inches='tight', dpi=299.5,
                    transparent=True, format='png', pad_inches=0.0)

    def make_cmap(self,colors, position=None, bit=False, *args, **kwargs):
        '''
        make_cmap takes a list of tuples which contain RGB values. The RGB
        values may either be in 8-bit [0 to 255] (in which bit must be set to
        True when called) or arithmetic [0 to 1] (default). make_cmap returns
        a cmap with equally spaced colors.
        Arrange your tuples so that the first color is the lowest value for the
        colorbar and the last is the highest.
        position contains values from 0 to 1 to dictate the location of each color.
        '''
        bit_rgb = np.linspace(0,1,256)
        if position == None:
            position = np.linspace(0,1,len(colors))
        else:
            if len(position) != len(colors):
                sys.exit("position length must be the same as colors")
            elif position[0] != 0 or position[-1] != 1:
                sys.exit("position must start with 0 and end with 1")
        if bit:
            for i in range(len(colors)):
                colors[i] = (bit_rgb[colors[i][0]],
                             bit_rgb[colors[i][1]],
                             bit_rgb[colors[i][2]])
        cdict = {'red':[], 'green':[], 'blue':[]}
        for pos, color in zip(position, colors):
            cdict['red'].append((pos, color[0], color[0]))
            cdict['green'].append((pos, color[1], color[1]))
            cdict['blue'].append((pos, color[2], color[2]))

        cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
        return cmap

    def makeLatLng(self):
        lats = []
        lons = []
        for k in range(20, 380):
            lons.append(float(k))
        for l in range(-90, 90):
            lats.append(float(l))

        lons_np = np.array(lons)
        lats_np = np.array(lats)
        return lons_np,lats_np

    def getPNG(self,da, *args, **kwargs):
        plt.figure(figsize=(40,30), frameon=False, dpi=300)
        box = sgeom.box(minx=-180, maxx=180, miny=-85,
                        maxy=85)
        x0, y0, x1, y1 = box.bounds
        # Set output projection
        ax = plt.axes(projection=ccrs.PlateCarree())

        #ax.set_global()
        ax.set_extent([x0, x1, y0, y1], crs=ccrs.PlateCarree())

        # Define the coordinate system that the grid lons and grid lats are on
        coord = ccrs.PlateCarree()  # aka Lat,Long

        # Plots the data
        da.plot(ax=ax, transform=coord, add_colorbar=False, vmin=self.vmin, vmax=self.vmax, add_labels=False, cmap=self.my_cmap)
        ax.background_patch.set_visible(False)
        ax.outline_patch.set_visible(False)

        plt.savefig(os.path.join(self.new_path, '{0}.png'.format(self.names[self.i])),
                    bbox_inches='tight', dpi=300,
                    transparent=True, format='png', pad_inches=0.0)

    def prnt_lib_ver(self):
        '''
            Function used to print the current versions of xarray, cartopy, and numpy
        '''
        print "xarray version: " + xr.__version__
        print "cartopy version: " + cartopy.__version__
        print "numpy version: " + np.__version__

    def processData(self):

        lons_np, lats_np = self.makeLatLng()

        # Processing
        for self.i in range(0, len(self.names)):
            if self.i == 0 or self.i == 9:
                print "Processing "+ self.names[self.i]

                lons_r = np.roll(lons_np, 200, axis=0)
                lons_c = add_cyclic_point(lons_r)

                ds_np = np.array(self.dataset[self.i])
                ds_rolled = np.roll(ds_np, 200, axis=1)
                cyclic_data = add_cyclic_point(ds_rolled)

                da = xr.DataArray(cyclic_data, coords=[lats_np, lons_c], dims=['lat', 'lon'])

                self.getPNG(da)

class Socat(Glodap):

    def __init__(self,pth,ds_name,avg_method = 'weighted'):
        super(Socat, self).__init__(pth,ds_name)

        if not os.path.exists("socat_decade"):
            os.mkdir("socat_decade")

        if avg_method == 'weighted':
            v = "fco2_ave_weighted_decade"
            print "Working on {}".format(v)

            self.data = self.ds[v]
            self.pre = v
        elif avg_method == 'unweighted':
            v = "fco2_ave_unwtd_decade"
            print "Working on {}".format(v)

            self.data = self.ds[v]
            self.pre = v
        else:
            print "That is an invalid average method, please type 'weighted' or 'unweighted'."


    def makeLatLng(self):
        lats = []
        lons = []
        for i in range(-180, 180):
            lons.append(float(i) + 0.5)
        for j in range(-90, 90):
            lats.append(float(j) + 0.5)

        lons_np = np.array(lons)
        lats_np = np.array(lats)

        return lons_np, lats_np

    def get_dataset(self):
        if not os.path.exists("./socat_decade/{}_climatology".format(self.pre)):
            os.mkdir("./socat_decade/{}_climatology".format(self.pre))

        self.new_path = "./socat_decade/{}_climatology".format(self.pre)


        date = np.array(self.ds.tdecade)
        time_list = date.astype(str)

        time = [l.split('T')[0] for l in time_list]
        time = [t.replace('-', '_') for t in time]

        names = []

        fw = open("./socat_decade/{0}_min_max.txt".format(self.pre), 'w')
        # Min Max
        for i in range(0, 5):
            # Get multiple time dataset
            self.dataset.append(self.data[i, :, :])

            self.names.append("{0}_{1}".format(self.pre, time[i]))
            fw.write("{0},{1},{2};".format(time[i], self.data[i, :, :].min().values,
                                           self.data[i, :, :].max().values))

        fw.close()


    def processData(self):
        lons_np, lats_np = self.makeLatLng()

        # Processing
        for self.i in range(0, len(self.names)):

            ds_np = np.array(self.dataset[self.i])
            cyclic_data, cyclic_lon = add_cyclic_point(ds_np, coord=lons_np)

            da = xr.DataArray(cyclic_data, coords=[lats_np, cyclic_lon], dims=['lat', 'lon'])


            self.getPNG(da)
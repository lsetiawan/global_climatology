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
    def __init__(self, pth, ds_name):
        self.pth = pth
        self.ds_name = ds_name

    def export_colormap(self,name, cmap):
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
        ax.imshow(im, cmap=cmap)
        ax.axis('off')
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(4.3115, 0.5)

        plt.savefig('{}.png'.format(name), bbox_inches='tight', dpi=299.5, transparent=True, format='png', pad_inches=0.0)
        if name == 'fco2_colorbar':
            plt.savefig('./socat_decade/{}.png'.format(name), bbox_inches='tight', dpi=299.5, transparent=True, format='png', pad_inches=0.0)

    def make_cmap(self,colors, position=None, bit=False):
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

    def getPNG(self,name, data, pre):
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


        if pre == "arag":
            ### Create a list of RGB tuples
            colors = [(8, 0, 5), (255, 0, 242), (91, 0, 234), (0, 255, 245), (0, 255, 124),
                      (244, 250, 97), (255, 122, 53), (255, 0, 25), (111, 8, 18)] # This example uses the 8-bit RGB
            ### Create an array or list of positions from 0 to 1.
            position = [0,0.19,0.19,0.38,0.50,0.62,0.75,0.9,1]
            ### Call the function make_cmap which returns your colormap
            my_cmap = self.make_cmap(colors, position=position, bit=True)
            # Plots the data
            data.plot(ax=ax, transform=coord, add_colorbar=False, vmin=0, vmax=5, add_labels=False, cmap=my_cmap)
            ax.background_patch.set_visible(False)
            ax.outline_patch.set_visible(False)
            # Put Coastline on figure
            if not os.path.exists("{}_climatology".format(pre)):
                os.mkdir("{}_climatology".format(pre))
            plt.savefig(os.path.join("{}_climatology".format(pre), '{0}.png'.format(name)), bbox_inches='tight', dpi=300,
                        transparent=True, format='png', pad_inches=0.0)

            self.export_colormap('arag_colorbar', my_cmap)
        elif pre == "ph":
            my_cmap = 'rainbow'
            print data
            data.plot(ax=ax, transform=coord, add_colorbar=False, vmin=7.7, vmax=8.2, add_labels=False, cmap=my_cmap)
            ax.background_patch.set_visible(False)
            ax.outline_patch.set_visible(False)
            # Put Coastline on figure
            # ax.coastlines()
            if not os.path.exists("{}_climatology".format(pre)):
                os.mkdir("{}_climatology".format(pre))
            plt.savefig(os.path.join("{}_climatology".format(pre), '{0}.png'.format(name)), bbox_inches='tight', dpi=300,
                        transparent=True, format='png', pad_inches=0.0)

            self.export_colormap('ph_colorbar', my_cmap)
        elif pre == "tco2":
            ### Create a list of RGB tuples
            colors = [(38, 38, 38), (33, 45, 84), (40, 142, 132), (212, 219, 21), (219, 113, 15), (173, 25, 18)]  # This example uses the 8-bit RGB
            ### Create an array or list of positions from 0 to 1.
            position = [0, 0.2, 0.4, 0.6, 0.8, 1]
            ### Call the function make_cmap which returns your colormap
            my_cmap = self.make_cmap(colors, position=position, bit=True)
            # Plots the data
            print data
            data.plot(ax=ax, transform=coord, add_colorbar=False, vmin=1800,vmax=2200, add_labels=False, cmap=my_cmap)

            ax.background_patch.set_visible(False)
            ax.outline_patch.set_visible(False)
            # Put Coastline on figure
            # ax.coastlines()
            if not os.path.exists("{}_climatology".format(pre)):
                os.mkdir("{}_climatology".format(pre))
            plt.savefig(os.path.join("{}_climatology".format(pre), '{0}.png'.format(name)), bbox_inches='tight', dpi=300,
                        transparent=True, format='png', pad_inches=0.0)

            self.export_colormap('tco2_colorbar', my_cmap)

        elif pre == "fco2_weighted" or pre == "fco2_unwtd":
            ### Call the function make_cmap which returns your colormap
            my_cmap = 'rainbow'
            # Plots the data
            print data
            data.plot(ax=ax, transform=coord, add_colorbar=False, vmin=240, vmax=480, add_labels=False, cmap=my_cmap)

            ax.background_patch.set_visible(False)
            ax.outline_patch.set_visible(False)
            # Put Coastline on figure
            # ax.coastlines()

            if not os.path.exists("./socat_decade/{}_climatology".format(pre)):
                os.mkdir("./socat_decade/{}_climatology".format(pre))
            plt.savefig(os.path.join("./socat_decade/{}_climatology".format(pre), '{0}.png'.format(name)), bbox_inches='tight', dpi=300,
                        transparent=True, format='png', pad_inches=0.0)

            self.export_colormap('fco2_colorbar', my_cmap)

    def get_dataset(self, pth, ds_name):
        work_file = os.path.join(pth, '{}'.format(ds_name))
        print "Working on {}".format(work_file)
        ds = xr.open_dataset(work_file)
        if ds_name == "GLODAPv2.2016b.OmegaA.nc":
            data = ds.OmegaA
            pre = "arag"
        elif ds_name == "GLODAPv2.2016b.pHts25p0.nc":
            data = ds.pHts25p0
            pre = "ph"
        elif ds_name == "GLODAPv2.2016b.TCO2.nc":
            data = ds.TCO2
            pre = "tco2"

        ds72_13 = []

        depth_list = np.array(ds.Depth).tolist()
        d = []
        for l in depth_list:
            d.append(int(l))
        names = []

        fw = open("{}_min_max_72_13.txt".format(pre), 'w')
        # Time 1
        for i in range(0,33):
            # Get multiple depth 1972-2013 dataset
            ds72_13.append(data[i, :, :])
            time = "7213"
            names.append("{0}_{1}m_{2}".format(pre, d[i], time))
            fw.write("{0}m,{1},{2},{3};".format(d[i], time, data[i, :, :].min().values,
                                                    data[i, :, :].max().values))

        fw.close()


        return ds72_13, names, pre

    def prnt_lib_ver(self):
        '''
            Function used to print the current versions of xarray, cartopy, and numpy
        '''
        print "xarray version: " + xr.__version__
        print "cartopy version: " + cartopy.__version__
        print "numpy version: " + np.__version__

    def processData(self):
        ds72_13, names, pre = self.get_dataset(self.pth, self.ds_name)

        lons_np, lats_np = self.makeLatLng()

        # Processing
        for i in range(0, len(names)):
            if "7213" in names[i]:
                # print "{0} {1} {2}".format(i, names[i], ds72_13[i])
                if i == 0 or i == 9:
                    print names[i]
                    # print ds72_13[i]
                    # Shift

                    lons_r = np.roll(lons_np, 200, axis=0)
                    lons_c = add_cyclic_point(lons_r)

                    ds_d0_np = np.array(ds72_13[i])
                    ds_rolled = np.roll(ds_d0_np, 200, axis=1)
                    cyclic_data = add_cyclic_point(ds_rolled)

                    da = xr.DataArray(cyclic_data, coords=[lats_np, lons_c], dims=['lat', 'lon'])
                    print da

                    self.getPNG(names[i], da, pre)
class Socat(Glodap):

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

    def get_dataset(self, pth, ds_name):
        work_file = os.path.join(pth, '{}'.format(ds_name))
        print "Working on {}".format(work_file)
        ds = xr.open_dataset(work_file)

        var = [str(k) for k in ds.keys()]

        for v in var:
            if v == "fco2_ave_weighted_decade":
                data = ds.fco2_ave_weighted_decade
                pre_w = "fco2_weighted"
                da_w, names_w = self.calcMinMax(ds,pre_w,data)
            if v == "fco2_ave_unwtd_decade":
                data = ds.fco2_ave_unwtd_decade
                pre_uw = "fco2_unwtd"
                da_uw, names_uw = self.calcMinMax(ds, pre_uw, data)

        dataset = [da_w,da_uw]
        names = [names_w,names_uw]
        pre = [pre_w, pre_uw]
        return dataset, names, pre

    def calcMinMax(self, ds, pre, data):
        dataset = []

        date = np.array(ds.tdecade)
        time_list = date.astype(str)

        time = [l.split('T')[0] for l in time_list]
        time = [t.replace('-', '_') for t in time]

        names = []

        if not os.path.exists("socat_decade"):
            os.mkdir("socat_decade")

        fw = open("./socat_decade/{0}_min_max.txt".format(pre), 'w')
        # Min Max
        for i in range(0, 5):

            # Get multiple time dataset
            dataset.append(data[i, :, :])

            names.append("{0}_{1}".format(pre, time[i]))
            fw.write("{0},{1},{2};".format(time[i], data[i, :, :].min().values,
                                                data[i, :, :].max().values))

        fw.close()

        return dataset, names

    def processData(self):
        dataset, names, pre = self.get_dataset(self.pth, self.ds_name)

        #print pre

        lons_np, lats_np = self.makeLatLng()

        # Processing
        for j in range(0, len(names)):
            for i in range(0, len(names[j])):

                ds_np = np.array(dataset[j][i])
                cyclic_data, cyclic_lon = add_cyclic_point(ds_np, coord=lons_np)

                da = xr.DataArray(cyclic_data, coords=[lats_np, cyclic_lon], dims=['lat', 'lon'])
                print pre[j], names[j][i], da

                self.getPNG(names[j][i], da, pre[j])
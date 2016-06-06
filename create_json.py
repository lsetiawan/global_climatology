#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time, calendar, datetime
import os

class MakeJSON(object):
    '''
        This class is intended to make JSON files for the different dataset of GLODAPv2 data
        Parameters are set in the main section of the script
    '''

    def __init__(self,var,dataset,min_max,base_url,year,units,colormap,colorbar,p,tickmarks):
        # Set variables
        self.num = 0
        self.dataset = dataset
        self.min_max = min_max
        self.base_url = base_url
        self.year = year
        self.units = units
        self.colormap = colormap
        self.colorbar = colorbar
        self.p = p
        self.tickmarks = tickmarks
        self.var = var
        self.colormap_long_pixels = 256
        self.colormap_short_pixels = 16
        self.bbox = [-180, 180, -85, 85]

        # Get Date info
        self.forecast_date, self.forecast_start_date, \
        self.forecast_end_date, self.creation_timestamp, \
        self.model_date = self.dates()

        # Get Legend info
        self.legend = self.legends()

    def getMINMAX(self):
        fr = open(self.min_max, 'r')
        s = fr.read()
        fr.close()

        array = s.split(";")

        split = []
        for i in range(0, len(array)):
            split.append(array[i].split(","))

        return split

    def create_json(self,image_url, values):

        # Create main JSON keys
        mainkey = dict()
        if self.legend != "":
            mainkey["legends"] = self.legend
        if self.forecast_date != "":
            mainkey["forecast_date"] = self.forecast_date
        if self.colormap != "":
            mainkey["colormap"] = self.colormap
        if self.colorbar != "":
            mainkey["colorbar_url"] = self.colorbar
        if self.model_date != "":
            mainkey["model_date"] = self.model_date
        if self.colormap_long_pixels != "":
            mainkey["colormap_long_pixels"] = self.colormap_long_pixels

        # FOR MULTIPLE DEPTH
        #if images != "":
        #    mainkey["images"] = images
        if values != "":
            mainkey["values"] = values
        if image_url != "":
            mainkey["image_url"] = image_url
        if self.colormap_short_pixels != "":
            mainkey["colormap_short_pixels"] = self.colormap_short_pixels
        if self.bbox != "":
            mainkey["bbox"] = self.bbox
        if self.var != "":
            mainkey["var"] = self.var
        if self.forecast_end_date != "":
            mainkey["forecast_end_date"] = self.forecast_end_date
        if self.creation_timestamp != "":
            mainkey["creation_timestamp"] = self.creation_timestamp
        if self.forecast_start_date != "":
            mainkey["forecast_start_date"] = self.forecast_start_date
        return mainkey

    def imagesURL(self):
        images = []

        for png in os.listdir(self.dataset):
            for d in self.p:
                if ".DS_Store" not in png:
                    spt = png.split("_")
                    if "{}m".format(d) in spt and "7213" in spt:
                        url = os.path.join(self.base_url, png)
                        key = "{}m".format(d)
                        img = {
                            'url': '{}'.format(url),
                            'key': '{}'.format(key)
                        }
                        images.append(img)
        return images

    def dates(self):
        ts = time.time()
        # Create vars for forecast stuff
        forecast_date = ""
        forecast_start_date = ""
        forecast_end_date = ""

        creation_timestamp = calendar.timegm(time.gmtime())
        model_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')

        if self.year[0] == "7213":
            forecast_date = "1972-01-01T00:00:00Z"
            forecast_start_date = "1972-01-01T00:00:00Z"
            forecast_end_date = "2013-01-01T00:00:00Z"

        return forecast_date,forecast_start_date,forecast_end_date,creation_timestamp,model_date

    def legends(self):
        # Setting units and tickmarks
        units1 = self.units
        units2 = units1
        tick_marks1 = self.tickmarks
        tick_marks2 = tick_marks1

        # main keys
        legend = {
            "v1": {
                "units": units1,
                "colormap_tick_labels": {
                    "0.0": "{}".format(tick_marks1[0]),
                    "0.1": "",
                    "0.2": "{}".format(tick_marks1[1]),
                    "0.3": "",
                    "0.4": "{}".format(tick_marks1[2]),
                    "0.5": "",
                    "0.6": "{}".format(tick_marks1[3]),
                    "0.7": "",
                    "0.8": "{}".format(tick_marks1[4]),
                    "0.9": "",
                    "1.0": "{}".format(tick_marks1[5])
                }
            },
            "v2": {
                "units": units2,
                "colormap_tick_labels": {
                    "0.0": "{}".format(tick_marks2[0]),
                    "0.1": "",
                    "0.2": "{}".format(tick_marks2[1]),
                    "0.3": "",
                    "0.4": "{}".format(tick_marks2[2]),
                    "0.5": "",
                    "0.6": "{}".format(tick_marks2[3]),
                    "0.7": "",
                    "0.8": "{}".format(tick_marks2[4]),
                    "0.9": "",
                    "1.0": "{}".format(tick_marks2[5])
                }
            },
            "default": "v1"
        }

        return legend

    def getJSON(self):
        depth1 = []
        depth2 = []

        # Return min max of each depth in an array
        split = self.GetMINMAX()
        print split

        for png in os.listdir(self.dataset):
            if ".DS_Store" not in png:
                spt = png.split("_")
                if "{}m".format(0) in spt:
                    for y in range(0, len(self.year)):
                        for n in range(0, len(split)):
                            if "{0}.png".format(self.year[y]) in spt and "0m" in split[n] and n == 0:
                                image_url = os.path.join(self.base_url, png)
                                values = {
                                    "min": "{}".format(split[n][2]),
                                    "max": "{}".format(split[n][3])
                                }
                                depth1.append(self.create_json(image_url, values, forecast_start_date=None,
                                                               forecast_end_date=None, creation_timestamp=None,
                                                               model_date=None))

                elif "{}m".format(200) in spt:
                    for y in range(0, len(self.year)):
                        for n in range(0, len(split)):
                            if "{0}.png".format(self.year[y]) in spt and "200m" in split[n] and n == 9:
                                image_url = os.path.join(self.base_url, png)
                                values = {
                                    "min": "{}".format(split[n][2]),
                                    "max": "{}".format(split[n][3])
                                }
                                depth2.append(self.create_json(image_url, values, forecast_start_date=None,
                                                               forecast_end_date=None, creation_timestamp=None,
                                                               model_date=None))
                else:
                    pass

        f0 = open("{0}_{1}m.json".format(self.var, 0), 'w')
        print json.dumps(depth1, sort_keys=False, indent=4, separators=(',', ': '))
        f0.write(json.dumps(depth1, sort_keys=False, indent=4, separators=(',', ': ')))
        f0.close()

        f200 = open("{0}_{1}m.json".format(self.var, 200), 'w')
        print json.dumps(depth2, sort_keys=False, indent=4, separators=(',', ': '))
        f200.write(json.dumps(depth2, sort_keys=False, indent=4, separators=(',', ': ')))
        f200.close()

class SocatJSON(MakeJSON):
    def create_json(self, image_url, values):
        self.num = self.num + 1

        forecast_date, forecast_start_date, forecast_end_date, creation_timestamp, model_date = self.dates()

        # Create main JSON keys
        mainkey = dict()
        if self.legend != "":
            mainkey["legends"] = self.legend
        if self.forecast_date != "":
            mainkey["forecast_date"] = forecast_date
        if self.colormap != "":
            mainkey["colormap"] = self.colormap
        if self.colorbar != "":
            mainkey["colorbar_url"] = self.colorbar
        if self.model_date != "":
            mainkey["model_date"] = model_date
        if self.colormap_long_pixels != "":
            mainkey["colormap_long_pixels"] = self.colormap_long_pixels

        # FOR MULTIPLE DEPTH
        # if images != "":
        #    mainkey["images"] = images
        if values != "":
            mainkey["values"] = values
        if image_url != "":
            mainkey["image_url"] = image_url
        if self.colormap_short_pixels != "":
            mainkey["colormap_short_pixels"] = self.colormap_short_pixels
        if self.bbox != "":
            mainkey["bbox"] = self.bbox
        if self.var != "":
            mainkey["var"] = self.var
        if self.forecast_end_date != "":
            mainkey["forecast_end_date"] = forecast_end_date
        if self.creation_timestamp != "":
            mainkey["creation_timestamp"] = creation_timestamp
        if self.forecast_start_date != "":
            mainkey["forecast_start_date"] = forecast_start_date
        return mainkey

    def getJSON(self):
        socat = []

        # Return min max of each depth in an array
        split = self.getMINMAX()
        print split
        for n in range(0, len(split)-1):
            image_url = os.path.join(self.base_url, "{0}_{1}.png".format(self.var,split[n][0]))
            values = {
                "min": "{}".format(split[n][1]),
                "max": "{}".format(split[n][2])
            }
            socat.append(self.create_json(image_url, values))

        #print socat

        f = open("{}.json".format(self.dataset), 'w')
        print json.dumps(socat, sort_keys=False, indent=4, separators=(',', ': '))
        f.write(json.dumps(socat, sort_keys=False, indent=4, separators=(',', ': ')))
        f.close()

    def dates(self):
        time_list = ['1964-12-31T12:00:00Z',
                     '1975-01-01T00:00:00Z',
                     '1984-12-31T12:00:00Z',
                     '1995-01-01T00:00:00Z',
                     '2004-12-31T12:00:00Z',
                     '2015-01-01T00:00:00Z']

        ts = time.time()

        creation_timestamp = calendar.timegm(time.gmtime())
        model_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')

        forecast_date = self.year[self.num - 1].replace('_', '-')
        forecast_start_date = time_list[self.num - 1]
        forecast_end_date = time_list[self.num]

        return forecast_date, forecast_start_date, forecast_end_date, creation_timestamp, model_date


def main():
    glodap_ds = ['arag_climatology','ph_climatology','tco2_climatology']
    for dataset in glodap_ds:
        #pth = "/media/lsetiawan/main/PycharmProjects/Global_Climatology/{}".format(dataset)
        pth = "./{}".format(dataset)
        p = [0, 10, 20, 30, 50, 75, 100, 125, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300,
             1400, 1500, 1750, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500]
        baseurl = "http://data.nanoos.org/files/goaon/mapoverlays/"
        year = ["7213"]

        # Set the min_max text, units, colors, and produce JSON
        if dataset == "arag_climatology":
            var = "aragonite"
            min_max ='arag_min_max_72_13.txt'
            units = 'Aragonite Saturation State'
            colormap = 'liqing'
            colorbar = os.path.join(baseurl,'arag_colorbar.png')
            tickmarks = [0, 1, 2, 3, 4, 5]
            MakeJSON(var, pth, min_max, baseurl, year, units, colormap, colorbar, p, tickmarks)
        elif dataset == "ph_climatology":
            var = "ph"
            min_max = 'ph_min_max_72_13.txt'
            units = 'pH'
            colormap = 'pH'
            colorbar = os.path.join(baseurl, 'ph_colorbar.png')
            tickmarks = [7.7, 7.8, 7.9, 8.0, 8.1, 8.2]
            MakeJSON(var, pth, min_max, baseurl, year, units, colormap, colorbar, p, tickmarks)
        elif dataset == "tco2_climatology":
            var = "tco2"
            min_max = 'tco2_min_max_72_13.txt'
            units = 'Dissolved Inorganic Carbon (μmol/kg)'
            colormap = 'tco2'
            colorbar = os.path.join(baseurl, 'tco2_colorbar.png')
            tickmarks = [1800, 1880, 1960, 2040, 2120, 2200]
            MakeJSON(var, pth, min_max, baseurl, year, units, colormap, colorbar, p, tickmarks)

    socat_ds = ['fco2_weighted_climatology', 'fco2_unwtd_climatology']

    for dataset in socat_ds:
        pth = './socat_decade/{}'.format(dataset)
        baseurl = "http://data.nanoos.org/files/goaon/mapoverlays/"
        year = ['1975_01_01', '1984_12_31', '1995_01_01', '2004_12_31', '2015_01_01']
        if dataset == "fco2_weighted_climatology":
            var = "fco2_weighted"
            min_max = './socat_decade/fco2_weighted_min_max.txt'
            units = 'fCO2 (μatm)'
            colormap = 'fco2'
            colorbar = os.path.join(baseurl, 'fco2_colorbar.png')
            tickmarks = [240, 288, 336, 384, 432, 480]
            socat = SocatJSON(var, pth, min_max, baseurl, year, units, colormap, colorbar, p=None, tickmarks=tickmarks)
            socat.getJSON()
        if dataset == "fco2_unwtd_climatology":
            var = "fco2_unwtd"
            min_max = './socat_decade/fco2_unwtd_min_max.txt'
            units = 'fCO2 (μatm)'
            colormap = 'fco2'
            colorbar = os.path.join(baseurl, 'fco2_colorbar.png')
            tickmarks = [240, 288, 336, 384, 432, 480]
            socat = SocatJSON(var, pth, min_max, baseurl, year, units, colormap, colorbar, p=None, tickmarks=tickmarks)
            socat.getJSON()


    ########################################################################################################
    ##### FOR MULTIPLE DEPTH ##################################################################################
    '''images = imagesURL(p,pth)
    for i in range(0,len(images)):
        legend = legends()
        year = ["8699","0013","7213"]
        forecast_date, forecast_start_date, forecast_end_date, creation_timestamp, model_date = dates(year[i])
        arag_climatology.append(create_json(forecast_date, model_date, images[i], forecast_end_date,
                                            creation_timestamp,forecast_start_date,legend))'''
    #######################################################################################################

if __name__ == '__main__':
    main()
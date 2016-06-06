#!/usr/bin/env python

from nc2png import global_climatology as gc

def main():
    pth = "/home/lsetiawan/Documents/GOA-ON/GLODAPv2.2016b_MappedClimatologies"
    #pth = "/Users/lsetiawan/Desktop/shared_ubuntu/GLODAPv2.2016b_MappedClimatologies"
    ds_names = ["GLODAPv2.2016b.TCO2.nc"]
    # pth =  raw_input("Where are your GLODAPv2_Mapped_Climatologies? [enter path] ")
    #ds_name = raw_input("Which dataset would you like to work on? [enter name of netCDF. eg. GLODAPv2.2016b.OmegaA.nc] ")

    #pth = "/Users/lsetiawan/Desktop/shared_ubuntu/APL/SOCAT"
    #ds_name = 'SOCAT_tracks_gridded_decades_v3.nc'

    for ds_name in ds_names:
        glodap = gc.Glodap(pth,ds_name)
        glodap.get_dataset()
        glodap.create_cmap()
        glodap.processData()

    #socat = Socat(pth,ds_name)
    #socat.processData()

if __name__ == '__main__':
    main()
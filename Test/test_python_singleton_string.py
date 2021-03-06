#!/usr/bin/env python

from test_python_common import *  # common subroutines

import cmor._cmor
import os

pth = os.path.split(os.path.realpath(os.curdir))
if pth[-1] == 'Test':
    ipth = opth = '.'
else:
    ipth = opth = 'Test'


myaxes = numpy.zeros(9, dtype='i')
myaxes2 = numpy.zeros(9, dtype='i')
myvars = numpy.zeros(9, dtype='i')


cmor.setup(
    inpath=ipth,
    set_verbosity=cmor.CMOR_NORMAL,
    netcdf_file_action=cmor.CMOR_REPLACE,
    exit_control=cmor.CMOR_EXIT_ON_MAJOR)
cmor.dataset_json("Test/CMOR_input_example.json")

tables = []
a = cmor.load_table("Tables/CMIP6_grids.json")
tables.append(a)

t = 'CMIP6_Omon.json'
te = 'dissic'
u = 'mol m-3'
time = 'time'
ts = 'month'
tscl = 1.

t = 'CMIP6_Lmon.json'
te = 'baresoilFrac'
u = ''
time = 'time'
ts = 'months'
tscl = 3.5e-4

tables.append(cmor.load_table("Tables/%s" % t))
print 'Tables ids:', tables

cmor.set_table(tables[0])

x, y, lon_coords, lat_coords, lon_vertices, lat_vertices = gen_irreg_grid(
    lon, lat)


myaxes[0] = cmor.axis(table_entry='y',
                      units='m',
                      coord_vals=y)
myaxes[1] = cmor.axis(table_entry='x',
                      units='m',
                      coord_vals=x)

grid_id = cmor.grid(axis_ids=myaxes[:2],
                    latitude=lat_coords,
                    longitude=lon_coords,
                    latitude_vertices=lat_vertices,
                    longitude_vertices=lon_vertices)
print 'got grid_id:', grid_id
myaxes[2] = grid_id

mapnm = 'lambert_conformal_conic'
params = ["standard_parallel1",
          "longitude_of_central_meridian", "latitude_of_projection_origin",
          "false_easting", "false_northing", "standard_parallel2"]
punits = ["", "", "", "", "", ""]
pvalues = [-20., 175., 13., 8., 0., 20.]
cmor.set_grid_mapping(grid_id=myaxes[2],
                      mapping_name=mapnm,
                      parameter_names=params,
                      parameter_values=pvalues,
                      parameter_units=punits)

cmor.set_table(tables[1])
myaxes[3] = cmor.axis(table_entry=time,
                      units='%s since 1980' % ts)

pass_axes = [myaxes[3], myaxes[2]]

myvars[0] = cmor.variable(table_entry=te,
                          units=u,
                          axis_ids=pass_axes,
                          history='no history',
                          comment='no future'
                          )

ntimes = 2
for i in range(ntimes):
    data2d = read_2d_input_files(i, varin2d[0], lat, lon) * 1.E-6
    print 'writing time: ', i, data2d.shape  # ,data2d
    print Time[i], bnds_time[2 * i:2 * i + 2]
    cmor.write(myvars[0], data2d, 1, time_vals=Time[i],
               time_bnds=bnds_time[2 * i:2 * i + 2])
    print 'wrote'
cmor.close()

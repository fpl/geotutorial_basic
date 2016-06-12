#!/usr/bin/env python
#
#   Copyright (C) 2013 Francesco P Lovergine <frankie@gisgeek.org>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#
#   This script creates a new layer of perpendicular transects starting from
#   a list of source vector of lines (streams), along with a points layer
#   of all middle and end points belonging to the transects. The only attribute
#   currently handled is the ID of the original linestring feature used
#   to build the transects. That could be possibly changed in a nearest
#   future.
#
#   Dependencies: 
#       OGR and Numpy
#

import os.path, sys, math, getopt

try:
    from osgeo import ogr
    from osgeo import osr
except ImportError:
    print 'Missing GDAL/OGR library bindings for Python'
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print 'Missing NumPy package'
    sys.exit(1)

__version__ = '0.1'

verbose = 0

# This is the machine epsilon
eps = np.spacing(1)

def usage(program):
    print '''
Usage: %s [--verbose=level|-v level] [--length=len|-l len] [--help|-h] 
          [--outdir=name|-o name] [--threshold=t|-t t] [--increment=incr|-i incr]
          [--format=format|-F format] [--force|-f] source_dsn ... 
''' % program

def middlepoint(one,two):
    '''Computes the median point between two 2D points'''
    mx = (one[0]+two[0])/2.0
    my = (one[1]+two[1])/2.0
    return [mx,my]

def slope(one,two):
    '''
    Computes the slope for the line associated to a pair of 2D points
    '''
    dx = (two[0]-one[0])
    dy = (two[1]-one[1])
    if np.abs(dx) < eps: return None
    return float(dy)/float(dx)

#
# Maybe we should use the Proj distance por non-projected coords?
#
def distance(one,two):
    '''
    Computes the cartesian distance of a pair of 2D points
    '''
    dx = float(two[0]-one[0])
    dy = float(two[1]-one[1])
    return math.sqrt(dy*dy+dx*dx)

def sqrdistance(one,two):
    '''
    Computes the cartesian distance of a pair of 2D points
    '''
    dx = float(two[0]-one[0])
    dy = float(two[1]-one[1])
    return dy**2+dx**2

def write_transect_lines(t, lyr, lid):
    '''
    Add transects lines with 3 vertexes to a pre-existing linestring layer.
    Note that the input list is a list of a list of [x,y] coords 
    
    '''
    for transect in t:
        line = ogr.Geometry(ogr.wkbLineString)
        for point in transect:
            line.AddPoint_2D(point[0],point[1])
        feature = ogr.Feature(lyr.GetLayerDefn())
        feature.SetGeometry(line)
        feature.SetField('orig_lid', int(lid))
        lyr.CreateFeature(feature)
        feature.Destroy()
        line.Destroy()
    
def write_transect_points(t, lyr, lid):
    '''
    Add vertexes of transects and intersection points to a pre-existing
    point cloud layer.
    Note that the input list is a list of a list of [x,y] coords, so
    an initial reduce comes useful.
    
    '''
    points = reduce(lambda x, y: x+y, t)
    for coord in points:
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint_2D(coord[0], coord[1])
        feature = ogr.Feature(lyr.GetLayerDefn())
        feature.SetGeometry(point)
        feature.SetField('orig_lid', int(lid))
        lyr.CreateFeature(feature)
        feature.Destroy()
        point.Destroy()

###############################################################################

def main(argv=None):

    global verbose

    if argv is None:
        argv = sys.argv

    if len(argv) <= 1:
        print 'No argument provided' 
        usage(argv[0])
        sys.exit(1)

    length = 100.0
    inc = 0.01
    th = None
    output_dir = ''
    output_format = 'ESRI Shapefile'
    output_ext = '.shp'
    force = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], \
                'i:v:l:ho:t:fF:',['verbose=','length=','help','outdir=', \
                'threshold=','format=','force','increment='])
    except getopt.GetoptError as err:
        print str(err)
        usage(argv[0])
        sys.exit(2)

    for o, a in opts:
        if o in ['-v', '--verbose']:
            try:
                verbose = int(a)
            except ValueError:
                print 'Verbosity level must be an integer'
                sys.exit(3)
        elif o in ['-l', '--length']:
            try:
                length = float(a)
            except ValueError:
                print 'Length must be a float'
                sys.exit(3)
        elif o in ['-o', '--outdir']:
            output_dir = a
            if not os.path.exists(a):
                os.makedirs(a)
        elif o in ['-F', '--format']:
            output_format = a
            output_ext = ''
        elif o in ['-f', '--force']:
            force = True
        elif o in ['-t', '--threshold']:
            try:
                th = float(a)
            except ValueError:
                print 'Threshold must be a float'
                sys.exit(3)
        elif o in ['-i', '--increment']:
            try:
                inc = float(a)
            except ValueError:
                print 'Increment must be a float'
                sys.exit(3)
        elif o in ['-h', '--help']:
            usage(argv[0])
            sys.exit(3)
        else:
            assert False, 'Unhandled option'

    if len(args) < 1:
        print 'No argument provided' 
        usage(argv[0])
        sys.exit(1)

    outdriver = ogr.GetDriverByName(output_format)
    if outdriver is None:
        print '%s driver not available' % output_format
        sys.exit(4)

    for name in args:
        dsn = ogr.Open(name, False)
        head, tail = os.path.split(name)
        name, ext = os.path.splitext(tail)
        indriver = dsn.GetDriver()
        if verbose>0:
            print 'Driver: ', indriver.GetName()
        layer = dsn.GetLayer()

        if verbose>0:
            print 'Number of feature to be considered: ', layer.GetFeatureCount()

        # FIXME: how to manage non projected cases?
        inspatialref = layer.GetSpatialRef()
        if not force:
            if inspatialref is None or not inspatialref.IsProjected():
                print 'SRS not defined or it is not a projection. Skipping %s, use --force to force' % name
                continue

        #
        # Warning! Never use original input spatialref for output!
        #
        outspatialref = inspatialref.Clone()
        outdsn = os.path.join(output_dir,name) + '_transects' + output_ext
        if verbose>0:
            print 'Ouput transects: %s' % outdsn
        if os.path.exists(outdsn):
            outdriver.DeleteDataSource(outdsn)
        dst_lines = outdriver.CreateDataSource(outdsn)
        lyr_lines = dst_lines.CreateLayer("lines", outspatialref, ogr.wkbLineString )

        outdsn = os.path.join(output_dir,name) + '_points' + output_ext
        if verbose>0:
            print 'Ouput points: %s' % outdsn
        if os.path.exists(outdsn):
            outdriver.DeleteDataSource(outdsn)
        dst_points = outdriver.CreateDataSource(outdsn)
        lyr_points = dst_points.CreateLayer("points", outspatialref, ogr.wkbPoint)

        if verbose>0:
            print 'Output layers created'

        field_def = ogr.FieldDefn("orig_lid", ogr.OFTInteger)
        lyr_lines.CreateField(field_def)
        field_def = ogr.FieldDefn("orig_lid", ogr.OFTInteger)
        lyr_points.CreateField(field_def)
        if verbose>0: 
            print 'Output attribute tables created'

        tn = 0
        lid = 0
        sqrlength = length**2
        for feature in layer:
            if verbose>0:
                print 'Feature #: ', lid
            geom = feature.GetGeometryRef()
            # should eventually manage multiline or collections?
            if geom.GetGeometryName() != 'LINESTRING':
                print 'Geometry is not appropriate to proceed, skipping layer'
                break
            n = geom.GetPointCount() 
            points = geom.GetPoints(2) 
            t = n - 1
            tn = tn + t
            if verbose>0:
                print 'Number of transects to build: ', t
            transects = []
            for i in range(1,n):
                curr = points[i]
                prev = points[i-1]
                xc, yc = middlepoint(curr, prev) 
                m = slope(prev, curr)
                dist = distance(curr, prev)
                if verbose>1:
                    print curr
                    print prev
                    print [xc, yc]
                    print 'Distance: ', dist, ' Slope: ', m
                if th is not None and dist < th:
                    continue
                if m is not None:
                    if verbose>1:
                        print 'Slope: ', m
                    if np.abs(m) > eps:
                        mm = - 1.0/float(m)
                        if verbose>1:
                            print 'Perp Slope: ', mm
                        #
                        # While a simple analytical eq could be used to get
                        # end points on the perpendiculare line, in practice
                        # it simply does not work because the numerical
                        # problem is very unstable. This is the best
                        # approximation to the problem of finding the solution 
                        # of the following easy geometrical problem: finding the two
                        # points at a certain distance from the intersection
                        # of a line with its perpedicular and lying on the perpedicular
                        # line itself.
                        #
                        bb = yc - mm * xc
                        x1 = xc
                        y1 = bb + mm*x1 
                        while True:
                            xx = x1+inc
                            yy = bb + mm*xx
                            if sqrdistance([xx,yy],[xc,yc])<sqrlength:
                                x1 = xx
                                y1 = yy
                                continue
                            else:
                                break
                        x2 = xc
                        y2 = bb + mm*x2 
                        while True:
                            xx = x2-inc
                            yy = bb + mm*xx
                            if sqrdistance([xx,yy],[xc,yc])<sqrlength:
                                x2 = xx
                                y2 = yy
                                continue
                            else:
                                break
                        assert sqrdistance([x1,y1],[x2,y2]) <= 4.0*sqrlength
                    else:
                        x1, x2 = xc - length, xc + length
                        y1 = y2 = yc
                else:
                    x1 = x2 = xc
                    y1, y2 = yc - length, yc + length

                transects.append([[x1,y1], [xc,yc], [x2,y2]])

            if verbose>1:
                print transects

            write_transect_lines(transects, lyr_lines, lid)
            write_transect_points(transects, lyr_points, lid)
            lid += 1
                
        if verbose>0:
            print 'Total number of transects: ', tn

        dst_lines.Destroy()
        dst_points.Destroy()

if __name__ == '__main__':
    sys.exit(main())

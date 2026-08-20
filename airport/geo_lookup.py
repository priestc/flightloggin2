"""
Point-in-polygon country/state lookup, replacing the old PostGIS-backed
WorldBorders/USStates models. Reads the same shapefiles that used to be
imported into those tables, and does the containment check in-process with
Shapely instead of a spatial database query.
"""

import os

import shapefile
from shapely.geometry import Point, shape

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

WORLD_SHP = os.path.join(DATA_DIR, 'world', 'TM_WORLD_BORDERS-0.3.shp')
STATES_SHP = os.path.join(DATA_DIR, 'states', 's_01au07.shp')

_world_polygons = None
_state_polygons = None


def _load_polygons(shp_path, code_field):
    """
    Returns a list of (code, shapely geometry) tuples from a shapefile,
    where code is the value of the given DBF field (e.g. 'ISO2', 'STATE').
    """
    reader = shapefile.Reader(shp_path)
    fields = [f[0] for f in reader.fields[1:]]  # skip the deletion flag field
    code_index = fields.index(code_field)

    polygons = []
    for sr in reader.shapeRecords():
        code = sr.record[code_index]
        geom = shape(sr.shape.__geo_interface__)
        polygons.append((code, geom))

    return polygons


def _get_world_polygons():
    global _world_polygons
    if _world_polygons is None:
        _world_polygons = _load_polygons(WORLD_SHP, 'ISO2')
    return _world_polygons


def _get_state_polygons():
    global _state_polygons
    if _state_polygons is None:
        _state_polygons = _load_polygons(STATES_SHP, 'STATE')
    return _state_polygons


def _find_containing(polygons, lat, lng):
    point = Point(lng, lat)
    for code, geom in polygons:
        if geom.contains(point):
            return code
    return None


def country_for_point(lat, lng):
    """Returns the ISO2 country code the given point falls in, or None."""
    return _find_containing(_get_world_polygons(), lat, lng)


def state_for_point(lat, lng):
    """Returns the US state code the given point falls in, or None."""
    return _find_containing(_get_state_polygons(), lat, lng)

from shapely import Polygon
import numpy as np
import geopandas as gpd
from shapely.ops import transform
from pyproj import Transformer, CRS

def convert_long(long_input):
    corrected_long = long_input - 180
    return corrected_long

def test_convert_long():
    in_out_expected = {
        360: 180,
        0: -180,
        150: -30,
    }
    in_out_actual = dict()

    for val in in_out_expected:
        actual_out = convert_long(val)
        in_out_actual[val] = actual_out
    
    assert in_out_actual == in_out_expected

def polygon_area(polygon, src_crs="EPSG:4326"):
    src_crs = CRS.from_user_input(src_crs)
    lon, lat = polygon.centroid.x, polygon.centroid.y
    zone_number = int((lon + 180) / 6) + 1
    is_northern = lat >= 0
    
    target_crs = CRS.from_dict({
        "proj": "utm",
        "zone": zone_number,
        "south": not is_northern
    })
    
    transformer = Transformer.from_crs(src_crs, target_crs, always_xy=True)
    projected_polygon = transform(transformer.transform, polygon)
    
    return projected_polygon.area

def test_polygon_area():
    test1_poly = Polygon((
        (-86.6438776698407, 34.734749149519885),
        (-86.63514227683883, 34.73453095062663),
        (-86.63527503357139, 34.72855207679599),
        (-86.64401042657326, 34.72866118420732)
    ))
    test2_poly = Polygon((
        (-94.82410003109636, 36.63909846215287), 
        (-94.69157744558204, 36.66278659355647),
        (-94.70325041943563, 36.623669715462306),
        (-94.64007903152208, 36.591149031108166),
        (-94.67235137099965, 36.552547386449646),
        (-94.73552275891322, 36.57681352976981),
        (-94.77328826255719, 36.549789387859505)
    ))

    in_out_expected = {
        test1_poly: 522000,
        test2_poly: 113550000
    }

    for poly, expected in in_out_expected.items():
        actual_out = polygon_area(poly)
        assert np.isclose(actual_out, expected, rtol=0.03)
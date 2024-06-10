# This code is based on:
# https://gist.github.com/c060604/8a51f8999be12fc2be498e9ca56adc72

import os
import piexif
from io import BytesIO as bio
from fractions import Fraction

def to_deg(value: float, loc: list) -> tuple:
    """
    Converts decimal coordinates into degrees, minutes and seconds tuple.

    :param value: GPS value
    :param loc: Direction list ["S", "N"] or ["W", "E"]
    :return: tuple like (25, 13, 48.343 ,'N')
    """
    if value < 0:
        loc_value = loc[0]
    elif value > 0:
        loc_value = loc[1]
    else:
        loc_value = ""
    abs_value = abs(value)
    deg = int(abs_value)
    t1 = (abs_value-deg)*60
    min = int(t1)
    sec = round((t1 - min)* 60, 5)
    return (deg, min, sec, loc_value)


def change_to_rational(number) -> tuple:
    """
    Converts a number to rational.

    :param number:
    :return: tuple like (1, 2), (numerator, denominator)
    """
    f = Fraction(str(number))
    return (f.numerator, f.denominator)


def with_gps_location(data: bytes, lat: float, lng: float, alt: float) -> bio:
    """
    Adds GPS degrees position as EXIF metadata.

    :param data: Image file data
    :param lat: Latitude
    :param lng: Longitude
    :param alt: Altitude
    :param output: Output buffer for the image with EXIF data.
    """
    lat_deg = to_deg(lat, ["S", "N"])
    lng_deg = to_deg(lng, ["W", "E"])

    exif_lat = (change_to_rational(lat_deg[0]), change_to_rational(lat_deg[1]), change_to_rational(lat_deg[2]))
    exif_lng = (change_to_rational(lng_deg[0]), change_to_rational(lng_deg[1]), change_to_rational(lng_deg[2]))

    gps_ifd = {
        piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
        piexif.GPSIFD.GPSAltitudeRef: 0,
        piexif.GPSIFD.GPSAltitude: change_to_rational(round(alt)),
        piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
        piexif.GPSIFD.GPSLatitude: exif_lat,
        piexif.GPSIFD.GPSLongitudeRef: lng_deg[3],
        piexif.GPSIFD.GPSLongitude: exif_lng,
    }

    exif_dict = {"GPS": gps_ifd}
    exif_bytes = piexif.dump(exif_dict)

    output: bio = bio()
    piexif.insert(exif_bytes, data, output)

    return output

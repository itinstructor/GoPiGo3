import pytest
from gps_api import position

test_msg = "$GPGGA,223315.000,3356.2748,S,01828.1605,E,2,10,0.80,26.5,M,32.6,M,0000,0000*42"

def test_position():
    p = position.Position()
    p.update(test_msg)
    assert p.get_latitude() == -33.937913333333334
    assert p.get_longitude() == 18.469341666666665
    assert p.get_altitude() == 26.5
    assert p.get_current_location() == (-33.937913333333334, 18.469341666666665)

# https://github.com/Knio/pynmea2
import pynmea2


class Position:
    """
    position class, used to store latitude, longitude and altitude.
    get_latitude, get_longitude and get_current_location methods
    """

    def __init__(self):
        # Initialization of variables
        self.latitude = ""
        self.longitude = ""
        self.altitude = ""
        self.location = ""
        self.time = ""
        self.date = ""
        self.speed = ""
        self.num_sats = ""

    def update(self, nmea_msg):
        """
        update the position's attributes with the NMEA message

        :param nmea_msg: The raw NMEA message to be parsed
        """
        if "GPGGA" in nmea_msg:
            msg = pynmea2.parse(nmea_msg)
            self.latitude = msg.latitude
            self.longitude = msg.longitude
            self.altitude = msg.altitude
            self.num_sats = msg.num_sats
        elif "GPRMC" in nmea_msg:
            msg = pynmea2.parse(nmea_msg)
            self.time = msg.timestamp
            self.date = msg.datestamp
        elif "GPVTG" in nmea_msg:
            msg = pynmea2.parse(nmea_msg)
            self.speed = msg.spd_over_grnd_kmph

    def get_num_sats(self)->str:
        """
        get number of satellites at current position

        return: current number of satellites as string
        """
        return self.num_sats

    def get_latitude(self)->str:
        """
        get latitude at current position

        return: current latitude value
        """
        return self.latitude

    def get_longitude(self)->str:
        """
        get longitude at current position

        return: current longitude value
        """
        return self.longitude

    def get_altitude(self)->str:
        """
        get altitude at current position

        return: current altitude value
        """
        return self.altitude

    def get_current_location(self)->str:
        """
        get location of current position

        return: current location in the form of (latitude, longitude)
        """
        location = (self.latitude, self.longitude)
        return location

    def get_UTC_time(self)->str:
        """
        get UTC time at current position

        return: current UTC time value
        """
        return self.time

    def get_date(self)->str:
        """
        get UTC date at current position

        return: current UTC date value
        """
        return self.date

    def get_speed(self)->str:
        """
        get current speed over ground

        return: current speed in km/h
        """
        return self.speed

"""
    Plane class
"""


class Plane:
    def __init__(self, cockpit_x, cockpit_y, orientation):
        """
        Initialization of an object of type "plane".
        :param cockpit_x: the horizontal coordinate of the cockpit on the board
        :param cockpit_y: the vertical coordinate of the cockpit on the board
        :param orientation: the orientation of the plane
        """
        self.__cockpit_x = cockpit_x
        self.__cockpit_y = cockpit_y
        self.__orientation = orientation

    @property
    def cockpit_x(self):
        return self.__cockpit_x

    @property
    def cockpit_y(self):
        return self.__cockpit_y

    @property
    def orientation(self):
        return self.__orientation

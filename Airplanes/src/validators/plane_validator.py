"""
    Plane validator class
"""

U = '\u001b[4m'  # Underline
N = '\u001b[0m'  # Reset
B = '\u001b[1m'  # Bold
G = '\u001b[32m'  # Green
R = '\u001b[31m'  # Red
Bl = '\033[94m'  # Blue
Y = '\u001b[33m'  # Yellow


class StoreException(Exception):
    pass


class PlaneOutOfBoundsException(StoreException):
    pass


class PlanesIntersectingException(StoreException):
    pass


class WrongOrientationException(StoreException):
    pass


class PlaneValidator:
    @staticmethod
    def plane_out_of_bounds(plane):
        """
        :param plane: the plane to be checked
        :return:
        """

        # Getting cockpit coordinates
        cockpit_x = plane.cockpit_x
        cockpit_y = plane.cockpit_y

        # If the cockpit exceeds the board bounds
        if cockpit_x < 1 or cockpit_x > 10 or cockpit_y < 0 or cockpit_y > 10:
            raise PlaneOutOfBoundsException(
                R + "The airplane that you are trying to place exceeds the board's bounds!" + N)

        # If the plane is placed pointing upwards
        if plane.orientation == "up":
            # If the wingspan of the plane exceeds the board bounds
            if cockpit_x - 2 < 1 or cockpit_x + 2 > 10:
                raise PlaneOutOfBoundsException(
                    R + "The airplane that you are trying to place exceeds the board's bounds!" + N)

            # If the plane's tail exceeds the board bounds
            if cockpit_y + 3 > 10:
                raise PlaneOutOfBoundsException(
                    R + "The airplane that you are trying to place exceeds the board's bounds!" + N)

        # If the plane is placed pointing downwards
        elif plane.orientation == "down":
            # If the wingspan of the plane exceeds the board bounds
            if cockpit_x - 2 < 1 or cockpit_x + 2 > 10:
                raise PlaneOutOfBoundsException(
                    R + "The airplane that you are trying to place exceeds the board's bounds!" + N)

            # If the plane's tail exceeds the board bounds
            if cockpit_y - 3 < 0:
                raise PlaneOutOfBoundsException(
                    R + "The airplane that you are trying to place exceeds the board's bounds!" + N)

        # If the plane is placed pointing towards the right
        elif plane.orientation == "right":
            # If the wingspan of the plane exceeds the board bounds
            if cockpit_y + 2 > 10 or cockpit_y - 2 < 0:
                raise PlaneOutOfBoundsException(
                    R + "The airplane that you are trying to place exceeds the board's bounds!" + N)

            # If the plane's tail exceeds the board bounds
            if cockpit_x - 3 < 1:
                raise PlaneOutOfBoundsException(
                    R + "The airplane that you are trying to place exceeds the board's bounds!" + N)

        # If the plane is placed pointing towards the left
        elif plane.orientation == "left":
            # If the wingspan of the plane exceeds the board bounds
            if cockpit_y + 2 > 10 or cockpit_y - 2 < 0:
                raise PlaneOutOfBoundsException(
                    R + "The airplane that you are trying to place exceeds the board's bounds!" + N)

            # If the plane's tail exceeds the board bounds
            if cockpit_x + 3 > 10:
                raise PlaneOutOfBoundsException(
                    R + "The airplane that you are trying to place exceeds the board's bounds!" + N)

    @staticmethod
    def plane_intersecting(board, plane):
        """
        Checks if a plane intersects another plane on the board.
        :param board: the current board
        :param plane: the plane to be checked
        :return:
        """
        try:
            # Getting cockpit coordinates
            cockpit_x = plane.cockpit_x
            cockpit_y = plane.cockpit_y

            # If the plane is placed pointing upwards
            if plane.orientation == "up":
                # Checking plane's tail
                for index in range(cockpit_y, cockpit_y + 4):
                    if board.board_is_marked(index, cockpit_x):
                        raise PlanesIntersectingException(R +
                                                          "The plane that you are trying to place will collide with another plane!" + N)

                # Checking plane's front wings
                for index in range(cockpit_x - 2, cockpit_x + 3):
                    if board.board_is_marked(cockpit_y + 1, index):
                        raise PlanesIntersectingException(R +
                                                          "The plane that you are trying to place will collide with another plane!" + N)

                # Checking plane's rear wings
                for index in range(cockpit_x - 1, cockpit_x + 2):
                    if board.board_is_marked(cockpit_y + 3, index):
                        raise PlanesIntersectingException(R +
                                                          "The plane that you are trying to place will collide with another plane!" + N)

            # If the plane is placed pointing downwards
            elif plane.orientation == "down":
                # Checking plane's tail
                for index in range(cockpit_y - 3, cockpit_y + 1):
                    if board.board_is_marked(index, cockpit_x):
                        raise PlanesIntersectingException(R +
                                                          "The plane that you are trying to place will collide with another plane!" + N)

                # Checking plane's front wings
                for index in range(cockpit_x - 2, cockpit_x + 3):
                    if board.board_is_marked(cockpit_y - 1, index):
                        raise PlanesIntersectingException(R +
                                                          "The plane that you are trying to place will collide with another plane!" + N)

                # Checking plane's rear wings
                for index in range(cockpit_x - 1, cockpit_x + 2):
                    if board.board_is_marked(cockpit_y - 3, index):
                        raise PlanesIntersectingException(R +
                                                          "The plane that you are trying to place will collide with another plane!" + N)

            # If the plane is placed pointing right
            elif plane.orientation == "right":
                # Checking plane's tail
                for index in range(cockpit_x - 3, cockpit_x + 1):
                    if board.board_is_marked(cockpit_y, index):
                        raise PlanesIntersectingException(R +
                                                          "The plane that you are trying to place will collide with another plane!" + N)

                # Checking plane's front wings
                for index in range(cockpit_y - 2, cockpit_y + 3):
                    if board.board_is_marked(index, cockpit_x - 1):
                        raise PlanesIntersectingException(R +
                                                          "The plane that you are trying to place will collide with another plane!" + N)

                # Checking plane's rear wings
                for index in range(cockpit_y - 1, cockpit_y + 2):
                    if board.board_is_marked(index, cockpit_x - 3):
                        raise PlanesIntersectingException(R +
                                                          "The plane that you are trying to place will collide with another plane!" + N)

            # If the plane is placed pointing left
            elif plane.orientation == "left":
                # Checking plane's tail
                for index in range(cockpit_x, cockpit_x + 4):
                    if board.board_is_marked(cockpit_y, index):
                        raise PlanesIntersectingException(R +
                                                          "The plane that you are trying to place will collide with another plane!" + N)

                # Checking plane's front wings
                for index in range(cockpit_y - 2, cockpit_y + 3):
                    if board.board_is_marked(index, cockpit_x + 1):
                        raise PlanesIntersectingException(R +
                                                          "The plane that you are trying to place will collide with another plane!" + N)

                # Checking plane's rear wings
                for index in range(cockpit_y - 1, cockpit_y + 2):
                    if board.board_is_marked(index, cockpit_x + 3):
                        raise PlanesIntersectingException(R +
                                                          "The plane that you are trying to place will collide with another plane!" + N)
        except IndexError:
            raise PlaneOutOfBoundsException

    @staticmethod
    def check_orientation(plane):
        if plane.orientation not in ["right", "up", "left", "down"]:
            raise WrongOrientationException(R + "The orientation that you have typed is of incorrect form!"
                                                " Orientation can only be: right, left, up, down." + N)

    def validate(self, board, plane):
        self.plane_out_of_bounds(plane)
        self.plane_intersecting(board, plane)
        self.check_orientation(plane)

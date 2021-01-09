"""
    Board Service module
"""

from model.plane import Plane
from prettytable import PrettyTable
import random

from validators.plane_validator import PlaneOutOfBoundsException, PlanesIntersectingException

U = '\u001b[4m'  # Underline
N = '\u001b[0m'  # Reset
B = '\u001b[1m'  # Bold
G = '\u001b[32m'  # Green
R = '\u001b[31m'  # Red
Bl = '\033[94m'  # Blue
Y = '\u001b[33m'  # Yellow


class BoardService:
    def __init__(self, board, validator):
        self.__validator = validator
        self.__board = board

        # Inserting column indexes, for when I need to
        # pass the board to a pretty table.
        self.insert_column_index()

    def get_board(self):
        """
        Gets board layout.
        :return:
        """
        return self.__board.get_board_info()

    def add_plane(self, cockpit_x, cockpit_y, orientation):
        """
        Adds a plane to the board
        :param cockpit_x:
        :param cockpit_y:
        :param orientation:
        :return:
        """

        cockpit_x = int(cockpit_x)
        cockpit_y = int(cockpit_y) - 1

        # Creating the plane with the corresponding information
        p = Plane(cockpit_x, cockpit_y, orientation)

        # Validating plane
        self.__validator.validate(self.__board, p)

        # Adding plane to the board

        self.__board.add_plane(p)
        plane_index = str(self.__board.get_plane_id())

        # If the plane is pointing upwards
        if orientation == "up":
            # Adding tail
            for index in range(cockpit_y, cockpit_y + 4):
                self.__board.mark_board(index, cockpit_x, plane_index)

            # Adding front wings
            for index in range(cockpit_x - 2, cockpit_x + 3):
                self.__board.mark_board(cockpit_y + 1, index, plane_index)

            # Adding rear wings
            for index in range(cockpit_x - 1, cockpit_x + 2):
                self.__board.mark_board(cockpit_y + 3, index, plane_index)

        # If the plane is pointing downwards
        elif orientation == "down":
            # Adding tail
            for index in range(cockpit_y, cockpit_y - 4, -1):
                self.__board.mark_board(index, cockpit_x, plane_index)

            # Adding front wings
            for index in range(cockpit_x - 2, cockpit_x + 3):
                self.__board.mark_board(cockpit_y - 1, index, plane_index)

            # Adding rear wings
            for index in range(cockpit_x - 1, cockpit_x + 2):
                self.__board.mark_board(cockpit_y - 3, index, plane_index)

        # If the plane is pointing towards the right
        elif orientation == "right":
            # Adding tail
            for index in range(cockpit_x - 3, cockpit_x + 1):
                self.__board.mark_board(cockpit_y, index, plane_index)

            # Adding front wings
            for index in range(cockpit_y - 2, cockpit_y + 3):
                self.__board.mark_board(index, cockpit_x - 1, plane_index)

            # Adding rear wings
            for index in range(cockpit_y - 1, cockpit_y + 2):
                self.__board.mark_board(index, cockpit_x - 3, plane_index)

        # If the plane is pointing towards the left
        elif orientation == "left":
            # Adding tail
            for index in range(cockpit_x, cockpit_x + 4):
                self.__board.mark_board(cockpit_y, index, plane_index)

            # Adding front wings
            for index in range(cockpit_y - 2, cockpit_y + 3):
                self.__board.mark_board(index, cockpit_x + 1, plane_index)

            # Adding rear wings
            for index in range(cockpit_y - 1, cockpit_y + 2):
                self.__board.mark_board(index, cockpit_x + 3, plane_index)

    def remove_plane_by_index(self, index):
        """
        Removes the plane with index = "index"
        :param index:
        :return:
        """

        # Removing the plane from the list of planes of the board
        plane_to_be_erased = self.__board.remove_plane_by_index(index)

        # Erasing the plane from the board

        orientation = plane_to_be_erased.orientation
        cockpit_x = plane_to_be_erased.cockpit_x
        cockpit_y = plane_to_be_erased.cockpit_y

        # If the plane is pointing upwards
        if orientation == "up":
            # Removing tail
            for index in range(cockpit_y, cockpit_y + 4):
                self.__board.unmark_board(index, cockpit_x)

            # Removing front wings
            for index in range(cockpit_x - 2, cockpit_x + 3):
                self.__board.unmark_board(cockpit_y + 1, index)

            # Removing rear wings
            for index in range(cockpit_x - 1, cockpit_x + 2):
                self.__board.unmark_board(cockpit_y + 3, index)

        # If the plane is pointing downwards
        elif orientation == "down":
            # Removing tail
            for index in range(cockpit_y, cockpit_y - 4, -1):
                self.__board.unmark_board(index, cockpit_x)

            # Removing front wings
            for index in range(cockpit_x - 2, cockpit_x + 3):
                self.__board.unmark_board(cockpit_y - 1, index)

            # Removing rear wings
            for index in range(cockpit_x - 1, cockpit_x + 2):
                self.__board.unmark_board(cockpit_y - 3, index)

        # If the plane is pointing towards the right
        elif orientation == "right":
            # Removing tail
            for index in range(cockpit_x - 3, cockpit_x + 1):
                self.__board.unmark_board(cockpit_y, index)

            # Removing front wings
            for index in range(cockpit_y - 2, cockpit_y + 3):
                self.__board.unmark_board(index, cockpit_x - 1)

            # Removing rear wings
            for index in range(cockpit_y - 1, cockpit_y + 2):
                self.__board.unmark_board(index, cockpit_x - 3)

        # If the plane is pointing towards the left
        elif orientation == "left":
            # Removing tail
            for index in range(cockpit_x, cockpit_x + 4):
                self.__board.unmark_board(cockpit_y, index)

            # Removing front wings
            for index in range(cockpit_y - 2, cockpit_y + 3):
                self.__board.unmark_board(index, cockpit_x + 1)

            # Removing rear wings
            for index in range(cockpit_y - 1, cockpit_y + 2):
                self.__board.unmark_board(index, cockpit_x + 3)

    @staticmethod
    def create_pretty_table(board_info):
        """
        Creates a pretty table corresponding to the board.
        :return: the pretty table
        """
        table = PrettyTable()

        table.field_names = [G + '', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10' + N]

        # Adding information to the table.
        table.add_rows(board_info)

        return table

    def insert_column_index(self):
        # Preparing the information for table insertion.
        board_info = self.get_board()
        index = '1'

        # For each row, insert its index on the first position,
        # so that in the end, I get a table with 2 coordinates:
        # a vertical one, and a horizontal one.
        for element in board_info:
            element.insert(0, G + index + N)
            index = str(int(index) + 1)

    @staticmethod
    def insert_column_index_by_info(board_info):
        # Preparing the information for table insertion.
        index = '1'

        # For each row, insert its index on the first position,
        # so that in the end, I get a table with 2 coordinates:
        # a vertical one, and a horizontal one.
        for element in board_info:
            element.insert(0, G + index + N)
            index = str(int(index) + 1)

    def place_random_planes(self):
        """
        Places random planes on the board until there are 3 planes.
        :return:
        """

        # List of orientations, so I can pick randomly from it
        orientations = ["up", "down", "left", "right"]

        # While there are less than 3 airplanes on the board.
        while len(self.__board.get_planes()) != 3:

            # Generating random airplane
            cockpit_x = random.randint(3, 8)
            cockpit_y = random.randint(3, 8)

            orientation_index = random.randint(0, 3)
            orientation = orientations[orientation_index]

            # print("cockpit_x: " + str(cockpit_x))
            # print("cockpit_y: " + str(cockpit_y))
            # print("orientation: " + orientation)

            try:
                self.add_plane(cockpit_x, cockpit_y, orientation)
            except PlaneOutOfBoundsException:
                pass
            except PlanesIntersectingException:
                pass

            # self.create_pretty_table()

    def get_number_of_planes(self):
        """
        :return: the number of planes on the board
        """
        return len(self.__board.get_planes())

    def fire_upon_location(self, x, y, blind_board_info):
        """
        Simulates firing upon the location indicated by coordinates x and y.
        :param x:
        :param y:
        :param blind_board_info:
        :return: True if a plane was hit, False if the shot missed, or -1 if the location has already been fired upon.
        """
        x = int(x)
        y = int(y) - 1

        # print("x:", x)
        # print("y:", y)

        if blind_board_info[y][x] != 0:
            print(R + "Commander, ou have already fired at that location! Fire elsewhere!" + N)
            return -1

        if self.__board.board_is_marked(y, x):
            blind_board_info[y][x] = Bl + 'X' + N
            return True

        blind_board_info[y][x] = R + 'X' + N
        return False

    @staticmethod
    def generate_random_shot(blind_board_info):
        """
        :return: Random coordinates for the computer to fire upon
        """

        x = random.randint(1, 10)
        y = random.randint(1, 10)

        while blind_board_info[y - 1][x] != 0:
            x = random.randint(1, 10)
            y = random.randint(1, 10)

        return str(x), str(y)

"""
    Board class
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


class BoardException(StoreException):
    pass


class Board:
    def __init__(self):
        """
        Initialization of an object of type "board".
        Boards have a fixed size of 10x10 squares, and are represented
        in memory by lists of lists.
        """
        self.__board = [[0] * 10 for x in range(10)]
        self.__plane_id = 0
        self.__dict_planes = {}

    def get_board_info(self):
        """
        :return: the list of lists containing the board information
        """
        return self.__board

    def board_is_marked(self, x, y):
        """
        :return: True if there is a plane at the position specified, False otherwise.
        """
        return not self.__board[x][y] == 0

    def mark_board(self, x, y, index):
        """
        Marks the board at the position with coordinates x and y
        with the character "index".
        :param x:
        :param y:
        :param index:
        :return:
        """
        self.__board[x][y] = Bl + index + N

    def unmark_board(self, x, y):
        """
        Unmarks the board at the position with coordinates x and y.
        :param x:
        :param y:
        :return:
        """
        self.__board[x][y] = 0

    def add_plane(self, plane):
        """
        Adds a plane to the list of planes on the board.
        :param plane:
        :return:
        """
        self.__plane_id += 1
        self.__dict_planes[self.__plane_id] = plane

    def remove_plane_by_index(self, index):
        """
        Removes the plane with index "index" from the list of planes
        :return: the removed plane
        """
        if index > len(self.__dict_planes) or index < 1:
            raise BoardException(R + "The plane that you are trying to remove does not exist." + N)

        return self.__dict_planes.pop(index)

    def get_planes(self):
        """
        :return: A list of all the planes on the board
        """
        return self.__dict_planes.values()

    def get_plane_id(self):
        return self.__plane_id

    def location_is_fired_upon(self, x, y):
        """

        :param x:
        :param y:
        :return:
        """
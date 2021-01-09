"""
    Console class
"""

# Font formatting
from model.board import BoardException
from validators.plane_validator import PlaneOutOfBoundsException, PlanesIntersectingException, WrongOrientationException

U = '\u001b[4m'  # Underline
N = '\u001b[0m'  # Reset
B = '\u001b[1m'  # Bold
G = '\u001b[32m'  # Green
R = '\u001b[31m'  # Red
Bl = '\033[94m'  # Blue
Y = '\u001b[33m'  # Yellow


#


class Console:
    def __init__(self, human_board_service, computer_board_service):
        """
        Initialization of the console.
        It receives the services of the boards of the 2 players playing the game.
        :param human_board_service:
        :param computer_board_service:
        """
        self.__board_human_service = human_board_service
        self.__board_computer_service = computer_board_service

    def run_console(self):
        while True:
            self.print_menu()
            cmd = input("Command: ")

            # Acting upon user input
            if cmd == "P" or cmd == "p":
                # Printing tips
                self.print_tips()

                # PLACING PLANES

                # Human placing planes
                # Asking question about placing the planes
                self.print_question()
                user_placing_planes = self.get_correct_input("Answer: ")

                # If the user wants to place the planes manually
                if user_placing_planes == "Y" or user_placing_planes == "y":
                    # Printing board
                    self.print_human_board()

                    # Adding planes until there are three on the board
                    self.place_until_three()

                # If the user wants the planes to be randomly placed.
                elif user_placing_planes == "N" or user_placing_planes == "n":
                    self.__board_human_service.place_random_planes()
                    print(Y + "This is your board!" + N)
                    self.print_human_board()

                # Allowing user to rearrange board
                print(Y + "If you want to rearrange your board, you can do so!" + N)

                user_rearranging_board = self.get_correct_input(Y + "Would you like to"
                                                                    " rearrange your board? (Y/N)\n" + N)

                # If the answer is yes, rearranging...
                if user_rearranging_board == "Y" or user_rearranging_board == "y":
                    print("\n" + Bl + "In order to rearrange the board, you will do the following: \n"
                                      "type the index of the plane that you want to remove in order to remove\n"
                                      "the plane with that index "
                                      "(you can remove planes as long as there are planes on the board).\n"
                                      "After removing the planes that you don't like, you will have to add new ones\n"
                                      "manually, until you have a total of three planes on your board.\n"
                                      "In order to start adding planes, type \"add\".\n"
                                      "Think carefully!\n" + N)

                    # Getting input and executing command
                    rearrange_input = None
                    while rearrange_input != "add" and self.__board_human_service.get_number_of_planes() != 0:
                        rearrange_input = self.get_rearrange_input()
                        if rearrange_input.isdigit():
                            try:
                                self.__board_human_service.remove_plane_by_index(int(rearrange_input))
                            except BoardException as ex:
                                print(str(ex))
                        self.print_human_board()

                    # When user is done removing, add planes
                    self.place_until_three()

                # Computer placing planes
                print("\nThe computer is deploying aircrafts...")
                self.__board_computer_service.place_random_planes()
                print("Done!\n")
                # self.print_computer_board()
                # COMMENCING BATTLE

                # # Deciding who shoots first
                # human_shoots_first = self.get_correct_input(Y + "Would you like to shoot first? (Y/N): " + N)
                # print("\n")
                print(Y + B + U + "LET THE BATTLE BEGIN!\n" + N)

                # Initializing blind board for human and computer to display their fire.
                human_blind_board_info = [[0] * 10 for x in range(10)]
                computer_blind_board_info = [[0] * 10 for x in range(10)]

                self.__board_human_service.insert_column_index_by_info(human_blind_board_info)
                self.__board_human_service.insert_column_index_by_info(computer_blind_board_info)

                human_hits = 0
                computer_hits = 0

                # While the game is not over (there still is a position to hit)
                while human_hits != 30 and computer_hits != 30:
                    # If human shoots first

                    # Human firing
                    x, y = self.get_fire_input()
                    # x, y = self.__board_computer_service.generate_random_shot(computer_blind_board_info)
                    hit = self.__board_computer_service.fire_upon_location(x, y, computer_blind_board_info)

                    # If human hits, he gets another shot
                    while hit is True or hit == -1:
                        # If human hits
                        if hit is True:
                            human_hits += 1
                            print(Y + "Great shot! You hit an enemy plane!" + N)

                        #
                        print("Hits: " + str(human_hits))
                        self.print_board_by_info(computer_blind_board_info)

                        if human_hits < 30:
                            x, y = self.get_fire_input()
                            # x, y = self.__board_computer_service.generate_random_shot(computer_blind_board_info)
                            hit = self.__board_computer_service.fire_upon_location(x, y, computer_blind_board_info)

                        if human_hits == 30:
                            print(Y + "Congratulations! You destroyed all of the enemies' aircrafts!" + N)
                            return

                    # If human missed
                    if hit is False:
                        print(Y + "You missed! You'll get them next time!" + N)
                        self.print_board_by_info(computer_blind_board_info)

                    # Computer firing

                    print(Bl + "The enemies are aiming their shot..." + N)
                    print(Bl + "Fire!" + N)
                    x, y = self.__board_computer_service.generate_random_shot(human_blind_board_info)
                    hit = self.__board_human_service.fire_upon_location(x, y, human_blind_board_info)

                    # If computer hits, he gets another shot
                    while hit is True or hit == -1:
                        # If computer hits
                        if hit is True:
                            computer_hits += 1
                            print(Bl + "The enemies hit!" + N)

                        #
                        print("Hits: " + str(computer_hits))
                        self.print_board_by_info(human_blind_board_info)

                        if computer_hits < 30:
                            x, y = self.__board_computer_service.generate_random_shot(human_blind_board_info)
                            hit = self.__board_human_service.fire_upon_location(x, y, human_blind_board_info)

                        if computer_hits == 30:
                            print(Bl + "The enemies destroyed all of our aircrafts!" + N)
                            return

                    # If computer missed
                    if hit is False:
                        print(Bl + "The enemies missed!" + N)
                        self.print_board_by_info(human_blind_board_info)

            elif cmd == "X" or cmd == 'x':
                return

    def place_until_three(self):
        # Getting input and placing aircrafts on the board until there are 3.
        while self.__board_human_service.get_number_of_planes() != 3:
            x, y, orientation = self.get_add_plane_input()

            try:
                self.__board_human_service.add_plane(x, y, orientation)
            except PlaneOutOfBoundsException as ex:
                print(str(ex))
            except PlanesIntersectingException as ex:
                print(str(ex))
            except WrongOrientationException as ex:
                print(str(ex))

            self.print_human_board()
        print("\n")
        print(Y + "This is your board!" + N)
        self.print_human_board()

    @staticmethod
    def get_add_plane_input():
        x = input("Type the X coordinate of the plane's cockpit: ")
        y = input("Type the Y coordinate of the plane's cockpit: ")
        orientation = input("Type the orientation of the plane: ")
        return x, y, orientation

    @staticmethod
    def print_menu():
        print("1.) " + Y + "P" + N + " - Play\n"
                                     "2.) " + R + "X" + N + " - Exit")

    @staticmethod
    def print_tips():
        print(G + "You will need to deploy 3 aircrafts before commencing the battle!\n"
                  "In order to do this, you will choose the location of each of the\n"
                  "planes' cockpits on the board, as well as their orientation (up, down left, right)\n"
                  "Tip: try to place the airplanes in a formation that is as confusing as possible!" + N)

    @staticmethod
    def print_question():
        print(Y + "Would you like to place the airplanes yourself? (Y/N)\nIf you answer \"N\", your planes"
                  " will be placed randomly." + N)

    @staticmethod
    def get_correct_input(message):
        correct_input = False
        answer = None

        while correct_input is False:
            answer = input(message)

            if answer in "YNyn":
                correct_input = True
            else:
                print(R + "The answer you have typed is of incorrect form.\nAccepted answers are Y, y, N, n." + N)

        return answer

    @staticmethod
    def get_rearrange_input():
        correct_input = False
        answer = None

        while correct_input is False:
            answer = input(Bl + "Index: " + N)

            if answer.isdigit() is True or answer == "add":
                correct_input = True
            else:
                print(
                    R + "The answer you have typed is of incorrect form.\nAccepted answers are \"add\" or an integer." + N)

        return answer

    @staticmethod
    def get_fire_input():
        print(Y + "Aim your shot!" + N)

        correct_input = False
        x, y = None, None

        while correct_input is False:
            x = input(Y + "Type the X coordinate of where you want to shoot: " + N)
            y = input(Y + "Type the Y coordinate of where you want to shoot: " + N)

            if x.isdigit() and y.isdigit() and 1 <= int(x) <= 10 and 1 <= int(y) <= 10:
                correct_input = True
            else:
                print(
                    R + "You did not type an integer, or the location you indicate to is out of the board's bounds!" + N)

        return x, y

    def print_human_board(self):
        board_info = self.__board_human_service.get_board()
        print(self.__board_human_service.create_pretty_table(board_info))

    def print_computer_board(self):
        board_info = self.__board_computer_service.get_board()
        print(self.__board_computer_service.create_pretty_table(board_info))

    def print_board_by_info(self, board_info):
        print(self.__board_human_service.create_pretty_table(board_info))

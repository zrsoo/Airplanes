"""
    Control module
"""
import traceback

from controller.board_service import BoardService
from model.board import Board
from validators.plane_validator import PlaneValidator
from view.console import Console

if __name__ == "__main__":
    try:
        human_board = Board()
        computer_board = Board()

        plane_validator = PlaneValidator()

        human_board_service = BoardService(human_board, plane_validator)
        computer_board_service = BoardService(computer_board, plane_validator)

        console = Console(human_board_service, computer_board_service)
        console.run_console()
    except Exception as ex:
        print("Error: " + str(ex))
        traceback.print_exc()

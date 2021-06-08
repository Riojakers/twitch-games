from rusthour.game_board import GameBoard
from rusthour.gui import Board
import asyncio
from api.chat import CommandChat

game = GameBoard("1-1")
board = Board(game)


def on_move_event(color, direction):
    print(color)
    print(direction)


async def run_chat():
    CommandChat(on_move_event=on_move_event, debug=False)


async def run_gui():
    board.draw()


asyncio.get_event_loop().run_until_complete(run_chat())
asyncio.get_event_loop().run_until_complete(run_gui())

from game.constants import Color
from game.piece import Piece


class Player:
    def __init__(self, color: Color):
        self.__pieces = [Piece(color) for _ in range(8)]
        self.__color = color
        self.__won = False
    
    def __str__(self) -> str:
        return "Azul" if self.__color == Color.BLUE else "Vermelho"

    def get_color(self) -> Color:
        return self.__color

    def place_piece(self) -> Piece:
        if self.has_pieces():
            return self.__pieces.pop()
        return None

    def take_piece(self, piece: Piece):
        self.__pieces.append(piece)

    def has_pieces(self) -> bool:
        return len(self.__pieces) > 0

    def get_piece_count(self) -> int:
        return len(self.__pieces)

    def set_win(self) -> None:
        self.__won = True

    def has_won(self) -> bool:
        return self.__won
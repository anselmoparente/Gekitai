from game.constants import DIRECTIONS, Color, Status

from game.piece import Piece
from game.player import Player


class Cell:
    def __init__(self):
        self.__piece = None

    def place_piece(self, piece: Piece) -> None:
        self.__piece = piece

    def remove_piece(self) -> Piece:
        piece = self.__piece
        self.__piece = None
        return piece

    def is_occupied(self) -> bool:
        return self.__piece is not None

    def is_empty(self) -> bool:
        return self.__piece is None

    def get_piece(self) -> Piece:
        return self.__piece


class Board:
    def __init__(self):
        self.__cells: list[list[Cell]]
        self.__players: list[Player]
        self.__status: Status
        self.__current_player: Player
        self.__winner: Player

        self.initialize()

    def get_status(self) -> Status:
        return self.__status

    def get_winner(self) -> Player:
        return self.__winner

    def click(self, position: tuple[int, int]) -> None:
        if self.__status == Status.NO_MATCH:
            self.__status = Status.IN_PROGRESS
        elif self.__status == Status.IN_PROGRESS:
            self.place_piece(position)
        elif self.__status == Status.FINISHED:
            self.initialize()

    def initialize(self) -> None:
        self.__cells = [[Cell() for _ in range(6)] for _ in range(6)]
        self.__players = [Player(Color.RED), Player(Color.BLUE)]
        self.__status = Status.NO_MATCH
        self.__current_player = self.__players[0]
        self.__winner = None

    def current_player(self) -> Player:
        return self.__current_player

    def flip_players(self) -> None:
        for player in self.__players:
            if player.get_color() != self.__current_player.get_color():
                self.__current_player = player
                return

    def get_player(self, color: Color) -> Player:
        for player in self.__players:
            if player.get_color() == color:
                return player

    def get_cell(self, position: tuple[int, int]) -> Cell:
        if self.position_valid(position):
            return self.__cells[position[0]][position[1]]
        return None

    def position_valid(self, position: tuple[int, int]) -> bool:
        return 0 <= position[0] < 6 and 0 <= position[1] < 6

    def move_piece(self, source: Cell, destination: Cell) -> None:
        if destination.is_empty():
            piece = source.remove_piece()
            destination.place_piece(piece)

    def remove_piece(self, cell: Cell) -> None:
        piece = cell.remove_piece()
        owner = self.get_player(piece.get_color())
        owner.take_piece(piece)

    def check_alignment(self, position: tuple[int, int]) -> bool:
        x, y = position

        cell = self.get_cell((x, y))
        if cell.is_empty():
            return False
        color = cell.get_piece().get_color()

        for (i, j) in [(1,1), (0,1), (1,0), (1,-1)]:
            neighbor = (x+i, y+j)
            if not self.position_valid(neighbor):
                continue
            cell = self.get_cell(neighbor)
            if cell.is_empty():
                continue
            if color != cell.get_piece().get_color():
                continue

            neighbor = (x-i, y-j)
            if not self.position_valid(neighbor):
                continue
            cell = self.get_cell(neighbor)
            if cell.is_empty():
                continue
            if color != cell.get_piece().get_color():
                continue

            return True
        return False

    def check_match_end(self) -> bool:
        match_end = False

        for player in self.__players:
            if not player.has_pieces():
                player.set_win()
                match_end = True

        for x in range(6):
            for y in range(6):
                if self.check_alignment((x, y)):
                    color = self.get_cell((x, y)).get_piece().get_color()
                    player = self.get_player(color)
                    player.set_win()
                    match_end = True

        return match_end

    def finish_match(self) -> None:
        self.__status = Status.FINISHED

        player1, player2 = self.__players
        if player1.has_won() == player2.has_won():
            self.__winner = None
        else:
            self.__winner = player1 if player1.has_won() else player2

    def end_turn(self) -> None:
        if self.check_match_end():
            self.finish_match()
        else:
            self.flip_players()

    def place_piece(self, position: tuple[int, int]) -> None:
        if self.position_valid(position):
            cell = self.get_cell(position)
            if cell.is_occupied():
                return
        else:
            return

        player = self.current_player()
        piece = player.place_piece()
        cell.place_piece(piece)

        self.push_neighbors(position)
        self.end_turn()

    def push_neighbors(self, position: tuple[int, int]) -> None:
        for direction in DIRECTIONS:
            neighbor_position = (position[0] + direction[0], position[1] + direction[1])
            if self.position_valid(neighbor_position):
                neighbor = self.get_cell(neighbor_position)
                if neighbor.is_empty():
                    continue
            else:
                continue

            push_position = (neighbor_position[0] + direction[0], neighbor_position[1] + direction[1])
            if self.position_valid(push_position):
                push = self.get_cell(push_position)
                self.move_piece(neighbor, push)
            else:
                self.remove_piece(neighbor)

import sys

import pygame as pg

from game.board import Board
from game.constants import FRAMERATE, RESOLUTION, Color, Status
from game.client import Client
import threading
import socket
import pickle


class Interface:
    def __init__(self):
        pg.init()

        HOST = 'localhost'
        PORT = 9000

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

        self.__sock = sock

        thread = threading.Thread(target=self.handle_server)
        thread.start()

        self.__screen = pg.display.set_mode(RESOLUTION, pg.RESIZABLE | pg.HWSURFACE | pg.DOUBLEBUF | pg.SCALED, 32)
        self.__board = Board()
        self.__clock = pg.time.Clock()
        self.__playerColor = ''
        self.__yourTurn = ''
        self.draw()
        self.run()

    def handle_server(self):
        while True:
            message = self.__sock.recv(1024)
            try:
                message = message.decode('utf-8')
            except:
                message = pickle.loads(message)

            if (message[1] != False):
                position = (message[1] // 64, (message[2] - 50) // 64)
                if position != None:
                    self.__yourTurn = True
                    self.__board.click(position)
                    self.draw()
            else:
                self.__playerColor = message[0]
                if (self.__playerColor == 'red'):
                    self.__yourTurn = True
                elif (self.__playerColor == 'blue'):
                    self.__yourTurn = False

    def run(self) -> None:
        while True:
            self.__clock.tick(FRAMERATE)
            self.loop()
            pg.display.update()

    def write_text(self, text: str, position: tuple[int, int]) -> None:
        font = pg.font.Font(None, 32)
        surface = font.render(text, False, (0, 0, 0))
        self.__screen.blit(
            surface,
            (position[0] - (surface.get_width() // 2), position[1] - (surface.get_height() // 2))
        )

    def draw(self):
        self.__screen.fill((255, 255, 255))

        cell_image = pg.image.load("assets/cell.png")
        red_piece = pg.image.load("assets/vermelho.png")
        blue_piece = pg.image.load("assets/azul.png")
        logo = pg.image.load("assets/logo.png")
        
        pg.draw.rect(self.__screen, (0,0,0),pg.Rect(384 + 50, 0, 500, 400), 1)

        pg.draw.rect(self.__screen, (255,0,0),pg.Rect(384 + 200, 405, 200, 95))
        self.write_text("Desistir", (684, 450))

        self.__screen.blit(logo, (0, 0))
        self.__screen.blit(red_piece, (0, 384 + 50))
        self.__screen.blit(blue_piece, (384 - 64, 384 + 50))

        self.__screen.blit

        red = self.__board.get_player(Color.RED)
        blue = self.__board.get_player(Color.BLUE)

        self.write_text(str(red.get_piece_count()), (64, 448))
        self.write_text(str(blue.get_piece_count()), (384 - 64, 448))

        if self.__board.get_status() == Status.NO_MATCH:
            self.write_text("Clique para iniciar a partida", (self.__screen.get_width() // 5, 516))
        elif self.__board.get_status() == Status.FINISHED:
            winner = self.__board.get_winner()
            if winner is not None:
                self.write_text(f"Vencedor: {winner}", (self.__screen.get_width() // 5, 516))
            else:
                self.write_text("Empate!", (self.__screen.get_width() // 5, 516))
        elif self.__board.get_status() == Status.IN_PROGRESS:
            turn = self.__board.current_player()
            self.write_text(f"Vez do {turn}", (self.__screen.get_width() // 5, 516))

        for x in range(6):
            for y in range(6):
                self.__screen.blit(cell_image, (x * 64, y * 64 + 50))
                cell = self.__board.get_cell((x, y))
                if cell.is_occupied():
                    piece = cell.get_piece()
                    self.__screen.blit(
                        red_piece if piece.get_color() == Color.RED else blue_piece,
                        (x * 64, y * 64 + 50),
                    )

    def loop(self):
        if (position := self.get_input()) != None:
            self.__board.click(position)
            self.draw()

    def get_input(self) -> tuple[int, int]:
        for event in pg.event.get():
            if (event.type == pg.MOUSEBUTTONDOWN):
                if (self.__board.get_status() == Status.NO_MATCH):
                    i, j = pg.mouse.get_pos()
                    if ((584 < i < 784)  and (405 < j < 500)):
                        self.__board.finish_match()
                    print('i:' + str(i))
                    print('j:' + str(j))
                    position = (i // 64, (j - 50) // 64)
                    self.__yourTurn = True
                    return position
                else:
                    if (self.__yourTurn):
                        i, j = pg.mouse.get_pos()
                        if ((584 < i < 784)  and (405 < j < 500)):
                            self.__board.finish_match()
                        print('i:' + str(i))
                        print('j:' + str(j))
                        mensagem = pickle.dumps([False, i, j])
                        self.__sock.sendall(mensagem)
                        position = (i // 64, (j - 50) // 64)
                        self.__yourTurn = False
                        return position

            if event.type == pg.QUIT:
                self.__sock.close()
                pg.quit()
                sys.exit()
import pygame as pg

class Paddle:
    def __init__(self, x, y, net=None):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 100
        self.color = (255, 255, 255)
        self.speed = 15
        self.net = net

    def draw(self, w):
        pg.draw.rect(w, self.color, (self.x, self.y, self.width, self.height))

    def move(self, up, game):
        if up and not self.y < 0:
            self.y -= self.speed
        elif not self.y > game.height - self.height:
            self.y += self.speed

    def ai_handle(self, d, game):
        if d == 0:
            self.move(True, game)
        elif d == 1:
            pass
        elif d == 2:
            self.move(False, game)

    def handle_paddle_movement(self, keys, game):
        if keys[pg.K_w]:
            self.move(True, game)
        if keys[pg.K_s]:
            self.move(False, game)

    def movement_handle(self, option, game, keys):
        if option == 1:
            self.handle_paddle_movement(keys, game)

        elif option == 2:
            output = self.net.activate((self.y,
                                    game.ball.y,
                                    abs(game.ball.x - self.x)))
            decision = output.index(max(output))
            self.ai_handle(decision, game)


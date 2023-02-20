import pygame as pg
import random
class Ball:
    def __init__(self, x, y, radius, x_vel=7, y_vel=random.randint(-7, 7)):
        self.MAX_VEL = 15 
        self.x = x
        self.y = y
        self.r = radius

        self.x_vel = int(random.choice([x_vel, - x_vel]))
        self.y_vel = y_vel 
        self.color = (255, 255, 255)

    def draw(self, w):
        pg.draw.rect(w, self.color , (self.x, self.y, self.r, self.r))

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def handle_collision(self, left_paddle, right_paddle, game):
        if self.y + self.r//2 < 0 or self.y + self.r//2 >= game.height:
            self.y_vel *= -1
        
        if self.x_vel < 0:
            if self.y >= left_paddle.y and self.y <= left_paddle.y + left_paddle.height:
                if self.x - self.r<= left_paddle.x + left_paddle.width:
                    self.collide(left_paddle)
                    game.left_hits += 1
        else:
            if self.y >= right_paddle.y and self.y  <= right_paddle.y + right_paddle.height:
                if self.x + self.r >= right_paddle.x:
                    self.collide(right_paddle)
                    game.right_hits += 1

    def collide(self, paddle):
        self.x_vel *= -1.05 if abs(self.x_vel) < self.MAX_VEL else -1
        middle_y = paddle.y + paddle.height /2
        dy = middle_y - self.y
        reduct = (paddle.height/2)//abs(self.x_vel)
        self.y_vel = dy//reduct if self.y_vel < 0 else - dy//reduct
        if random.randint(-10, 10) == 1:
            self.y_vel += 1




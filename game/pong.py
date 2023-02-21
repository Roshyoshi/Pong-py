from .paddle import *
from .ball import *
import pygame as pg
from time import sleep 
import neat
class PongGame:
    def __init__(self, width, height):
        pg.display.set_caption("AI Pong")
        pg.font.init()
        self.height = height
        self.width = width
        self.run = True
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("comicsans", 50)            
    
    def ai_game(self, genome, config, l_option=1, r_option=2):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.ball = Ball(self.height//2, self.width//2, 15)
        self.left_paddle = Paddle(10, self.height//2 - 50, net)
        self.right_paddle = Paddle(self.width - 30, self.width//2 - 50, net)

        self.w = pg.display.set_mode((self.width, self.height))
        left_score = 0
        right_score = 0
        self.right_hits = 0
        self.left_hits = 0

        while self.run:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print("Thanks for playing!")
                    self.run = False
                    break
            keys = pg.key.get_pressed()

            self.left_paddle.movement_handle(l_option, self, keys)
            self.right_paddle.movement_handle(r_option, self, keys)     
            
            
            self.ball.handle_collision(self.left_paddle, 
                                       self.right_paddle, self)
            
            self.ball.move()

            if self.ball.x < 0:
                left_score += 1
                self.ball = Ball(self.width//2, self.height//2, 15, -7)
                self.left_paddle = Paddle(10, self.height//2 - 50, net)
                self.right_paddle = Paddle(self.width - 30, self.height//2 - 50, net)
                sleep(1)
                self.draw(left_score, right_score)
                sleep(1)
            elif self.ball.x > self.width:
                right_score += 1
                self.ball = Ball(self.width//2, self.height//2, 15)
                self.left_paddle = Paddle(10, self.height//2 - 50, net)
                self.right_paddle = Paddle(self.width - 30, self.height//2 - 50, net)
                sleep(1)
                self.draw(left_score, right_score)
                sleep(1)

            self.draw(left_score, right_score)
    
    def train_ai(self, genome1, genome2, config):
        self.left_paddle = Paddle(10, self.height//2 - 50)
        self.right_paddle = Paddle(self.width - 30, self.width//2 - 50)
        self.ball = Ball(self.height//2, self.width//2, 15)

        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.run = True
        self.right_hits = 0
        self.left_hits = 0
        right_score = 0
        left_score = 0

        while self.run:

            output1 = net1.activate((self.left_paddle.y, 
                                     self.ball.y, 
                                     abs(self.ball.x - self.left_paddle.x)))

            decision1 = output1.index(max(output1))
            self.left_paddle.ai_handle(decision1)

            output2 = net2.activate((self.right_paddle.y, 
                                     self.ball.y, 
                                     abs(self.ball.x - self.right_paddle.x)))
            decision2 = output2.index(max(output2))
            self.right_paddle.ai_handle(decision2)
            
            self.ball.handle_collision(self.left_paddle, 
                                       self.right_paddle, self)

            ball.move()
            if self.ball.x < 0:
                left_score += 1
                self.ball = Ball(self.width//2, self.height//2, 15, -7)
                self.left_paddle = Paddle(10, self.height//2 - 50)
                self.right_paddle = Paddle(self.width - 30, self.height//2 - 50)

            elif self.ball.x > self.width:
                
                right_score += 1
                ball = Ball(self.width//2, self.height//2, 15)
                left_paddle = Paddle(10, self.height//2 - 50)
                right_paddle = Paddle(self.width - 30, self.height//2 - 50)
                

            if left_score >= 1 or right_score >= 1 or self.left_hits > 500:
                genome1.fitness += self.left_hits
                genome2.fitness += self.right_hits
                self.run = False
                break

    def draw(self, right_score, left_score):
        self.w.fill(((0, 0, 0)))
        left_score_text = self.font.render(f"{left_score}", 1, (255, 255, 255))
        right_score_text = self.font.render(f"{right_score}", 1, (255, 255, 255))
        self.w.blit(left_score_text, (self.width//4 * 3 - left_score_text.get_width()//2, 20 ))
        self.w.blit(right_score_text, (self.width//4 - right_score_text.get_width()//2, 20))
        self.ball.draw(self.w)
        paddles = [self.left_paddle, self.right_paddle]
        for paddle in paddles:
            paddle.draw(self.w)
        
        for i in range(11, self.height, self.height//20):
            if i % 2 == 0:
                continue
            else:
                pg.draw.rect(self.w, (255, 255, 255), (self.width//2 - 5/2,i, 5, self.height//20))
        pg.display.update()



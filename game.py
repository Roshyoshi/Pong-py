import pygame as pg
from time import sleep 
import neat
import os
import random 
import pickle

WIDTH, HEIGHT = 700, 500

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
class Ball:
    def __init__(self, x, y, radius, x_vel=7, y_vel=random.randint(-7, 7)):

        self.MAX_VEL = 7 
        self.x = x
        self.y = y
        self.r = radius

        self.x_vel = int(random.choice([x_vel, - x_vel]))
        self.y_vel = y_vel 
        self.color = WHITE
    def draw(self, w):
        pg.draw.rect(w, WHITE, (self.x, self.y, self.r, self.r))

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

def handle_collision(ball, left_paddle, right_paddle, game):
    if ball.y + ball.r//2 < 0:
        ball.y_vel *= -1
    elif ball.y + ball.r//2 >= HEIGHT:
        ball.y_vel *= -1
    
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.r<= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1.05
                middle_y = left_paddle.y + left_paddle.height /2
                dy = middle_y - ball.y
                reduct = (left_paddle.height/2)//ball.MAX_VEL
                ball.y_vel = dy//reduct if ball.y_vel < 0 else - dy//reduct
                game.left_hits += 1 
    else:
        if ball.y >= right_paddle.y and ball.y  <= right_paddle.y + right_paddle.height:
            if ball.x + ball.r >= right_paddle.x:
                ball.x_vel *= -1.05
                middle_y = right_paddle.y + right_paddle.height /2
                dy = middle_y - ball.y
                reduct = (right_paddle.height/2)//ball.MAX_VEL
                ball.y_vel = dy//reduct if ball.y_vel < 0 else - dy//reduct
                game.right_hits += 1 




class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 100
        self.color = WHITE
        self.speed = 10
    def draw(self, w):
        pg.draw.rect(w, self.color, (self.x, self.y, self.width, self.height))
    def move(self, up=True):
        if up and not self.y < 0:
            self.y -= self.speed
        elif not self.y > HEIGHT - self.height:
            self.y += self.speed
    def ai_handle(self, d):
        if d == 0:
            self.move()
        elif d == 1:
            pass
        elif d == 2:
            self.move(False)
        
    
def haddle_paddle_movement(keys, lp, rp=None):
    if keys[pg.K_w]:
        lp.move(up=True)
    if keys[pg.K_s]:
        lp.move(up=False)
    if rp != None:
        if keys[pg.K_i]:
            rp.move(up=True)
        if keys[pg.K_k]:
            rp.move(up=False)


class PongGame:
    def __init__(self, width, height):
        self.w = pg.display.set_mode((width, height))
        pg.display.set_caption("AI Pong")
        pg.font.init()
        self.height = height
        self.width = width
        self.run = True
        self.clock = pg.time.Clock()
        self.ball = Ball(height//2, width//2, 15)
        self.left_paddle = Paddle(10, height//2 - 50)
        self.right_paddle = Paddle(width - 30, width//2 - 50)
        self.FONT = pg.font.SysFont("comicsans", 50)

    def ai_game(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        

        w = self.w
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle
        ball = self.ball
        HEIGHT = self.height
        WIDTH = self.width
        left_score = 0
        right_score = 0
        FONT = self.FONT
        self.right_hits = 0
        self.left_hits = 0
        while self.run:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print("asdf")
                    self.run = False
                    break
            keys = pg.key.get_pressed()
            haddle_paddle_movement(keys, left_paddle)
            output = net.activate((right_paddle.y,
                                    ball.y,
                                    abs(ball.x - right_paddle.x)))
            decision = output.index(max(output))
            right_paddle.ai_handle(decision)
            ball.move()
            handle_collision(ball, left_paddle, right_paddle, self)
            if ball.x < 0:
                left_score += 1
                ball = Ball(WIDTH//2, HEIGHT//2, 15, -7)
                left_paddle = Paddle(10, HEIGHT//2 - 50)
                right_paddle = Paddle(WIDTH - 30, HEIGHT//2 - 50)
                sleep(1)
                PongGame.draw(w, [left_paddle, right_paddle], ball, right_score, left_score, FONT)
                sleep(1)
            elif ball.x > WIDTH:
                right_score += 1
                ball = Ball(WIDTH//2, HEIGHT//2, 15)
                left_paddle = Paddle(10, HEIGHT//2 - 50)
                right_paddle = Paddle(WIDTH - 30, HEIGHT//2 - 50)
                sleep(1)
                PongGame.draw(w, [left_paddle, right_paddle], ball, right_score, left_score, FONT)
                sleep(1)
            PongGame.draw(w, [left_paddle, right_paddle], ball, right_score, left_score, FONT)
    
    
    def train_ai(self, genome1, genome2, config):
        def d():
            PongGame.draw(w, [left_paddle, right_paddle], ball, right_score, left_score, FONT)
        self.left_paddle = Paddle(10, self.height//2 - 50)
        self.right_paddle = Paddle(self.width - 30, self.width//2 - 50)
        self.ball = Ball(self.height//2, self.width//2, 15)

        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        w = self.w
        self.run = True
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle
        self.right_hits = 0
        self.left_hits = 0
        ball = self.ball
        HEIGHT = self.height
        WIDTH = self.width
        right_score = 0
        left_score = 0
        FONT = self.FONT
        while self.run:

            # PongGame.draw(w, [left_paddle, right_paddle], ball, right_score, left_score, FONT)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print("asdf")
                    quit()
            output1 = net1.activate((self.left_paddle.y, self.ball.y, abs(self.ball.x - self.left_paddle.x)))
            decision1 = output1.index(max(output1))
            left_paddle.ai_handle(decision1)
            output2 = net2.activate((self.right_paddle.y, self.ball.y, abs(self.ball.x - self.right_paddle.x)))
            decision2 = output2.index(max(output2))
            right_paddle.ai_handle(decision2)

            ball.move()
            handle_collision(ball, left_paddle, right_paddle, self)
            if ball.x < 0:
                
                left_score += 1
                d()
                ball = Ball(WIDTH//2, HEIGHT//2, 15, -7)
                left_paddle = Paddle(10, HEIGHT//2 - 50)
                right_paddle = Paddle(WIDTH - 30, HEIGHT//2 - 50)
            elif ball.x > WIDTH:
                
                right_score += 1
                d()
                ball = Ball(WIDTH//2, HEIGHT//2, 15)
                left_paddle = Paddle(10, HEIGHT//2 - 50)
                right_paddle = Paddle(WIDTH - 30, HEIGHT//2 - 50)
                

            if left_score >= 1 or right_score >= 1 or self.left_hits > 50:
                genome1.fitness += self.left_hits
                genome2.fitness += self.right_hits
                self.run = False
                break



        


    @classmethod
    def draw(cls, w, paddles, ball, right_score, left_score, FONT):
        w.fill((BLACK))
        left_score_text = FONT.render(f"{left_score}", 1, WHITE)
        right_score_text = FONT.render(f"{right_score}", 1, WHITE)
        w.blit(left_score_text, (WIDTH//4 * 3 - left_score_text.get_width()//2, 20 ))
        w.blit(right_score_text, (WIDTH//4 - right_score_text.get_width()//2, 20))
        ball.draw(w) 
        for paddle in paddles:
            paddle.draw(w)
        
        for i in range(11, HEIGHT, HEIGHT//20):
            if i % 2 == 0:
                continue
            else:
                pg.draw.rect(w, WHITE, (WIDTH//2 - 5/2,i, 5, HEIGHT//20))
        pg.display.update()

def main(cfg):
    a = PongGame(700, 500)
    with open("best.pickle", "rb") as FILE:
        winner = pickle.load(FILE) 
    a.ai_game(winner, cfg)

def eval_genomes(genomes, config):
    width, height = 700, 500
    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None  else genome2.fitness
            game = PongGame(width, height)
            game.train_ai(genome1, genome2, config)

def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 150)
    with open("best.pickle", "wb") as FILE:
        pickle.dump(winner, FILE)
    

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    main(config)
    #run_neat(config)



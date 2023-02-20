import pygame as pg
from time import sleep 
import neat
import os
import random 
import pickle

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
        print("Yay")

        self.y_vel = dy//reduct if self.y_vel < 0 else - dy//reduct
        if random.randint(-10, 10) == 1:
            self.y_vel += 1


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

def run_game(cfg):
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

    winner = p.run(eval_genomes, 1000)
    with open("best.pickle", "wb") as FILE:
        pickle.dump(winner, FILE)
    

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    run_game(config)

    # run_neat(config)



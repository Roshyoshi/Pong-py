from game import *
import neat
import random

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


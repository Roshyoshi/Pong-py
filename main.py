import game
import neat
import random
import os
import pickle

def run_game(cfg):
    a = game.PongGame(700, 500)
    with open("best.pickle", "rb") as FILE:
        winner = pickle.load(FILE)
    option = input("Press 1 for AI vs AI or anything else for a different option: ")
    if option == "1":
        a.ai_game(winner, cfg, 2, 2)
    else:
        option = input("Select a player. Press 1 for left player or anything else for right player: ")
        if option == "1":
            a.ai_game(winner, cfg, 1, 2)
        else:
            a.ai_game(winner, cfg, 2, 1)

def eval_genomes(genomes, config):
    width, height = 700, 500
    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None  else genome2.fitness
            game = game.PongGame(width, height)
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
    option = input("Select a run mode. Press 1 for Pong and 2 for AI Training: ").strip()
    if option == "1":
        run_game(config)
    elif option == "2":
        run_neat(config)
    else:
        print("Invalid option. Quitting ...")



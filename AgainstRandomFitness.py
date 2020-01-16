import neat
from sys import stdout
from random import choice
from Morpx import Morpx, play, listMoves

class AgainstRandomFitness:
    def __init__(self, n=10):
        self.n=n
    
    def run(self, genomes, config):
        i=0
        for g_id, genome in genomes:
            stdout.write(chr(27))
            stdout.write('[2;1H')
            stdout.write(chr(27))
            stdout.write('[2K')
            stdout.write("Network ")
            stdout.write(str(i))
            stdout.flush()
            i+=1
            network=neat.nn.recurrent.RecurrentNetwork.create(genome, config)
            
            wins=0
            losses=0
            draws=0
            for j in range(self.n):
                if j!=0:
                    network.reset()
                turn = 0
                player = 1+(i%2)
                current_player = 1
                game = Morpx()
                while game.ended==0:
                    if current_player==player:
                        play(game, network, player, turn)
                    else:
                        xyxy=choice(listMoves(game))
                        game.set(int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3]), current_player)
                    current_player = 2 if current_player==1 else 1
                    turn+=1
                if game.ended==player:
                    wins+=1
                elif game.ended==(2 if player==1 else 1):
                    losses+=1
                else:
                    draws+=1
            genome.fitness=3*wins+draws

from swissround.tournament.Player import Player
from swissround.tournament.Tournament import Tournament

import neat
from sys import stdout

class Network(Player):
    def __init__(self, g_id, genome, network):
        self.name=str(g_id)
        self.g_id=g_id
        self.genome=genome
        self.network=network
        
        self.score=0
        self.hasPlayed=[]

class SwissRoundFitness:
    def __init__(self, gamefn):
        class GameWrapper:
            def __init__(self, p1, p2):
                self.n1=p1.network
                self.n2=p2.network
                self.even=True
            def play(self, ):
                self.even=not self.even
                if self.even:
                    self.result=gamefn(self.n1, self.n2)
                else:
                    rst=gamefn(self.n2, self.n1)
                    if rst==1:
                        self.result=2
                    elif rst==2:
                        self.result=1
                    else:
                        self.result=-1
        self.game=GameWrapper

    def run(self, genomes, config):
        players=[]
        for g_id, genome in genomes:
            network=neat.nn.recurrent.RecurrentNetwork.create(genome, config)
            players.append(Network(g_id, genome, network))
        tournament=Tournament(players, self.game, 3)
        for i in range(tournament.nbRounds):
            stdout.write(chr(27))
            stdout.write('[2;1H')
            stdout.write(chr(27))
            stdout.write('[2K')
            stdout.write("Round ")
            stdout.write(str(i))
            stdout.flush()
            tournament.createRound()
            tournament.playRound()
            tournament.updateRank()
        for network in tournament.ranking:
            network.genome.fitness=network.score

import neat
from sys import stdout
from Morpx import Morpx, play, listMoves
from minmax.minmax import Minmax

class GameWrapper:
    def __init__(self, player=1, status=0, game=Morpx()):
        if player==2:
            player=-1
        self.player=player
        self.status=status
        self.game=game
    
    def getPlayer(self):
        return self.player
    
    def getStatus(self):
        return self.status
    
    def getScore(self, weights):
        return 1000000*self.status
    
    def getMoves(self):
        if self.status!=0:
            return []
        return listMoves(self.game)
    
    def playClone(self, x, y, x2, y2):
        clone=self.game.clone()
        clone.set(x, y, x2, y2, 2 if self.player==-1 else 1)
        if clone.ended==1:
            status=1
        elif clone.ended==2:
            status=-1
        else:
            status=0
        return GameWrapper(-self.player, status, clone)

class AgainstMinmaxFitness:
    def __init__(self, n=10, depth=2):
        self.n=n
        self.depth=depth
    
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
                        state = GameWrapper(game=game, player=current_player)
                        moves, expectedScore = Minmax.getBestMove(state, self.depth)
                        move = moves[0]
                        game.set(move[0], move[1], move[2], move[3], current_player)
                    current_player = 2 if current_player==1 else 1
                    turn+=1
                if game.ended==player:
                    wins+=1
                elif game.ended==(2 if player==1 else 1):
                    losses+=1
                else:
                    draws+=1
            genome.fitness=3*wins+draws

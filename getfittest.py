#!/usr/bin/env python3

# syntax: getfittest.py <checkpoint>

from sys import stdout, argv
from random import choice
import neat
from Morpx import Morpx, play, listMoves

print("Loading network")
checkpoint = argv[1]
p = neat.Checkpointer.restore_checkpoint(checkpoint)
population = p.population
config = p.config

print("Running 10 games against random AI")
bestgid, bestscore=-1, -1
for gid in population:
    genome = population[gid]
    network=neat.nn.recurrent.RecurrentNetwork.create(genome, config)
    
    wins=0
    losses=0
    draws=0
    for i in range(10):
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
    score=3*wins+draws
    if score>bestscore:
        bestscore, bestgid=score, gid
print("Best network for checkpoint {}: {} Score: {}".format(checkpoint, bestgid, bestscore))

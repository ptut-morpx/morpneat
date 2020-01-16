#!/usr/bin/env python3

# syntax: backend.py <player> <checkpoint> [netid]

from sys import stdout, argv
import neat
from Morpx import Morpx, play

player = int(argv[1][1])
if player==-1:
    player = 2
p = neat.Checkpointer.restore_checkpoint(argv[2])
population = p.population
config = p.config
if len(argv)==4:
    genome = population[int(argv[3])]
else:
    for e in population:
        genome = population[e]
network=neat.nn.recurrent.RecurrentNetwork.create(genome, config)

turn = 0
current_player = 1
game = Morpx()
while True:
    if current_player==player:
        print("{}{}{}{}".format(*play(game, network, player, turn)))
    else:
        xyxy=input()
        if xyxy=='end':
            break
        game.set(int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3]), current_player)
    current_player = 2 if current_player==1 else 1
    turn+=1

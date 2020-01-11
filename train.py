#!/usr/bin/env python3
import os
from sys import stdout
import neat
import math
from TicTacToe import TicTacToe
from NoStagnation import NoStagnation
from CustomReporter import CustomReporter

ROUNT_COUNT=6

def sortedindexes(l):
    x=list(range(len(l)))
    l=[i for i in l]
    s=False
    n=len(l)-1
    while not s:
        s=True
        for i in range(n):
            if l[i]<l[i+1]:
                l[i], l[i+1], x[i], x[i+1]=l[i+1], l[i], x[i+1], x[i]
                s=False
        n-=1
    return x

def fight(a, b):
    result=0
    for i in range(ROUNT_COUNT):
        a.reset()
        b.reset()
        t=TicTacToe()
        turn=1 if i%2==0 else -1
        while t.result()==0 and not t.ended():
            rst=a.activate(t.board) if turn==1 else b.activate(t.board)
            idx=sortedindexes(rst)
            played=False
            while not played:
                c, idx=idx[0], idx[1:]
                try:
                    t.set(c//3, c%3, turn)
                    played=True
                except KeyError:
                    pass
            turn*=-1
        result+=t.result()
    return result

def eval_genomes(genomes, config):
    networks={g_id: neat.nn.recurrent.RecurrentNetwork.create(genome, config) for g_id, genome in genomes}
    count=0
    for a_id, a_genome in genomes:
        a_genome.fitness=0.0
        count+=1
    idx=0
    for a_id, a_genome in genomes:
        a_net=networks[a_id]
        idx+=1
        stdout.write(chr(27))
        stdout.write('[2;1H')
        stdout.write(chr(27))
        stdout.write('[2K')
        stdout.write(str(idx))
        stdout.flush()
        for b_id, b_genome in genomes:
            if b_id==a_id:
                continue
            b_net=networks[b_id]
            result=fight(a_net, b_net)
            a_genome.fitness+=result
            b_genome.fitness-=result

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, NoStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    
    # Use a reporter to show population info
    p.add_reporter(CustomReporter())
    
    # Use checkpoints to save progress to disk
    p.add_reporter(neat.Checkpointer(5))

    # Run until the heat death of the universe (until we get killed)
    winner = p.run(eval_genomes, math.inf)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

# clear screen
stdout.write(chr(27))
stdout.write('[2J')
stdout.flush()

# start training
run('TicTacToe.config')

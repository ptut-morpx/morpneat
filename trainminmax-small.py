#!/usr/bin/env python3
import os
from sys import stdout
import neat
import math
from AgainstMinmaxFitness import AgainstMinmaxFitness
from NoStagnation import NoStagnation
from CustomReporter import CustomReporter

fitness=AgainstMinmaxFitness(20, 2)

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, NoStagnation,
                         config_file)
    
    # Try loading a population, or create one
    files = [f for f in os.listdir('.') if "neat-minmax-small-checkpoint-" in f]
    generations = [int(f[29:]) for f in files]
    if len(generations)!=0:
        most = max(generations)
        stdout.write('Loading population from generation ')
        stdout.write(str(most))
        stdout.flush()
        p = neat.Checkpointer.restore_checkpoint('neat-minmax-small-checkpoint-'+str(most))
    else:
        stdout.write('Generating population')
        stdout.flush()
        p = neat.Population(config)
    
    # Use a reporter to show population info
    p.add_reporter(CustomReporter())
    
    # Use checkpoints to save progress to disk
    p.add_reporter(neat.Checkpointer(1, filename_prefix='neat-minmax-small-checkpoint-'))

    # Run until the heat death of the universe (until we get killed)
    p.run(fitness.run, math.inf)

# clear screen
stdout.write(chr(27))
stdout.write('[2J')
stdout.write(chr(27))
stdout.write('[1;1H')
stdout.flush()

# start training
run('Predator-small.config')

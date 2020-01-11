import neat
from sys import stdout
from neat.six_util import itervalues

def get_avg_fitness(pop):
    fit=[c.fitness for c in itervalues(pop)]
    s=0
    for f in fit:
        s+=f
    return s/len(fit)

class CustomReporter(neat.reporting.BaseReporter):
    def start_generation(self, generation):
        stdout.write(chr(27))
        stdout.write('[1;1H')
        stdout.write(chr(27))
        stdout.write('[2K')
        stdout.write("Generation ")
        stdout.write(str(generation))
        stdout.flush()
    
    def post_evaluate(self, config, pop, species, best):
        stdout.write(chr(27))
        stdout.write('[3;1H')
        stdout.write(chr(27))
        stdout.write('[2K')
        stdout.write("Fitness: AVG=")
        stdout.write(str(get_avg_fitness(pop)))
        stdout.write(", MAX=")
        stdout.write(str(best.fitness))
        stdout.flush() 

    def info(self, msg):
        stdout.write(chr(27))
        stdout.write('[5;1H')
        stdout.write(chr(27))
        stdout.write('[2K')
        stdout.write(msg)
        stdout.flush()

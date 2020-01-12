from os import listdir
from os.path import isfile
path = "."
files = [f for f in listdir(path) if isfile(path+f)]
print(files)

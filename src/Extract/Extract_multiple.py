import multiprocessing
from multiprocessing import Pool
import os

def Extract_single(tup):
    start = tup[0]
    end = tup[1] 
    command = "python3 Extract_single.py "
    command = command + str(start) + " "
    command = command + str(end)
    assert os.system(command)==0

param = [(125, 150), (150, 175), (175, 200)]
# param = [(200, 225)]
# param = [(0, 10)]

pool = Pool(2) #  2 CPUs
resultat = pool.map(Extract_single, param)

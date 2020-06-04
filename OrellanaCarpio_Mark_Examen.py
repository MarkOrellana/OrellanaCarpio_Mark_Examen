# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 09:43:53 2020

@author: danie
"""

import time
import random
import functools
from mpi4py import MPI
import numpy as np

def normalize_vector_sequential(ar):
    result = []
    squared_sum = 0
    for n in ar:
        squared_sum += n * n
    raiz = squared_sum**(.5)
    for n in ar:
        result.append(n/raiz)
    return result
# Complete the normalize_vector_parallel function below.
def normalize_vector_parallel():
    ar_count = 4000000
    matResult=[]
    comm = MPI.COMM_WORLD
    cw_size = comm.Get_size()
    cw_rank = comm.Get_rank()
    if cw_rank==0:
        ar = [random.randrange(1,30) for i in range(ar_count)]
        averow=int(ar_count/(cw_size))
        extra=ar_count%(cw_size)
        offset=0
        for dest in range(1,cw_size):
            rows=averow+1 if dest <= extra else averow
            comm.send(offset,dest)
            comm.send(rows,dest)
            comm.send(ar,dest)
            #comm.send(Mat2,dest)
            offset+=rows
            for i in range(1,cw_size):
                recupero=comm.recv(source=i)
                matResult.append(recupero)
    #print(matResult)
    if cw_rank>0:
        offse=comm.recv(source=0)
        row=comm.recv(source=0)
        data=comm.recv(source=0)
        #data2=comm.recv(source=0)
        #C=np.zeros((numberRows,numberColumns))
        squared_sum=0
        for k in range(data):
            squared_sum += k * k
        raiz = squared_sum**(.5)
        comm.send(raiz,0)
        
def normalize_vector_parallel1():
    ar_count=4000000
    
        
if __name__ == '__main__':
    # Prepare data
    ar_count = 4000000
    #Generate ar_count random numbers between 1 and 30
    ar = [random.randrange(1,30) for i in range(ar_count)]
    inicioSec = time.time()
    resultsSec = []
    resultsSec = normalize_vector_sequential(ar)
    finSec =  time.time()

    # You can modify this to adapt to your code
    inicioPar = time.time()   
    resultsPar = []
    resultsPar = normalize_vector_parallel()
    finPar = time.time()  
    
    # You can modify this to adapt to your code
    inicioMulti = time.time()   
    resultsMulti = []
    resultsMulti = normalize_vector_parallel1()
    finMulti = time.time()  

    #print('Results are correct!\n' if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,resultsSec,resultsPar), True) else 'Results are incorrect!\n')

    print('Sequential Process took %.3f ms \n' % ((finSec - inicioSec)*1000))

    print('Parallel Process MPI took %.3f ms \n' % ((finPar - inicioPar)*1000))
    
    print('Parallel Process MultiProcessing took %.3f ms \n' % ((finMulti - inicioMulti)*1000))
import numpy 
from mpi4py import MPI
import socket
import pickle
import importlib
from subprocess import call

import os
import  importlib

comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()

s_1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#s_1.setblocking(0)
def load_pickle(name):
	with open(name,"rb") as data_out:
		return pickle.load(data_out)
seed=0
numpy.random.seed(seed)
port=numpy.random.randint(1024,65535)
print(f"\nFinding a reciptint at port: {port}\n\n")
s_1.connect((socket.gethostname(),port))
print(f"Connection has been established with core: {seed}\n\n")
name=f"data_from_core_{rank}.py"
s_1.settimeout(1)

with open(name,'wb') as file:
	data=s_1.recv(1)
	while data:
		try:
			file.write(data)
			data=s_1.recv(1)

		except socket.timeout:
			#module=importlib.import_module(name[0:-3])
			#result=module
			break;

print("Function has been received!\n\n")

with open('out.txt','w+') as fout:
        out=call(["python3",name],stdout=fout)
        fout.seek(0)
        result=fout.read()
print("Computing result...\n\n")
print(f"Result={result}\n\n")
s_1.send(bytes(result,"utf-8"))

print("Work done in Core 1...")
s_1.close()
os.remove(name)

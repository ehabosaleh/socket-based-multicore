import numpy
import secrets
from mpi4py import MPI
import socket
import random
import concurrent.futures
from math import cos
import pickle
from math import pi
import os
import threading
import time

comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()
def integral_0(a_i, h, n):
	integ = 0.0
	for j in range(n):
		a_ij = a_i + (j + 0.5) * h
		integ += cos(a_ij) * h
	return integ
	
def integral(file_name,core_id,a,h,n,size):
	with open(file_name,'at') as core_file:
		with open("function.py","rt") as function_file:
			a_i=a+core_id*n*h
			module="from math import cos,pi\n"
			core_file.write(module)
			parameters=f"n={n};a={a};b=pi/2.0;h=({b}-{a})/({n}*{size});a_i={a_i}\n"
			core_file.write(parameters)
			fun=function_file.read()
			core_file.write(fun)
	with open(file_name,"a") as file:
		file.write(f"result=integral({a_i}, {h}, {n})\n")
		file.write("print(result)\n")


def scatter_data(file_name,core_id,conn):
	with open(file_name,'rb') as file:
		f=file.read(1)
		while f:
			conn.send(f)
			f=file.read(1)
			if not f :
				break;
		print("Function file has been sent\n\n")

def gather_data(core_id,conn):
	print(f"Receiving from core {core_id} ...\n\n")
	result=0
	conn.settimeout(10)
	try:
		result=conn.recv(1024).decode('utf-8')

	except socket.timeout:
		pass
	print(f"Partial integral {result} has been captured from core {core_id}. ")
	
	return result
if rank==0:
	print(f"\n\nThis is Master at core {rank}\n\n")
	s_0=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	seed=rank
	numpy.random.seed(seed)
	port=numpy.random.randint(1024,65535)
	s_0.bind((socket.gethostname(),port))
	s_0.listen(5)
	core_id=1
	result=[]
	while core_id<size:
		print(f"Listening to port: {port} ....\n")
		conn,addr=s_0.accept()

		print(f"Connection has been established with core: {core_id}\n")

		n=5000;a=0.0;b=pi/2.0; h=(b-a)/(n*size);

		file_name=f"data_for_core_{core_id}.py"
		integral(file_name,core_id,a,h,n,size)
		scatter_data(file_name,core_id,conn)

		result.append(float(gather_data(core_id,conn)))
		core_id=core_id+1
		os.remove(file_name)
	core_id=0;n=5000;a=0.0;b=pi/2.0; h=(b-a)/(n*size);
	result_c0=integral_0(a,h,n);
	print(f"Core {core_id} calculated the partial integral {result_c0}\n\n")
	result.append(result_c0);
	print(f"Total integral is: {sum(result)}\n")
	conn.close()



# socket-based-multicore
If we want to connect two nodes in a network, we usually open a channel and direct one of the nodes to listen to a specific port at a specific IP address while the other establishes the connection.  In networking terminology we call the listener node the server and the other is the client. On the other side, we refer to this process of establishing a connection as Socket Programming. 
In the real world, these nodes could be any terminal (PCs, mobile phones, etc.) controlled by a user. However, the goal of this experiment is to see if we can use the socket programming concept to connect cores belonging to the same processor and participate in solving a mathematical problem.<br> 
We used the Intel(R) Core(TM) i5-2430M CPU, which has two physical cores each can run two threads simultaneously, for a total of four threads. We will use these four threads as standalone cores despite the fact that we only  have two cores.
<h2> Problem to be solved:</h2>
We aim to find the  integral of cos(x) in the domain <img src="https://latex.codecogs.com/svg.image?[0&space;-\pi&space;/2]" title="[0 \pi /2]" />, which is given in the following equation:<br>
<img src="https://latex.codecogs.com/svg.image?y=\int_{0}^{\pi/2}&space;cos(x)&space;dx" title="y=\int_{0}^{\pi/2} cos(x) dx" />  (1) <br>
 But instead, we will use the Riemann Sums rule that approximate the actual area under the curve by dividing it into multiple simple shapes and have the following formula:<br>
 <img src="https://latex.codecogs.com/svg.image?y=\sum_{i=0}^{p-1}[\sum_{j=0}^{n-1}&space;cos(aij)*h" title="y=\sum_{i=0}^{p-1}[\sum_{j=0}^{n-1} cos(aij)*h" /> (2) <br> 
 Where:<br>
 <img src="https://latex.codecogs.com/svg.image?h=(b-a)/pn&space;" title="h=(b-a)/pn " /> (3) <br>
 <img src="https://latex.codecogs.com/svg.image?ai=a&plus;i*n*h&space;" title="ai=a+i*jn*h " /> (4) <br>
 <img src="https://latex.codecogs.com/svg.image?aij=ai&plus;(j&plus;0.5)*h&space;" title="aij=ai+(j+0.5)*h " /> (5) <br>
 p: the number of partions (number of cores), h is the number of icreament per partion. n: should be as big as possible for more accurate results.<br>
<p>In mathematics, a Riemann sum is a certain kind of approximation of an integral by a finite sum. One very common application is approximating the area of functions or lines on a graph, but also the length of curves and other approximations. </p>
<img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Riemann_sum_convergence.png" width="300" height="300" align="center">
The sum is calculated by partitioning the region into shapes (rectangles, trapezoids, parabolas, or cubics) that together form a region that is similar to the region being measured, then calculating the area for each of these shapes, and finally adding all of these small areas together. This approach can be used to find a numerical approximation for a definite integral even if the fundamental theorem of calculus does not make it easy to find a closed-form solution.<br>
<h2> The implementation:</h2>
The code is available in five different files: <br>
<b>core_0.py</b>: Prepare the first core to open a socket, then send the function (function.py) with the appropriate parameters when it receives any response from the other three cores, and lastly, calculate the final result once all of the connected cores' results have been received. <br>
<b>core_1.py, core_2.py, core_3.py</b>: Each file instructs the remaining cores to listen to the socket created by core_0 and receive the function file with its parameters, calculate the result, and return it to core_0. <br>
<b>function.py</b>: It contains the implementation of the equations (2), (3), (4) and (5). <br>
We run core 0.py first, then core 1.py, core 2.py, and core 3.py in any order. The core_0 will wait until it receives the final partial integral before displaying the final integral. 
To make the core_0 expect receiving output from <i>n</i> cores we type the follwing command in terminal when we run the file code_0.py: <br>
mpirun --oversubscribe -np 4 python3 core_0.py <br>
Where 4 is the number of cores.<br>

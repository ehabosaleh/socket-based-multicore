# socket-based-multicore
If we want to connect two nodes in a network, we usually open a channel and direct one of the nodes to listen to a specific port at a specific IP address while the other establishes the connection.  In networking terminology we call the listener node the server and the other is the client. On the other side, we refer to this process of establishing a connection as Socket Programming. 
In the real world, these nodes could be any terminal (PCs, mobile phones, etc.) controlled by a user. However, the goal of this experiment is to see if we can use the socket programming concept to connect cores belonging to the same processor and participate in solving a mathematical problem. 
We used the Intel(R) Core(TM) i5-2430M CPU, which has two physical cores each can run two threads simultaneously, for a total of four threads. We will use these four threads as standalone cores despite the fact that we only  have two cores. 
##  Problem to be solved:
<img src="https://latex.codecogs.com/svg.image?\bg_white&space;\int_{0}^{2\pi&space;}cos(x)&space;dx" title="\bg_white \int_{0}^{2\pi }cos(x) dx" />

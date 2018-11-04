HW2: Chord distributed hash protocol

Student will implement the Chord protocol. It is described in the paper Chord: A scalable peer-to-peer lookup service for internet applications. It is also described in a wiki page. [Update This is another paper from Chord authors.]

The goal of this assignment is students to demonstrate an understanding of the Chord protocol.

Protocol

The Chord protocol is described elsewhere and will not be repeated here. We will review a few critical components. The Chord nodes form a ring, each node has a successor and a predecessor. Each Chord ring supports a hash table with a fixed number of keys that is a power of 2 (i.e., 256, 1024, 4096). Because finding the proper node takes O(N)--where N is number of nodes--steps in a ring, each Chord node maintains a finger table to short-cut this step, reducing the cost to O(log N). The ring is fault-tolerant and there is no master. Therefore, the data may become stale. Chord has developed several methods that are periodically invoked to keep data update. Students will need to implement several methods to support the protocol. Below are some of the Chord methods that will be needed from wiki.

join -- called when a node joins the ring; initialize successor and finger table.
stabilize -- called periodically; node updates who it thinks its successor is.
notify -- a node tells its successor that it exists so the successor can update it predecessor value.
fix_fingers -- updates the finger table
The above list is not exhaustive.

Implementation

Students will develop a simulation of a chord system. It is implemented as a single program--not a set of distributed nodes. I implemented this as a python program that maintained the chord nodes as instances of an object. An objects is created (simulating node creation). Then, methods are called on objects (simulating an RPC on the simulated node). The state of each simulated node is maintained in object variables. Destroying an object simulates the node exiting the system. This is an example, students may choose a different way to implement their simulation.

The program runs a command line interface. For example:

> add 9
< Added node 9
> show 9
< Node 9: suc 9, pre None: finger 9,9,9,9,9,9,9,9,9,9
> add 44
< Added node 44
> join 44 9
> list
< Nodes:9, 44
> add 22
< Added node 22
> join 22 9
> list
< Nodes:9, 22, 44
UPDATE: Example of list and show:
> list
< Nodes: 9, 22, 44
> show 9
< Node 9: suc 9, pre None: finger 9,9,9,9,9,9,9,9,9,9
The right arrow is the prompt and indicates input to the program. The left arrow is the output from the program.

The simulation program has one parameter that define the size of the hash table. The parameter is the power to which 2 is raise. Thus a size parameter of 6 create a distributed hash table with 64 keys. The program also has an optional parameter ("-i") that is an input file of commands that are run in batch mode. The program should not output a prompt in batch mode.

The program will accept the following commands either interactively or in batch mode. Emit errors if the commands are ill formed in any way. Common errors are node does not exist; incorrect number of parameters; etc.

end -- stop the program without saying anything.
add <id> -- add node to ring with given id.
drop <id> -- remove node with given id from ring.
join <from> <to> -- join node from with the node to. Join should be call only once right after a node is added.
fix <id> -- fix the finger table for given node.
stab <id> -- invoke stabilize method on given node.
list -- show the id for each node in the ring.
show <id> -- show the successor, predecessor, and finger table for the given node.
Output

Please follow the required output carefully to ease grading of your assignment.

General
ERROR: invalid integer <n>
ERROR: node id must be in [0,<n>)
SYNTAX ERROR: <cmd> expects <n> parameters not <m>
ERROR: Node <n> does not exist
ERROR: Node <n> exists
No output--that means no output--except for errors.
end
join
fix
stab
add
Added node <n>
drop
Dropped node <n>
list (order least to greatest)
Nodes: <n1>, <n2>, ..., <nM>
show (for the given node)
Node <n>: suc <n1>, pre <n2 or None>: finger <f1>,<f2>,...,<fM>

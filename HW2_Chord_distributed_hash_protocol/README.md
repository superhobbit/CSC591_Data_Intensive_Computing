The fix command wasn't executed along with the join command

inorder to keep the finger table in the right order, you need to continuously call 'fix node' 

Only the first node through 'add' command would be added in the ring, otherwise it wasn't in the ring without join command, eg: 

add 100

add 120

list

[100]

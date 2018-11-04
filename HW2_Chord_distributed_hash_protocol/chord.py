#!/usr/bin/python

import sys

node_size = 0
maxNodeID = 0
nodes = {}
nodes_in_ring = {}

class table_item:
	def __init__(self, s, suc):
		self.start = s
		self.succ = suc

class node:
	def __init__(self, id, size):
		self.m = size
		self.id = id
		self.succ = self
		self.pre = None
		self.next = 0
		self.total = pow(2, size)
		self.finger_table = [table_item((id + pow(2, i)) % self.total, self.succ) for i in range(size)]

	def find_succ(self, id):
		successor = self.succ
		if self.interval(self.id, successor.id, id, True):
			return successor
		else:
			return successor.closest_pre(id).find_succ(id)

	def interval(self, left, right, x, right_close):
		if left < right:
			return left < x <= right if right_close else left < x < right
		if right_close:
			return left < x <= self.total-1 or 0 <= x <= right
		return left < x <= self.total-1 or 0 <= x < right

	def closest_pre(self, id):
		for i in range(self.m-1, -1, -1):
			if self.interval(self.id, id, self.finger_table[i].succ.id, False):
				return self.finger_table[i].succ
		return self

	def join(self, otherNode):
		self.pre = None
		self.succ = otherNode.find_succ(self.id)

	def stab(self):
		x = self.succ.pre
		if x != None and self.interval(self.id, self.succ.id, x.id, False):
			self.succ = x
		self.succ.notify(self)

	def notify(self, pre):
		if self.id != pre.id:
			if self.pre == None or self.interval(self.pre.id, self.id, pre.id, False):
				self.pre = pre

	def fix_fingers(self):
		self.next %= self.m
		#print (self.id + pow(2, self.next)) % self.total
		self.finger_table[self.next].succ = self.find_succ((self.id + pow(2, self.next)) % self.total)
		self.next += 1

	def drop(self):
		if self.succ.id != self.id:
			if self.pre != None and self.pre.id != self.id:
				self.succ.pre = self.pre
			else:
				self.succ.pre = None
		if self.pre != None and self.pre.id != self.id:
			if self.succ.id != self.id:
				self.pre.succ = self.succ
			else:
				self.pre.succ = self.pre

	def show(self):
		arr = []
		for i in range(self.m):
			arr.append(self.finger_table[i].succ.id)
		prestr = str(self.pre.id) if self.pre != None else "None"
		return "Node {0}: suc {1}, pre ".format(self.id, self.succ.id) + prestr + ": finger " + ",".join(str(arr[i]) for i in range(len(arr))) 

def to_int(val):
	try:
		val = int(val)
		return val
	except:
		print "ERROR: invalid integer {0}".format(val)
		sys.exit()		

def handle_cmd(cmds):
	out = []
	for cmd in cmds:
		arr = cmd.split()
		length = len(arr)
		for i in range(length):
			if i >= 1:
				arr[i] = to_int(arr[i])

		if arr[0] == "add":
			if length != 2:
				print "SYNTAX ERROR: add command expects 2 parameters not {0} with second type int".format(length)
				sys.exit()
			if arr[1] in nodes:
				print "ERROR: Node {0} exists".format(arr[1])
				sys.exit()
			if arr[1] > maxNodeID or arr[1] < 0:
				print "ERROR: node id must be in [0, {0})".format(maxNodeID+1)
				sys.exit()
			nodes[arr[1]] = node(arr[1], node_size)
			if len(nodes_in_ring) == 0:
				nodes_in_ring[arr[1]] = nodes[arr[1]]
			out.append("Added node {0}".format(arr[1]))

		elif arr[0] == "join":
			if length != 3:
				print "SYNTAX ERROR: join command expects 3 parameters not {0} with last two type int".format(length)
				sys.exit()
			if arr[1] not in nodes:
				print "ERROR: Node {0} does not exist".format(arr[1])
				sys.exit()
			if arr[2] not in nodes:
				print "ERROR: Node {0} does not exist".format(arr[2])
				sys.exit()
			nodes[arr[1]].join(nodes[arr[2]])
			nodes_in_ring[arr[1]] = nodes[arr[1]]
			nodes_in_ring[arr[2]] = nodes[arr[2]]

		elif arr[0] == "drop":
			if length != 2:
				print "SYNTAX ERROR: drop command expects 2 parameters not {0} with second type int".format(length)
				sys.exit()
			if arr[1] not in nodes:
				print "ERROR: Node {0} does not exist".format(arr[1])
				sys.exit()
			try:
				if arr[1] in nodes_in_ring:
					nodes[arr[1]].drop()
					del nodes_in_ring[arr[1]]
				del nodes[arr[1]]
				out.append("Dropped node {0}".format(arr[1]))	
			except e:
				print e
				raise

		elif arr[0] == "end":
			if length != 1:
				print "SYNTAX ERROR: end command expects 1 parameters not {0}".format(length)
				sys.exit()				
			return out

		elif arr[0] == "fix":
			if length != 2:
				print "SYNTAX ERROR: fix command expects 2 parameters not {0} with second type int".format(length)
				sys.exit()		
			if arr[1] not in nodes_in_ring:
				print "ERROR: Node {0} does not exist in the ring, please refer to the ReadME".format(arr[1])
				sys.exit()
			nodes[arr[1]].fix_fingers()

		elif arr[0] == "stab":
			if length != 2:
				print "SYNTAX ERROR: stab command expects 2 parameters not {0} with second type int".format(length)
				sys.exit()
			if arr[1] not in nodes_in_ring:
				print "ERROR: Node {0} does not exist in the ring, please refer to the ReadME".format(arr[1])
				sys.exit()
			nodes[arr[1]].stab()

		elif arr[0] == "list":
			arr = []
			for key in nodes_in_ring:
				arr.append(nodes_in_ring[key].id)
			arr.sort()
			out.append("Nodes: " + ",".join(str(arr[i]) for i in range(len(arr))))

		elif arr[0] == "show":
			if length != 2:
				print "SYNTAX ERROR: show command expects 2 parameters not {0} with second type int".format(length)
				sys.exit()	
			if arr[1] not in nodes_in_ring:
				print "ERROR: Node {0} does not exist in the ring, please refer to the ReadME".format(arr[1])
				sys.exit()							
			out.append(nodes[arr[1]].show())

		else:
			raise Exception("Wrong Argument")

	return out

if __name__ == "__main__":

	argv = sys.argv
	length = len(argv)

	if length == 4:
		aaa = to_int(argv[3])
		if aaa <= 0:
			print "ERROR: invalid integer {0}".format(aaa)
			sys.exit()	
		if argv[1] != "-i":
			print "SYNTAX ERROR: expects -i parameters not {0}".format(argv[1])
			sys.exit()		
		node_size = aaa
		maxNodeID = pow(2, aaa) - 1
		try:
			file = open(argv[2], "r")
			out = handle_cmd(file)
			for o in out:
				print o
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
		except ValueError:
			print "Could not convert data to an integer."
		except:
			print "Unexpected error:", sys.exc_info()[0]
			raise	

	elif length == 2:
		aaa = to_int(argv[1])
		if aaa <= 0:
			print "ERROR: invalid integer {0}".format(aaa)
			sys.exit()		
		node_size = aaa
		maxNodeID = pow(2, aaa) - 1
		while True:
			try:
				cmd = raw_input("> ")
				out = handle_cmd([cmd])
				if len(out):
					print "< " + out[0]
				if cmd == "end":
					sys.exit()
			except Exception as e:
				raise
			else:
				pass
			finally:
				pass

	else:
		print "SYNTAX ERROR: start command expects 1 or 3 parameters not {0}".format(length)
		sys.exit()



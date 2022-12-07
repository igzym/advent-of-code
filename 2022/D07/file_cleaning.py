import sys

import re

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()


class DirNode:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        if self.parent is None:
            self.path = name
        else:
            pp = self.parent.path
            if pp.endswith('/'):
                pp = pp[:-1]
            self.path = pp + '/' + name # convenience
        self.children = []
        self.file = []
        self.size = 0
        # print(f"DEBUG node: {self.path} (new)")

    def add_child_dir(self, node):
        self.children.append(node)
        # print(f"DEBUG node: {self.path} new child_dir {node.path}")

    def add_file(self, name, size):
        self.file.append((name, size))
        # print(f"DEBUG ... {self.file}")

max_size_threshold = 100000
tot_size_to_threshold = 0

def calc_sizes(node):
    global tot_size_to_threshold
    size = 0
    for c in node.children:
        size += calc_sizes(c)
    for f in node.file:
        size += f[1]
    node.size = size
    # print(f"DEBUG {node.path} size {node.size}")
    if size <= max_size_threshold:
        tot_size_to_threshold += size
    return size

cur_node = None
root_node = None

ls_req = False
cd_target = None

for ll in lines:
    ll = ll.strip("\n")

    ll = ll.split()
    if ll[0] == '$':
        if ll[1] == 'cd':
            ls_req = False
            cd_target = ll[2]
            if cd_target == '..':
                cur_node = cur_node.parent
                continue
            if cur_node is None:
                cur_node = DirNode(cd_target, None)
                root_node = cur_node
            else:
                nn = DirNode(cd_target, cur_node)
                cur_node.add_child_dir(nn)
                cur_node = nn
        elif ll[1] == 'ls':
            ls_req = True
            cd_target = None
        else:
            assert False, 'unexpected command'
    else:
        if ls_req:
            if ll[0] == 'dir':
                pass # we don't care about directories...
            else:
                cur_node.add_file(ll[1], int(ll[0]))

calc_sizes(root_node) 


capacity = 70000000
needed_size = 30000000
min_size_to_free = needed_size - (capacity - root_node.size)

print(f"root node size: {root_node.size}")
print(f"current free size: {capacity - root_node.size}")
print(f"min_size_to_free: {min_size_to_free}")


smallest_needed_to_free = root_node.size
def calc_smallest_needed_to_free(node):
    global smallest_needed_to_free
    if node.size >= min_size_to_free:
        if node.size < smallest_needed_to_free:
            smallest_needed_to_free = node.size

    for c in node.children:
        calc_smallest_needed_to_free(c)

calc_smallest_needed_to_free(root_node)

print(f"RESULT: tot_size_to_threshold {tot_size_to_threshold} (part 1)")
print(f"RESULT: smallest_needed_to_free {smallest_needed_to_free} (part 2)")

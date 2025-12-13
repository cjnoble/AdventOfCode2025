import time
from functools import cache
from collections import defaultdict

def read_text_file (file_path):

    with open(file_path, "r") as f:
        data = f.readlines()
        data = [line.replace("\n","") for line in data]

    return data


class Node(object):

    def __init__(self, name, connections):
        self.name = name
        self.connections = connections

    @classmethod
    def from_string(cls, string):
        #aaa: you hhh
        string = string.split(" ")
        name = string[0][:-1]

        return cls(name, string[1:])
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

def check_node(node:Node, nodes, routes):

    for connection in node.connections:
        if connection == "out":
            routes += 1 
        else:
            routes = check_node(nodes[connection], nodes, routes)

    return routes

class NodeChecker (object):
    def __init__(self,nodes):
        self.nodes = nodes
        self.looping_nodes = set()
        self.routes = 0
        self.cache = defaultdict(lambda: 0)

    def check_node_flags(self, node: Node, target, flag_dac=False, flag_fft=False, visited=None):
        if visited is None:
            visited = set()

        if node.name == "kuc":
            print("kuc")

        #Loop detection
        if node.name in visited:
            self.looping_nodes.add(node.name)
            return 0

        visited.add(node.name)
        total_paths = 0
        print(f"On node: {node.name} visited: {visited}")

        for connection_name in node.connections:
            if connection_name in self.looping_nodes:
                continue

            # propagate flags down the branch
            new_flag_dac = flag_dac or (connection_name == "dac")
            new_flag_fft = flag_fft or (connection_name == "fft")

            if connection_name == target:
                if new_flag_dac and new_flag_fft:
                    total_paths += 1
                continue

            if self.cache[connection_name] > 0 and new_flag_dac and new_flag_fft:
                total_paths += self.cache[connection_name]

            # update cache after recursion
            total_paths += self.check_node_flags(self.nodes[connection_name], target, new_flag_dac, new_flag_fft, visited.copy())

        #visited.remove(node.name)

        self.cache[node.name] = total_paths
        return total_paths 


    def check_node(self, node: Node, target, visited=None):
        if visited is None:
            visited = set()

        if node.name == "kuc":
            print("kuc")


        #Loop detection
        if node.name in visited:
            self.looping_nodes.add(node.name)
            return 0

        visited.add(node.name)
        total_paths = 0
        print(f"On node: {node.name} visited: {visited}")

        for connection_name in node.connections:
            if connection_name in self.looping_nodes:
                continue

            if connection_name == target:
                total_paths += 1
                continue
            elif connection_name == "out":
                continue

            if connection_name in self.cache:
                total_paths += self.cache[connection_name]

            # update cache after recursion
            else:
                total_paths += self.check_node(self.nodes[connection_name], target, visited.copy())

        #visited.remove(node.name)

        self.cache[node.name] = total_paths
        return total_paths 

def part_1(data):

    nodes = {node.name: node for node in [Node.from_string(row) for row in data]}

    routes = 0
    current = nodes["you"]
    routes = check_node(current, nodes, routes)

    return routes

def part_2(data):

    nodes = {node.name: node for node in [Node.from_string(row) for row in data]}

    svr_to_dac_checker = NodeChecker(nodes)
    svr_to_dac_checker.check_node(nodes["svr"], "dac")

    svr_to_fft_checker = NodeChecker(nodes)
    svr_to_fft_checker.check_node(nodes["svr"], "fft")

    dac_to_fft_checker = NodeChecker(nodes)
    dac_to_fft_checker.check_node(nodes["dac"], "fft")

    fft_to_dac_checker = NodeChecker(nodes)
    fft_to_dac_checker.check_node(nodes["fft"], "dac")

    dac_to_out_checker = NodeChecker(nodes)
    dac_to_out_checker.check_node(nodes["dac"], "out")
    
    fft_to_out_checker = NodeChecker(nodes)
    fft_to_out_checker.check_node(nodes["fft"], "out")

    print(svr_to_dac_checker.cache["svr"])
    print(dac_to_fft_checker.cache["dac"])
    print(fft_to_out_checker.cache["fft"])

    print(svr_to_fft_checker.cache["svr"])
    print(fft_to_dac_checker.cache["fft"])
    print(dac_to_out_checker.cache["dac"])
    
    return svr_to_dac_checker.cache["svr"] * dac_to_fft_checker.cache["dac"] * fft_to_out_checker.cache["fft"] + svr_to_fft_checker.cache["svr"] * fft_to_dac_checker.cache["fft"] * dac_to_out_checker.cache["dac"]

def part2_vis(data):

    nodes = {node.name: node for node in [Node.from_string(row) for row in data]}

    for node in nodes.values():
        for conn in node.connections:
            print(f"{node.name}: {conn}")

if __name__ == "__main__":

    DAY = "11"
    data = read_text_file(f"{DAY}.txt")
    part_1_start = time.time()
    print(part_1(data))
    print(f"Part 1 finished in {time.time() - part_1_start} s")

    part_2_start = time.time()
    #print(part2_vis(data))
    print(part_2(data))
    print(f"Part 2 finished in {time.time() - part_2_start} s")
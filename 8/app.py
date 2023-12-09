from dataclasses import dataclass
import re
from pprint import pprint
from typing import List

@dataclass
class Node:
    start: str
    left: str
    right: str

    @staticmethod
    def create_node(node_raw: str):
        start, rest = node_raw.split(" = ")
        left, right = re.findall("[A-Z0-9]+", rest)
        return Node(start, left, right)

@dataclass
class Graph:
    graph: List[Node]

    def to_dict(self) -> dict[str: tuple[str]]:
        return {node.start:(node.left, node.right) for node in self.graph}
    
    @staticmethod
    def follow_instructions(graph_dict: dict[str:tuple], 
                            instructions: List[bool], start: str="AAA") -> str:
        for step_right in instructions:
            if step_right:
                start = graph_dict[start][1]
            else:
                start = graph_dict[start][0]
        return start # last node in step sequence
    
    def from_a_to_z(self, instructions: List[bool], 
                    start: str="AAA", destination: str="ZZZ", stop_at: int=10000):
        nodes_dict = self.to_dict()
        iterations = 0
        while start != destination:
            start = Graph.follow_instructions(nodes_dict, instructions, start=start)
            iterations += 1
            if iterations == stop_at:
                return None
        return iterations
    

    def from_a_to_z_multiple(self, instructions: List[bool]) -> List[int]:
        nodes_dict = self.to_dict()
        inital_nodes = [node_start for node_start in nodes_dict if node_start.endswith("A")]
        final_nodes = [node_start for node_start in nodes_dict if node_start.endswith("Z")]
        iterations_possible_for_all = list() #accumulates all possible iterations for all starts

        for node_initial in inital_nodes:
            iterations_possible = list() #accumulates all possible iterations for this start
            n_tries_allowed = 1000
            while iterations_possible == []: #go on until at least one will be found
                for node_final in final_nodes:
                    n_iterations = self.from_a_to_z(instructions, start=node_initial, 
                                                destination=node_final, stop_at=n_tries_allowed)
                    if n_iterations is not None:
                        iterations_possible.append(n_iterations)
                n_tries_allowed *= 2
            iterations_possible_for_all.extend(iterations_possible)
        
        return iterations_possible_for_all


def import_dat(fn: str="8/input.txt") -> (List[bool], Graph):
    with open(fn, 'r') as f:
        dat = f.readlines()
        instructions = list(dat[0].strip("\n"))
        direction_to_bool = lambda x: True if x == 'R' else False
        instructions = [direction_to_bool(direction) for direction in instructions]
        # print(instructions)

        nodes = [Node.create_node(node_raw.strip("\n")) for node_raw in dat[2:]]
        # pprint(nodes)
        return instructions, Graph(nodes)


def find_common_denominator(int_list: List[int]):
    common = 1
    for int_ in int_list:
        common *= int_
    for denominator_candidate in reversed(range(min(int_list), max(int_list)+1)):
        for my_int in int_list:
            if my_int % denominator_candidate != 0:
                denominator = False
                break
            else:
                denominator = True
        if denominator is True:
            common = int(common/denominator_candidate)
    
    return common


def main():
    instructions, nodes = import_dat()
    n_steps = nodes.from_a_to_z(instructions)*len(instructions)
    print("Result Part One:", n_steps)

    ghost_steps_for_each = nodes.from_a_to_z_multiple(instructions)
    print("Result Part Two:", find_common_denominator(ghost_steps_for_each)*len(instructions))



if __name__ == "__main__":
    main()




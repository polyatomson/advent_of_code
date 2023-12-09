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
        left, right = re.findall("[A-Z]+", rest)
        return Node(start, left, right)

@dataclass
class Graph:
    graph: List[Node]

    def to_dict(self) -> dict[str: tuple]:
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
    
    def from_a_to_z(self, instructions: List[bool]):
        nodes_dict = self.to_dict()
        last_node = "AAA"
        steps = 0
        while last_node != "ZZZ":
            last_node = Graph.follow_instructions(nodes_dict, instructions, start=last_node)
            steps += len(instructions)
        return steps

            

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


def main():
    instructions, nodes = import_dat()
    n_steps = nodes.from_a_to_z(instructions)
    print("Result Part One:", n_steps)



if __name__ == "__main__":
    main()




import random
from typing import List

class Edge:
    def __init__(self, start: int, end: List[int], child: 'Node'):
        self.start = start
        self.end = end
        self.child = child
        
        
class Node:
    def __init__(self, name, is_leaf: bool = False):
        self.name = name
        self.edges = [0]*127
        self.suffix_link = None
        self.is_leaf = is_leaf
        
    def add_edge(self, edge: Edge, char: str):
        self.edges[ord(char)] = edge
        
    def get_edge(self, char: str) -> Edge:
        return self.edges[ord(char)] if self.edges[ord(char)] else None
    
    def set_suffix_link(self, node: 'Node'):
        self.suffix_link = node
        
    def get_suffix_link(self) -> 'Node':
        return self.suffix_link
    
    def __str__(self):
        return self.name.upper()
    
    def is_leaf(self) -> bool:
        return self.is_leaf
    
    def remove_edge(self, char: str):
        self.edges[ord(char)] = 0
        
class SuffixTree:
    
    def __init__(self, text: str):
        self.root = Node("root")
        self.active_node = self.root
        self.text = text
        self.remainder = None
        self.lastj = 0
        self.g_end = [0]
        self.build_tree()
        
    def base_case(self):
        """
        Create base case, rule 2 case 1, link root node to a new leaf node with the first character of the text.
        """
        first_leaf = Node("0", is_leaf=True)
        edge = Edge(0, self.g_end, first_leaf)
        
        self.root.add_edge(edge, self.text[edge.start])
        self.root.set_suffix_link(self.root)
        
    def build_tree(self):
        """
        Build the suffix tree using Ukkonen's algorithm.
        """
        # initiAlize base case
        self.base_case()
        
        for i in range(1, len(self.text)):
            print("phase", i, "remainder", self.remainder, "skip index", self.lastj)
            print("i char", self.text[i])
            self.g_end[0] += 1
            print("update", i, self.g_end)
            prev_internal_node = None
            
            for j in range(self.lastj+1, i+1):
                # traverse from current active + remainder to desired location
                # use skip count to skip over internal nodes
                # update active node and remainder accordingly
                print("phase", i, "extension", j)
                if self.remainder:
                    print(self.remainder, i, j)
                    print(self.active_node, self.active_node.edges )
                    # there is remainder from active node which allows us to skip to
                    # due to previous rule 3 extension
                    
                    # find the edge from active node that corresponds to the first character of the remainder
                    edge = self.active_node.get_edge(self.text[self.remainder[0]])
                    

                    # if the remainder is longer than the edge, skip over the edge
                    # by updating active node and remainder
                    while edge.end[0] - edge.start < self.remainder[1] - self.remainder[0]:
                        self.remainder = (self.remainder[0] + edge.end[0] - edge.start + 1, self.remainder[1])
                        self.active_node = edge.child
                        edge = self.active_node.get_edge(self.text[self.remainder[0]])
                        
                    print(edge)
                    print("pahse", i, "extension", j, "active node", str(self.active_node), "remainder", self.remainder, "edge", edge.start, edge.end, self.text[edge.start:edge.end[0]+1])
                    
                    print(edge.start, edge.end, self.remainder[0], self.remainder[1])
                    # there can be 2 cases after traversing the edge, whether we end up at the end of the edge or somewhere along the edge
                    
                    # CONDITION 1
                    # if the remainder is equal to the edge end, then we have reached the desired location
                    # update active node to next internal node and set remainder to None
                    if edge.end[0] - edge.start == self.remainder[1] - self.remainder[0]:
                        print("phase", i, "extension", j)
                        
                        self.active_node = edge.child
                        self.remainder = None
                        
                        # there can be 2 cases after reaching the internal node, whether next character is in the edge or not
                        
                        # CONDITION 1
                        # now, if next character is not in the edge, we can create new edge + leaf from internal node, using rule 2 case 1
                        if self.active_node.get_edge(self.text[i]) is None:
                            #TODO: implement rule 2 case 1
                            # rule 2 case 1
                            # create new leaf named j, and add edge from internal node to leaf (i, SuffixTree.g_end)
                            leaf = Node(str(j), is_leaf=True)
                            edge = Edge(i, self.g_end, leaf)
                            self.active_node.add_edge(edge, self.text[i])
                            
                            # increment lastj by 1, since we can ensure rule 2 willl be followed by rule 1 in next phase, means next phase can start from j+1
                            self.lastj += 1
                            
                            # if previous internal node is not None, set previous internal node's suffix link to current internal node/ active node
                            if prev_internal_node:
                                prev_internal_node.set_suffix_link(self.active_node)
                                
                            # # set active node's suffix link to root
                            # self.active_node.set_suffix_link(self.root)
                                
                            # if active node is not root, set active node as previous internal node
                            if self.active_node != self.root:
                                prev_internal_node = self.active_node
                                
                            # if active node is root and remainder is not None, set remainder to (remainder[0]+1, remainder[1])
                            if self.active_node == self.root and self.remainder:
                                self.remainder = (self.remainder[0]+1, self.remainder[1])
                            
                            print("ori active node", str(self.active_node), "j", j, "remainder", self.remainder)
                            # when everything is done, navigate to active node's suffix link
                            self.active_node = self.active_node.get_suffix_link()
                            
                            print("new active node", str(self.active_node), "j", j, "remainder", self.remainder)
                           
                        else: 
                            # CONDITION 2
                            # if next character is in the edge, we can add character to remainder and break phase
                            #TODO: implement rule 3 extension
                            self.remainder = (i, i)
                            break
                    
                    # CONDITION 2
                    # if remainder is not equal to edge end, that means our desired location is somewhere along the edge
                    else:
                        # CONDITION 1
                        # if next character is not in the edge
                        # we remove edge from active node and create new internal node, and a new leaf, using rule 2 case 2
                        x = edge.start + self.remainder[1] - self.remainder[0] + 1
                        
                        if self.text[x] != self.text[i]:
                            print("phase", i, "extension", j)
                            print("rule 2 case 2", self.text[x], self.text[i])
                            #TODO: implement rule 2 case 2
                            # store old_edge_start = edge.start, edge from active node
                            # update edge.start as x
                            old_edge_start = edge.start
                            print("old edge", edge.start, edge.end)
                            
                            edge.start = x
                            print("updated old edge", edge.start, edge.end)
                            
                            old_edge = edge
                            
                            # remove edge from active node
                            self.active_node.remove_edge(self.text[self.remainder[0]])
                            
                            # create new internal node with random name
                            new_internal_node = Node(self.text[random.randint(0, len(self.text)-1)])
                            
                            # create new leaf name j
                            new_leaf = Node(str(j), is_leaf=True)
                            
                            # create edge (i, gend) to leaf j
                            print("new edge", i, self.g_end, new_leaf)
                            new_edge_to_leaf = Edge(i, self.g_end, new_leaf)
                            
                            # add the new edge to new internal node
                            new_internal_node.add_edge(new_edge_to_leaf, self.text[i])
                            
                            # add old edge to new internal node
                            new_internal_node.add_edge(old_edge, self.text[x])
                            print("old edge", old_edge.start, old_edge.end)
                            
                            # create new edge from (old_edge_start, x-1), connect to new internal node
                            a = x-1
                            a = [a]
                            new_edge_to_internal = Edge(old_edge_start, a, new_internal_node)
                            
                            # add the new edge to active node
                            self.active_node.add_edge(new_edge_to_internal, self.text[old_edge_start])
                            
                            # increment lastj by 1, since we can ensure rule 2 willl be followed by rule 1 in next phase, means next phase can start from j+1
                            self.lastj += 1
                            
                            # if previous internal node is not None, set previous internal node's suffix link to new internal node
                            if prev_internal_node:
                                prev_internal_node.set_suffix_link(new_internal_node)
                                
                            # set new internal node's suffix link to root
                            new_internal_node.set_suffix_link(self.root)
                            
                            # set new internal node as previous internal node
                            prev_internal_node = new_internal_node
                            
                            # if active node is root and remainder is not None, set remainder to (remainder[0]+1, remainder[1])
                            if self.active_node == self.root and self.remainder:
                                if self.remainder[0] == self.remainder[1]:
                                    self.remainder = None
                                else:
                                    self.remainder = (self.remainder[0]+1, self.remainder[1])
                                
                            # when everything is done, navigate to active node's suffix link
                            print(self.active_node)
                            self.active_node = self.active_node.get_suffix_link()
                            print("after rule 2 case 2", self.active_node)
                        
                        else:  
                            # CONDITION 2
                            # if next character is in the edge, we can add character to remainder and break phase
                            #TODO: implement rule 3 extension
                            self.remainder = (self.remainder[0], self.remainder[1]+1)
                            break
   
                # CONDITION 2
                # there is no remainder, we have to traverse from active node                     
                else:
                    # CONDITION 1
                    # if next character is not in the edge, we create new edge, leaf from active node, using rule 2 case 1
                    if self.active_node.get_edge(self.text[i]) is None:
                    #TODO: implement rule 2 case 1
                        # rule 2 case 1
                        # create new leaf named j, and add edge from active node to leaf (i, SuffixTree.g_end)
                        leaf = Node(str(j), is_leaf=True)
                        edge = Edge(i, self.g_end, leaf)
                        self.active_node.add_edge(edge, self.text[i])
                        
                        # increment lastj by 1, since we can ensure rule 2 willl be followed by rule 1 in next phase, means next phase can start from j+1
                        self.lastj += 1
                        
                        # if previous internal node is not None, set previous internal node's suffix link to current internal node/ active node
                        if prev_internal_node:
                            prev_internal_node.set_suffix_link(self.active_node)
                            
                        # # set active node's suffix link to root
                        # self.active_node.set_suffix_link(self.root)
                            
                        # if active node is not root, set active node as previous internal node
                        if self.active_node != self.root:
                            prev_internal_node = self.active_node
                            
                        # if active node is root and remainder is not None, set remainder to (remainder[0]+1, remainder[1])
                        if self.active_node == self.root and self.remainder:
                            self.remainder = (self.remainder[0]+1, self.remainder[1])
                            
                        # when everything is done, navigate to active node's suffix link
                        self.active_node = self.active_node.get_suffix_link()
                        
                        print("active node", str(self.active_node), "j", j, "remainder", self.remainder)
                    
                    
                    # CONDITION 2
                    # if next character is in the edge, we can add character to remainder and break phase
                    #TODO: implement rule 3 extension
                    else:
                        # update remainder from none to (i, i)
                        self.remainder = (i, i)
                        break
                    
                print("active node", str(self.active_node), "j", j, "remainder", self.remainder)
            print(self, "done w phase", i)
        
    def sorted_suffix_array(self):
        """
        Return sorted suffix array of the text.
        """
        print(self)
        
        # use dfs to traverse the tree
        # if leaf node is reached, add the leaf node's name to the suffix array
        
        suffix_array = []
        
        def dfs(node: Node):
            if node.is_leaf:
                suffix_array.append(int(node.name))
                
            for edge in node.edges:
                if edge:
                    dfs(edge.child)
            
        dfs(self.root)
        
        return suffix_array
        
    def __str__(self):
        return self._str_recursive(self.root)

    def _str_recursive(self, node: Node, depth=0):
        indent = "  " * depth
        result = str(node) + "\n"
        print(node.edges)
        for edge in node.edges:
            if edge:
                char = self.text[edge.start]
                end_char = self.text[edge.end[0]]
                child_node = edge.child
                result += indent + f"  Edge: starting char: {char} index: {edge.start},\tending char: {end_char} index:{edge.end[0]}\n"
                result += self._str_recursive(child_node, depth + 1)
        return result
    


# import unittest
# import random

# class TestSuffixTree(unittest.TestCase):
#     def test_sorted_suffix_array(self):
        
#         for _ in range(20):  # Generate 5 random test cases
#             # Generate a random string for sample
#             print("hey")
#             # Define the ASCII range [36, 126]
#             ascii_range = list(range(36, 127))
#             ascii_range.remove(36)  # Remove the unique terminating character '$'
            

#             # Generate random characters for the string
#             random_string = ''.join(map(chr, random.choices(range(37, 127), k=30)))
            
#             # Append the terminating character '$'
#             random_string += '$'
            
#             sample = random_string
            
#             # Calculate ans using SuffixTree.sorted_suffix_array()
#             ans = SuffixTree(sample).sorted_suffix_array()

            
#             # Generate sorted_sample
#             sorted_sample = sorted([(sample[i:], i) for i in range(len(sample))])
            
#             print("here", sorted_sample, ans)
            
#             # Assert that the sorted suffix array matches the expected result
#             self.assertEqual([x[1] for x in sorted_sample], ans, f"Assertion error occurred for sample: {random_string}")


# if __name__ == '__main__':
#     unittest.main()

# sample = "mississippi$"

# ans = SuffixTree(sample).sorted_suffix_array()

# print([x+1 for x in ans])

# want = [2,8,10,6,7]

# suffix_sorted_position = [0]*len(sample)

# for sorted_position, suffix_index in enumerate(ans):
#     suffix_sorted_position[suffix_index] = sorted_position+1
    
# print(suffix_sorted_position)

# for index in want:
#     print(suffix_sorted_position[index-1])


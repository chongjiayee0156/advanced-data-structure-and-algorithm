import heapq
import bitarray
from typing import List

def get_huffman_code(tree_root: 'Node')-> List[bitarray.bitarray]:
    """
    traverse through the tree root using dfs to get the huffman code of each char.
    """
    char_code = [None]*127
    
    def dfs(node, binary = bitarray.bitarray()):
        if node.is_leaf:
            char_code[ord(node.char)] = binary        
        else:
            if node.left:
                dfs(node.left, binary + '0')
            if node.right:
                dfs(node.right, binary + '1')

    dfs(tree_root)
    
    return char_code
    
class Node:
    
    def __init__(self, freq, char=None, is_leaf=False):
        self.freq = freq
        self.char = char
        self.is_leaf = is_leaf
        self.left = None
        self.right = None
        
    def __lt__(self, other):
        return self.freq < other.freq
        
def build_huffman_tree(freq: List[int]):
    """
    Build a huffman tree from a frequency dictionary.

    Args:
        freq_dict (dict): _description_
    """
    char_freq_minheap = []
    # create node for each char with their frequency
    for char_ord in range(36, 127):
        if freq[char_ord] > 0:
            char = chr(char_ord)
            char_freq_minheap.append(Node(freq[char_ord], char, True))
            
    # heapify the nodes according to their frequency (minheap)
    heapq.heapify(char_freq_minheap)

    # if there is only 1 unique char in the text, build a parent node especially for that char
    if len(char_freq_minheap) == 1:
        left_child = heapq.heappop(char_freq_minheap)
        parent = Node(left_child.freq)
        parent.left = left_child
        return parent
        
    # build the huffman tree until there is only 1 node left in the heap
    while len(char_freq_minheap) > 1:
        
        # pop the 2 chars with the lowest frequency
        left_child = heapq.heappop(char_freq_minheap)
        right_child = heapq.heappop(char_freq_minheap)
        
        # merge them into a new node
        parent = Node(left_child.freq + right_child.freq)
        parent.left = left_child
        parent.right = right_child
        
        # push the new node back to the heap
        heapq.heappush(char_freq_minheap, parent)
        
        # repeat until there is only 1 node left in the heap
        # the last node is the root of the huffman tree
    return char_freq_minheap[0]

def huffman_encoding(text: str):
    """
    Encode a text using Huffman encoding.
    """
    # get a dict of each char and their frequency
    freq = [0]*127
    
    for x in text:
        freq[ord(x)] += 1

    # build a huffman tree
    tree_root = build_huffman_tree(freq)
    
    # traverse the tree to get list of each char and their huffman code
    char_code_list = get_huffman_code(tree_root)
    
    encoded_text = bitarray.bitarray()
    # encode each char of text using the code table
    for x in text:
        encoded_text.extend(char_code_list[ord(x)])
    
    # return the encoded text
    return encoded_text, char_code_list

def huffman_decoding(encoded_text: str, char_code_list: List[bitarray.bitarray]) -> str:
    """

    Args:
        encoded_text (str): _description_
        char_code_dict (dict): _description_
    """
      
    left_pointer = 0
    
    output = ''
    
    for right_pointer in range(1, len(encoded_text) + 1):
        code = encoded_text[left_pointer: right_pointer]
        if code in char_code_list:
            output += chr(char_code_list.index(code))
            left_pointer = right_pointer
        else:
            continue
        
    return output

# # Example usage:
# text = "abbcccddddeeeee"
# encoded_text, code_table = huffman_encoding(text)
# print("Encoded text:", encoded_text)
# decoded_text = huffman_decoding(encoded_text, code_table)
# print("Decoded text:", decoded_text)

# def bwt_construction(text: str) -> str:
#     """
#     Construct the Burrows-Wheeler Transform of a text.
#     """
#     cyclic_permutations = [text[i:] + text[:i] for i in range(len(text))]
    
     
#     cyclic_permutations.sort()
    
    
#     return "".join (x[-1] for x in cyclic_permutations)
    
# print(bwt_construction("banana$"))
# from bitarray import bitarray

# # Define your binary stream
# binary_stream = "000111000100110000110110001001111011011100101001001000111110110010110111110010"

# # Create a bitarray object
# ba = bitarray("00011111")

# # Pad the bitarray with zeros if necessary
# remainder = len(ba) % 8
# if remainder != 0:
#     padding = 8 - remainder
#     ba.extend('0' * padding)

# # Convert the bitarray to bytes
# byte_stream = ba.tobytes()

# # Print the byte stream
# print(byte_stream,"k")

with open('text.txt', 'w') as file:
    file.write("0001110011101111")
    
import os
print('0001110011101111', len('0001110011101111'))

print(os.path.getsize('text.txt'))

# change a bitarray to byte
a = bitarray.bitarray('000111001')
a = a.tobytes()
print(a)

# change the byte to bitarray again
b = bitarray.bitarray()
b.frombytes(a)
print(b)
print(len(b))

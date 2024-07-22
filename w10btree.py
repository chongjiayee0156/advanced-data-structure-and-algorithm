# Student Name: Chong Jia Yee
# Student ID: 33563888
# Question 2 Assignment 3 FIT3155

# Command line usage of the script:
# python q2.py <t> <dictionary.txt> <commands.txt>

#  B-tree is constructed based on the words provided in the file. 
# Subsequently, the commands specified in file are applied to the constructed B-tree one by one. 
# After executing the commands, the script traverses the final state of the B-tree and outputs 
# the sorted list of words contained in the B-tree to the output file (output_q2.txt).
 
import sys

class Node:
    def __init__(self, t, is_leaf = True):
        """
        Initialize a node in the B-tree.

        Args:
            t (int): Minimum degree parameter of the B-tree.
            is_leaf (bool, optional): Indicates whether the node is a leaf node. Defaults to True.
        """
        self.is_leaf = is_leaf
        self.elements = []
        self.children = []
        self.t = t
        self.parent = None

    def binary_search(self, word):
        """Return (True, index) if word is in the elements list of the node, otherwise return (False, index) where index is the index of the first element greater than word.

        Args:
            word (str): The word to search for.

        Returns:
            tuple: A tuple containing a boolean value indicating whether the word is found and the index where it should be inserted.
        """
        left = 0
        right = len(self.elements) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.elements[mid] == word:
                return (True, mid)
            if self.elements[mid] < word:
                left = mid + 1
            else:
                right = mid - 1
                
        return (False, left)
                
        
    def search(self, word):
        """Return True if word is in the tree, otherwise return False.

        Args:
            word (str): The word to search for.

        Returns:
            bool: True if word is found, False otherwise.
        """
        contains_word, index = self.binary_search(word)
        
        if contains_word:
            return True
        elif self.is_leaf:
            return False
        else:
            return self.children[index].search(word)
        
    
    def is_full(self):
        """Return True if the node is full, otherwise return False.

        Returns:
            bool: True if the node is full, False otherwise.
        """
        return len(self.elements) == 2 * self.t - 1
    

    def insert_to_node(self, word):
        """Insert a word into the node.

        If the node is a leaf node, insert the word into the node at the appropriate position.
        If the node is not a leaf node, insert the word into the appropriate child node.
        
        After inserting to a node, check if it is full, if yes, split it.

        Args:
            word (str): The word to insert.
        
        Returns:
            tuple: A tuple indicating whether a new root node is created after splitting and the new root node if created.
        """
        found, index = self.binary_search(word)
        
        if found:
            # Word already exists in the node, ignore
            return False, None
        
        if self.is_leaf:
            # Insert word into the node at the appropriate position
            self.elements.insert(index, word)
            if self.is_full():
                # If node is full after insertion, split it
                has_new_root , new_root = self.split()
                if has_new_root:
                    return has_new_root, new_root
                
            return False, None
        else:
            # Insert into the appropriate child node
            return self.children[index].insert_to_node(word)


            


    def split(self):
        """Split the node into two nodes.
        
        This method is called when a node becomes full after insertion.
        It splits the node into two and promotes the median element to the parent node.
        If new root is created, return True, otherwise return False.
        """
        median_index = len(self.elements) // 2
        median_key = self.elements[median_index]
        
        # Create a new node to hold the elements greater than the median
        new_node = Node(self.t, is_leaf=self.is_leaf)
        new_node.elements = self.elements[median_index + 1:]
        new_node.children = self.children[median_index + 1:]
        
        # Remove the elements and children greater than the median from the current node
        self.elements = self.elements[:median_index]
        self.children = self.children[:median_index + 1]
        
        # Promote the median key to the parent node
        if self.parent is None:
            # Create a new root if the current node is the root
            new_root = Node(self.t, is_leaf=False)
            new_root.elements = [median_key]
            new_root.children = [self, new_node]
            self.parent = new_root
            new_node.parent = new_root
            # return new root
            return (True, new_root)
        else:
            # Insert the median key into the parent node and adjust the child pointers
            contains, index = self.parent.binary_search(median_key)
            self.parent.children.insert(index+1, new_node)
            # update median
            self.parent.elements.insert(index, median_key)
            new_node.parent = self.parent
            return (False, None)
        
          
    def del_internal_word(self, index, word):
        """Delete the word at index from this internal node.

        Args:
            index (int): The index of the word to delete.
            word (str): The word to delete.

        Returns:
            tuple: A tuple indicating whether a new root node is created after deletion and the new root node if created.
        """
        # Find the predecessor of the word
        # if left subtree has more than minimum number of elements
        # case 2a
        if len(self.children[index].elements) >= self.t:
            predecessor = self.children[index].delete_max()
            self.elements[index] = predecessor
            return False, None
        # else if right subtree has more than minimum number of elements
        # case 2b
        elif len(self.children[index + 1].elements) >= self.t:
            successor = self.children[index + 1].delete_min()
            self.elements[index] = successor
            return False, None
        else:
            # case 2c might change height of tree
            # Merge children[index] and children[index + 1] and self.elements[index] into a single node
            merged_node = Node(self.t)
            merged_node.parent = self
            merged_node.elements = self.children[index].elements + [self.elements[index]] + self.children[index + 1].elements
            if not self.children[index].is_leaf:
                merged_node.children = self.children[index].children + self.children[index + 1].children

            del self.elements[index]
            del self.children[index]
            del self.children[index]
            
            self.children.insert(index, merged_node)
            
            if self.children[index].is_leaf:
                # if the merged node is a leaf node, delete the word from the merged node as leaf node, case 1
                self.children[index].delete_at_node(word)
            else:
                # if the merged node is not a leaf node, delete the word from the merged node as internal node
                # case 2 again
                self.children[index].del_internal_word(self.t-1, word)
                
            # check if has new root
            if self.elements == []:
                merged_node.parent = None
                return True, merged_node
            else:
                return False, None
    
    def delete_min(self):
        """Delete the minimum element from this tree

        Returns:
            str: The minimum element that is deleted.
        """
        # if the node is a leaf node, delete the minimum element from the node (leftmost)
        if self.is_leaf:
            return self.elements.pop(0)
        else:
            # if the node is not a leaf node, delete the minimum element from the child node
            if len(self.children[0].elements) >= self.t:
                return self.children[0].delete_min()
            else:
                # if the leftmost child node has only t-1 elements, we cant step into it
                # case 3
                # increase the number of elements in the child node by borrowing from its siblings or merging with its siblings
                self.delete_bare_minimum(0)
                return self.children[0].delete_min()
            
    def delete_max(self):
        """Delete the maximum element from this node or its child nodes.

        Returns:
            str: The maximum element that is deleted.
        """
        # if the node is a leaf node, delete the maximum element from the node (rightmost)
        if self.is_leaf:
            return self.elements.pop()
        else:
            # else, delete the maximum element from the child node
            if len(self.children[-1].elements) >= self.t:
                return self.children[-1].delete_max()
            else:
                # if the rightmost child node has only t-1 elements, we cant step into it
                # case 3
                # increase the number of elements in the child node by borrowing from its siblings or merging with its siblings
                self.delete_bare_minimum(len(self.children) - 1)
                # handle deletion again
                return self.children[-1].delete_max()
        
          
    def bare_minimum(self):
        """Check if the node has the bare minimum number of elements.

        Returns:
            bool: True if the node has the bare minimum number of elements, otherwise False.
        """
        return len(self.elements) == self.t - 1
    
    def delete_at_node(self, word):
        """Delete a word from this node.

        Args:
            word (str): The word to delete.

        Returns:
            tuple: A tuple indicating whether a new root node is created after deletion and the new root node if created.
        """
        found, index = self.binary_search(word)
        has_new_root, new_root = False, None
        if index<len(self.elements) and self.elements[index] == word:
            if self.is_leaf:
                # case 1
                del self.elements[index]
            else:
                # case 2
                x, y= self.del_internal_word(index, word)
                # update new root
                if x:
                    has_new_root, new_root = x, y
        else:
            # word is in child node
            # cant step into child node if it has only t-1 elements
            if self.children[index].bare_minimum():
                # case 3, need to borrow or merge elements from sibling for this child node
                x, y = self.delete_bare_minimum(index)
                # update new root
                if x:
                    has_new_root, new_root = x, y
            
            # rpt the samething on child node again
            x, y = self.children[index].delete_at_node(word)
            if x:
                has_new_root, new_root = x, y
                
        return has_new_root, new_root

    def delete_bare_minimum(self, index):
        """handle deletion when the child node has the bare minimum number of elements. 
        Increase the number of elements in the child node by borrowing from its siblings or merging with its siblings.

        Args:
            index (int): The index of the child node.
            word (str): The word to delete.

        Returns:
            tuple: A tuple indicating whether a new root node is created after deletion and the new root node if created.
        """
        has_new_root, new_root = False, None
        
        if len(self.children[index].elements) < self.t:
            # Case 3
            # if left sibling has more than t-1 elements, borrow from it
            # case 3a
            if index > 0 and len(self.children[index - 1].elements) > self.t - 1:
                self.get_from_left_sibling(index)
            # if right sibling has more than t-1 elements, borrow from it
            # case 3b
            elif index < len(self.elements) and len(self.children[index + 1].elements) > self.t - 1:
                self.get_from_right_sibling(index)
            # if both siblings have t-1 elements, merge with one of them
            # case 3c
            else:
                has_new_root, new_root = self.merge_with_sibling(index)
            
        return has_new_root, new_root

    def get_from_left_sibling(self, index):
        """Move an element from the left sibling to this node.

        Args:
            index (int): The index of the child node.
        """
        left_sibling = self.children[index - 1]
        child_node = self.children[index]

        # insert parent element to the beginning of child node
        child_node.elements.insert(0, self.elements[index - 1])
        # move the last element from left sibling to parent
        self.elements[index - 1] = left_sibling.elements.pop()
        
        # move the last child from left sibling to child node
        if not child_node.is_leaf:
            child_node.children.insert(0, left_sibling.children.pop())

    def get_from_right_sibling(self, index):
        """Move an element from the right sibling to this node.

        Args:
            index (int): The index of the child node.
        """
        right_sibling = self.children[index + 1]
        child_node = self.children[index]

        # insert parent element to the end of child node
        child_node.elements.append(self.elements[index])
        # move the first element from right sibling to parent
        self.elements[index] = right_sibling.elements.pop(0)
        
        # if child node is not a leaf, move the first child from right sibling to child node
        if not child_node.is_leaf:
            child_node.children.append(right_sibling.children.pop(0))

    def merge_with_sibling(self, index):
        """Merge this node with its sibling.

        Args:
            index (int): The index of the child node.

        Returns:
            tuple: A tuple indicating whether a new root node is created after merging and the new root node if created.
        """
        
        child_node = self.children[index]
        right_sibling = self.children[index + 1]

        # Move the parent element to the child node
        child_node.elements.append(self.elements[index])
        # move all elements from right sibling to child node
        child_node.elements.extend(right_sibling.elements)
        
        # move all children from right sibling to child node
        if not child_node.is_leaf:
            child_node.children.extend(right_sibling.children)

        # Remove the parent element
        del self.elements[index]
        # remove the right sibling
        del self.children[index + 1]

        if len(self.elements) == 0:
            # If the current node becomes empty after deletion, update the root
            child_node.parent = None
            return True, child_node
        else:
            return False, None

    def traverse(self, output):
        """Traverse all nodes in inorder and append elements to the output list.

        Args:
            output (list): The list to which the elements are appended.
        """
        if self.is_leaf:
            # If the node is a leaf node, print its elements
            for word in self.elements:
                output.append(word)
        else:
            # If the node is not a leaf node, recursively traverse its children
            for i in range(len(self.children)):
                # Traverse the subtree rooted at the ith child
                self.children[i].traverse(output)
                # Print the element at index i
                if i < len(self.elements):
                    output.append(self.elements[i])
                    
            
    def __str__(self):
        return (f"Elements: {[x for x in self.elements]}")

class BTree:
    def __init__(self, t):
        self.root = Node(t)
        self.t = t

    def traverse(self):
        """Traverse the B-Tree and return the sorted list of words.

        Returns:
            list: A sorted list of words in the B-Tree.
        """
        if self.root is not None:
            output = []
            self.root.traverse(output)
            return output

    def search(self, word):
        """Search for a word in the B-Tree.

        Args:
            word (str): word to be searched

        Returns:
            boolean: True if the word is found, False otherwise.
        """
        if self.root == None:
            return False
        else:
            return self.root.search(word)

    def insert(self, word):
        """Insert a word into the B-Tree.

        Args:
            word (str): The word to insert into the B-Tree.
        """
        
        # do nothing if the word is already in the tree
        is_in_tree = self.search(word)
        if is_in_tree:
            return
        
        # insert the word into the tree, starting from the root node
        has_new_root, new_root = self.root.insert_to_node(word)
        # update root if new root is created
        if has_new_root:
            self.root = new_root
            
    def delete(self, word):
        """Delete a word from the B-Tree.

        Args:
            word (str): The word to delete from the B-Tree.

        Returns:
            None
        """
        # do nothing if the tree is empty or the word is not in the tree
        if self.root is None or not self.search(word):
            return
        else:
            # delete word and update potential new root
            has_new_root, new_root = self.root.delete_at_node(word)
            if has_new_root:
                self.root = new_root
        
                
if __name__ == '__main__':
    def load_and_build_btree(filename, t):
        btree = BTree(t)
        with open(filename, 'r') as file:
            for line in file:
                word = line.strip()
                if word == "":
                    continue
                btree.insert(word)
        return btree
    
    def alter_command(filename, btree):
        with open(filename, 'r') as file:
            for line in file:
                command, word = line.strip().split()
                if command.lower() == 'insert':
                    btree.insert(word)
                else:
                    if word == "slicks":
                        btree.traverse()
                    btree.delete(word)
                    
    def write_output(filename, string):
        with open(filename, 'w') as file:
            file.write(string)

    t, dictionary_filename, commands_filename = int(sys.argv[1]), sys.argv[2], sys.argv[3]
    
    # creating a B-tree with words from a dictionary file
    btree = load_and_build_btree(dictionary_filename, t)
    
    # include commands in the file to alter the B-tree
    alter_command(commands_filename, btree)

    # write the sorted list of words contained in the B-tree to the output file
    output = btree.traverse()
    output = "\n".join(output)
    write_output("output_q2.txt", output)


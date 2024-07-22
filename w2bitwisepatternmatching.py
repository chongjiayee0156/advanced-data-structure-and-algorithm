from bitarray import bitarray

def preprocess_pattern_bitwise(pattern):
    """
    Preprocesses the pattern to calculate delta values for bitwise pattern matching.
    
    Time complexity: O(m)
    Space complexity: O(m)
    
    Args:
        pattern (str): The pattern string.
        
    Returns:
        dict: A dictionary containing delta values for each character in the pattern.
    """
    d = {}


    def calculate_delta(pattern):
        """
        Calculates delta values for each character in the pattern.
        
        Definition of delta value:
        Delta value is actually the position of that character in pattern 
        presented in a bit array form, but in reversed order. For example, 
        if the pattern is "abc", then the delta value of "a" is 001, the 
        delta value of "b" is 010, and the delta value of "c" is 100. 
        
        Args:
            pattern (str): The pattern string.
        """
        
        # use a dictionary to store the delta values
        # key is the ascii value of the character in pattern
        # value is the delta value in bitarray form
        
        # for each character in pattern, we add its position by shifting 1 i 
        # times to the left and use OR operation to combine them with previous positions
        for i in range(len(pattern)):
            cur_bitarray = d.get(ord(pattern[i]), bitarray(len(pattern)))
            new_bitarray = bitarray(len(pattern)) 
            new_bitarray[len(pattern) - 1] = 1
            
            d[ord(pattern[i])] = cur_bitarray | new_bitarray << i
            
    
    calculate_delta(pattern)
    return d
    
def search_bitwise(text, pattern):
    """
    Searches for the pattern in the text using bitwise pattern matching.
    
    Approach:
        We count the bitvector for each character in text
        
        Since we are using a bitwise OR operation, bit "1" represents a mismatch
        and bit "0" represents a match.
        
        Hence, if the first bit is bv[i] is 0, 
        tht means every character in pattern matches text in the position
        and we hv found a matched pattern
        
        By using dynamic programming, we only need to keep track of the bit 
        vector of previous chracter in order to calculate current bit vector
        formula given: bv[i] = bv[i-1]<<1 | delta[i]
        

    
    Args:
        text (str): The text string.
        pattern (str): The pattern string.
    """
    output = []
    
    # get delta values for each character in pattern
    delta = preprocess_pattern_bitwise(pattern)
    
    # for first character in text, its previous bit vector must be all 1s, 
    # since there is no previous character to be compared with pattern
    prev_bv = bitarray([1]*len(pattern))
    
    
    for i in range(len(text)):
        # get delta for current text character
        delta_value = delta.get(ord(text[i]), bitarray(len(pattern)))
        # we have to complement the delta value collected since we are using
        # bitwise OR operation, bit "1" represents a mismatch and bit "0" represents a match
        delta_value = ~delta_value
        
        # calculate current bit vector
        cur_bv = (prev_bv << 1) | delta_value
        
        if cur_bv[0] == 0:
            print("we found a match at position", i-len(pattern)+1)
            # we found a match
            output.append(i-len(pattern)+1)
            
        prev_bv = cur_bv
        
    return "\n".join(map(str,output))
        
text = "aaaaaaaaa"
pattern = "aaa"
print(search_bitwise(text, pattern))
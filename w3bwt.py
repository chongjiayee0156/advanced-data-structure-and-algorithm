def bwt(s):
    # # Add end-of-string marker
    # s += "$"
    # # Generate all rotations of the string
    # rotations = [s[i:] + s[:i] for i in range(len(s))]
    # # Sort the rotations
    # rotations.sort()
    # # Extract the last character of each rotation
    # bwt_result = ''.join(rotation[-1] for rotation in rotations)
    # return bwt_result
    
    s += '$'
    
    rotated_permutations = [s[i:] + s[:i] for i in range(len(s))]
    
    rotated_permutations.sort()
    
    bwt = [rotation[-1] for rotation in rotated_permutations]
    
    
    return ''.join(bwt)

# Example usage
input_string = "banana"
bwt_result = bwt(input_string)
print("Burrows-Wheeler Transform of", input_string, "is:", bwt_result)

# --------------------------------------------
import collections

def inverse_bwt(bwt):
    
    
    # get rank
    rank = {}
    
    sorted_bwt = sorted(bwt)
    
    for i,char in enumerate(sorted_bwt):
        if char not in rank:
            rank[char] = i
            
    # get count of tht char from [0:i] in bwt
    count = {s:0 for s in bwt}
    counter = [0]*len(bwt)
    
    for i,k in enumerate(bwt):
        counter[i] = count[k]
        count[k] += 1
        

    # get the original string
    
    x = '$'
    
    cur_char = bwt[0]
    index = 0
    
    while cur_char != '$':
        x += cur_char
        index_nxt_char = rank[cur_char] + counter[index]
        cur_char = bwt[index_nxt_char]
        index  = index_nxt_char
        print(x)
        
    return x[::-1]
    

# Example usage
bwt_string = "annb$aa"
print('j')
original_string = inverse_bwt(bwt_string)
print("Original string reconstructed from BWT:", original_string)


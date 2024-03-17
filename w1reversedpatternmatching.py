
# name: CHONG JIA YEE
# student id: 33563888

def compare_explicitly(string, k, z=None):
    count = 0
    
    s = 0 if z is None else z
    
    # compare each character of the string with the prefix
    
    while k<len(string) and string[k] == string[s]:
        count += 1
        k += 1
        s += 1
        
    return count

# Fills Z array for given string str[]
def zsuffix(string, z_val):
    n = len(string)
 
    # initialize l,r = 0, 0
    l, r = 0, 0
    
    # count z value for each indx and update l,r accordingly
    for k in range(1, n):
        
        # check for base case (k==1) (0-based index)
        # or case 1: k lies outside of rightmost z-box (k>r)
        if k>r:
            similar_count = compare_explicitly(string, k)
            if similar_count == 0:
                z_val[k] = 0
            else:
                z_val[k] = similar_count
                l = k
                r = k + similar_count - 1
                
        # case 2: k likes within rightmost z-box (k<=r)
        elif k<=r:
            # case 2a: z value of previous k lies within z-box (z_val[k-l] < -k+1)
            if z_val[k-l] < r-k+1:
                # its z value is the same as z value of k-l
                z_val[k] = z_val[k-l]
                # l and r remain the same
            
            # case 2b: if z value of previous k lies equal or outside the z-box
            elif z_val[k-l] >= r-k+1:
                # start to do explicit comparison on r+1  against r-l+1
                similar_count = compare_explicitly(string,r+1, r-l+1)
                
                z_val[k] = r-k+1 + similar_count
                l = k
                r = k + similar_count - 1
                
def reversed_z(string):
    # reverse input string and do normal z values
    reversed_str = string[::-1]
    z_val = [0]*len(reversed_str)
    z_val[0] = len(reversed_str)
    
    zsuffix(reversed_str, z_val)
    
    
reversed_z("aabcaabxaabcaabca")
                
    
    
    
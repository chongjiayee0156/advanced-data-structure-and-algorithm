
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
def gusfield(string, z_val):
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
            
            # case 2b: if z value of previous k lies equal to end of z-box
            elif z_val[k-l] == r-k+1:
                # start to do explicit comparison on r+1  against r-l+1
                similar_count = compare_explicitly(string, r+1, r-l+1)
                
                z_val[k] = r-k+1 + similar_count
                l = k
                r = k + similar_count - 1
            
            # case 2c: if z value of previous k lies beyond the end of z-box
            else:
                z_val[k] = r-k+1
                # l and r remain the same
                
                
                
        
    
def search (text, pattern):
    n = len(text)
    m = len(pattern)
    
    # concatenate both to form a string
    concat = pattern + "$" + text
    
    # initialize array to store z values for each index
    z_val = [0]*(n+m+1)
    
    # call function to calculate z values for each index
    # z value is the length of the longest substring starting from index i that matches prefix of the string
    gusfield(concat, z_val)
    
    # start looping from first alphabet of text to the end
    # (m+1, n+m+1) because we are only interested in the z values of the text
    # if z value of certain index is equal to the length of the pattern, 
    # means the substring of text matches the whole pattern
    # print the index of text
    print(z_val)
    print(len(z_val), m, n)
    print(m+1, m+n)
    
    for i in range(m+1, m+n+1):
        if z_val[i] == m:
            # print in 1-based index
            print("Pattern found at index", i-m)
            
search("GEEKS FOR GEEKS", "GEEK")
    
    
    
    
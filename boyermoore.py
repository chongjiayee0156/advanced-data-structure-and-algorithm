TOTAL_CHAR = 256

def preprocess_bad_char(pat):
    m = len(pat)
    
    bad_char_shift = [[-1]*TOTAL_CHAR for _ in range(m)]
    
    for i in range(m-1):
        char = ord(pat[i])
        bad_char_shift[i+1][char] = i 
        
    for i in range(1, m):
        for j in range(TOTAL_CHAR):
            if bad_char_shift[i][j] == -1:
                bad_char_shift[i][j] = bad_char_shift[i-1][j]
    
    return bad_char_shift

def preprocess_good_suffix(pattern):
    
    # Step 1: Get Z suffix
    # Fills Z array for given string str[]

    def compare_explicitly(string, k, z=None):
        count = 0
        
        s = 0 if z is None else z
        
        # compare each character of the string with the prefix
        
        while k<len(string) and string[k] == string[s]:
            count += 1
            k += 1
            s += 1
            
        return count

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
                    # start to do explicit comparison on r+1  against r-k+1
                    similar_count = compare_explicitly(string, r+1, r-k+1)
                    
                    z_val[k] = r-k+1 + similar_count
                    l = k
                    r = k + similar_count - 1
                
                # case 2c: if z value of previous k lies beyond the end of z-box
                else:
                    z_val[k] = r-k+1
                    # l and r remain the same
    
    # Step 2: Use Z suffix to get Good Suffix
    def good_suffix(z_suffix, gs, m):
        
        for i in range(m-1):
            gs[m-z_suffix[i]] = i+1
            
    def matched_prefix (z_val, mp, m):
        
        for i in range(m-1, 0, -1):
            # if z val is suffix then take it as mp, else copy from the next one
            if i + z_val[i] == m:
                mp[i] = z_val[i]
            else:
                mp[i] = mp[i+1]
                
        mp[0] = m
    
    m = len(pattern)
    z_suffix = [0] * m
    z_val = [0] * m
    gs = [0] *( m+1)
    mp = [0] * (m+1)
    
    gusfield(pattern[::-1], z_suffix)
    z_suffix = z_suffix[::-1]
    
    gusfield(pattern, z_val)
    # print(z_suffix)
    # print(z_val)
    
    good_suffix(z_suffix, gs, m)
    
    matched_prefix (z_val, mp, m)
    
    return gs, mp
    
    
    # # Step 3: Get Z values
    # z_values = z_suffix(pattern)
    
    # # Step 4: Use Z values to get matched prefix
    # matched_prefix = z_suffix(pattern[::-1])[::-1]
    
    # return z_values, matched_prefix

def boyermooregalils(text, pattern):
    
    output = []
    m, n = len(pattern), len(text)
    
    bc = preprocess_bad_char(pattern)
    # print("bc", bc)
    gs, mp = preprocess_good_suffix(pattern)
    print("gs", gs)
    print("mp", mp)    
    
    start, stop = -1, -1
    
    j = 0
    
    while j<=n-m:
        k = m-1
        
        print("start",start, "stop", stop, "j", j)
        
        
        while k>=0:
            print("k", k, "j+k", j+k)
            if k<=stop and k>=start:
                # CONFIRM IS MATCHED CHARACTER, skip comparison
                k -= 1
                continue
            else:
                # compare character
                print("compare", pattern[k], text[j+k])
                if pattern[k] == text[j+k]:
                    # MATCHED CHARACTER
                    k -= 1
                else:
                    # found a mismatch
                    break
        
        # while k>=0 and pattern[k] == text[j+k]:
        #     k -= 1
        print("k", k)
            
        if k<0:
            print("Pattern found at index: ", j+1)

            output.append(j+1)
            shift = (m - mp[1])
            j += shift
            stop = mp[1]if mp[1] else -1
            start = -1
            print("shift", shift, "stop", stop, "start", start)
            
        else:
            shiftbc = k - bc[k][ord(text[j+k])]
            print("shiftbc", shiftbc)
            
            
            print("gs[k+1]", gs[k+1], "mp[k+1]", mp[k+1], "k", k, "m", m)
            
            if gs[k+1]:
                shiftgs = m - gs[k+1]
                gsstop = gs[k+1]-1
                gsstart = gsstop - m + k + 2
                # update start and stop for good suffix
                print("gsstart", gsstart, "gsstop", gsstop, "shiftgs", shiftgs)
                
            else:
                shiftgs = m - mp[k+1]
                gsstart = -1
                gsstop = mp[k+1]-1
                # update start and stop for matched prefix
                print("gsstart", gsstart, "gsstop", gsstop, "shiftgs", shiftgs)
                
            
            if shiftbc > shiftgs:
                shift = shiftbc
            elif shiftbc <= shiftgs:
                shift = shiftgs
                # if k+1 <m:
                stop = gsstop
                start = gsstart
                    
            print("ultimate shift", shift)
            j += shift
            
    return output

# Example usage
# text = "dbcdbcdabdbcdabddbcdbcdabcb"
# pattern = "dbc"
# boyermooregalils(text, pattern)

text = "aaaaaaaaa"
pattern = "aaa"
boyermooregalils(text, pattern)

# text = "GEEKS FOR GEEKS"
# pattern = "GEEK"
# print(boyermooregalils(text, pattern))

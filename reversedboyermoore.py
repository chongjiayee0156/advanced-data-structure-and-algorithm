TOTAL_CHAR = 256

def preprocess_bad_char(pat):
    m = len(pat)
    
    bad_char_shift = [[-1]*TOTAL_CHAR for _ in range(m)]
    # store leftmost occurence of chaqracter c to the right of k
    
    # for i in range(m-1):
    #     char = ord(pat[i])
    #     bad_char_shift[i+1][char] = i 
        
    for i in range(m-1, 0, -1):
        char = ord(pat[i])
        bad_char_shift[i-1][char] = i
        
    for i in range(m-2, -1, -1):
        for j in range(TOTAL_CHAR):
            if bad_char_shift[i][j] == -1:
                bad_char_shift[i][j] = bad_char_shift[i+1][j]
    
    return bad_char_shift

def search(txt, pat):
    n = len(txt)
    m = len(pat)
    
    bad_char_shift = preprocess_bad_char(pat)
    
    j = n-m
    print("m: ", m, "n: ", n, "j: ", j, "txt[j]: ", txt[j], "pat: ", pat, "txt[j+m-1]: ", txt[j+m-1])
    while (j>=0):
        k = 0
        
        
        while (k<m) and (txt[j+k] == pat[k]):
            k += 1
            
        if k==m:
            print("Pattern found at index: ", j+1)
            j -= 1
        else:
            print("k: ", k)
            shift = max(bad_char_shift[k][ord(txt[j+k])]-k, 1)
            
            j -= shift
            
            print("shift: ", shift, "j: ", j)

text = "dbcdbcdabdbcdabddbcdbcdabcb"
pattern = "dbc"

search(text, pattern)

# print(preprocess_bad_char("acababacaba"))
TOTAL_CHAR = 256

def preprocess(pat):
    m = len(pat)
    
    bad_char_shift = [[-1]*TOTAL_CHAR for _ in range(m)]
    
    for i in range(m-1):
        
        char = ord(pat[i])
        print(pat[i], (i+1), char, i)
        bad_char_shift[i+1][char] = i 
        
    for i in range(1, m):
        for j in range(TOTAL_CHAR):
            if bad_char_shift[i][j] == -1:
                bad_char_shift[i][j] = bad_char_shift[i-1][j]
    
    return bad_char_shift

def search(txt, pat):
    n = len(txt)
    m = len(pat)
    
    bad_char_shift = preprocess(pat)
    print(bad_char_shift[2][100])
    
    j = 0
    while (j<=n-m):
        k = m-1
        
        while (k>=0) and (txt[j+k] == pat[k]):
            k -= 1
            
        if k<0:
            print("Pattern found at index: ", j+1)
            print(1)
            j += 1
        else:
            shift = k-bad_char_shift[k][ord(txt[j+k])]
            
            j += shift
            print(shift)

text = "dbcdbcdabdbcdabddbcdbcdabcb"
pattern = "dbc"

search(text, pattern)
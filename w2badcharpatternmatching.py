# # Python3 Program for Bad Character Heuristic
# # of Boyer Moore String Matching Algorithm

# NO_OF_CHARS = 256


# def badCharHeuristic(string, size):
# 	'''
# 	The preprocessing function for
# 	Boyer Moore's bad character heuristic
# 	'''

# 	# Initialize all occurrence as -1
# 	badChar = [-1]*NO_OF_CHARS

# 	# Fill the actual value of last occurrence
# 	for i in range(size):
# 		badChar[ord(string[i])] = i

# 	# return initialized list
# 	return badChar


# def search(txt, pat):
# 	'''
# 	A pattern searching function that uses Bad Character
# 	Heuristic of Boyer Moore Algorithm
# 	'''
# 	m = len(pat)
# 	n = len(txt)

# 	# create the bad character list by calling
# 	# the preprocessing function badCharHeuristic()
# 	# for given pattern
# 	badChar = badCharHeuristic(pat, m)

# 	# s is shift of the pattern with respect to text
# 	s = 0
# 	while(s <= n-m):
# 		j = m-1
# 		print(s)

# 		# Keep reducing index j of pattern while
# 		# characters of pattern and text are matching
# 		# at this shift s
# 		while j >= 0 and pat[j] == txt[s+j]:
# 			j -= 1

# 		# If the pattern is present at current shift,
# 		# then index j will become -1 after the above loop
# 		if j < 0:
# 			print("Pattern occur at index = {}".format(s))

# 			''' 
# 				Shift the pattern so that the next character in text
# 					aligns with the last occurrence of it in pattern.
# 				The condition s+m < n is necessary for the case when
# 				pattern occurs at the end of text
# 			'''
# 			s += (m-badChar[ord(txt[s+m])] if s+m < n else 1)
# 		else:
# 			'''
# 			Shift the pattern so that the bad character in text
# 			aligns with the last occurrence of it in pattern. The
# 			max function is used to make sure that we get a positive
# 			shift. We may get a negative shift if the last occurrence
# 			of bad character in pattern is on the right side of the
# 			current character.
# 			'''
# 			s += max(1, j-badChar[ord(txt[s+j])])


# # Driver program to test above function
# def main():
# 	txt = "ABAAABCD"
# 	pat = "ABC"
# 	search(txt, pat)


# if __name__ == '__main__':
# 	main()

# # This code is contributed by Atul Kumar
# # (www.facebook.com/atul.kr.007)



TOTAL_CHAR = 256

def preprocess_pat(pat):
    # O(256 + m) = O(m)
	bad_char_shift = [-1] * TOTAL_CHAR
	m = len(pat)
	for i in range(m):
		bad_char_shift[ord(pat[i])] = i
  
	return bad_char_shift
  
def search(txt, pat):
    
    
    bad_char_shift = preprocess_pat(pat) #o(m)
    
    n = len(txt)
    m = len(pat)
    
    # loop through 0 to n-m+1
    # j is pointer in txt from left to right
    j = 0
    while (j<=n-m):
        
        # k is pointer in pat from right to left
        k = m-1
        
        # find the first mismatch
        while k>=0 and txt[j+k] == pat[k]:
            k -= 1
            
        if k<0:
            # found a matching pattern
            #  print 1-based index
            print("Pattern found at index: ", j+1)
            
            # shift the pattern to the right by the rightmost occurence of 
            j += 1
            
        else:
            # bad character is met
            # shift the pattern to the right by the max of 1 and the 
            # difference between the current position and the rightmost occurence of the bad character in pat
            # k-R(x) where x is the bad character in txt
            
            j += max(1, k-bad_char_shift[ord(txt[j+k])])
        

text = "dbcdbcdabdbcdabddbcdbcdabcb"
pattern = "dbc"
# i 4 10 17 20

search(text, pattern)

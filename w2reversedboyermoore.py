TOTAL_CHAR = 130

def preprocess_bad_char(pat):
    
    """
    Preprocesses the bad character shift table for reversed Boyer-Moore algorithm.
    Find reversed Rk(x) for each character in txt and pattern.
    
    Definition of reversed Rk(x):
    Store leftmost occurence of character c to the RIGHT of k
    Default value is set to -1
    
    Time complexity: O(m*TOTAL_CHAR) = O(m)
    
    Space complexity: O(m*TOTAL_CHAR)
    
    Args:
        pat (str): The pattern string.
        
    Returns:
        list: A 2D list representing the bad character shift table.
    """
    
    m = len(pat)
    
    # create the 2D bad char shift table
    bad_char_shift = [[-1]*TOTAL_CHAR for _ in range(m)]
    
    # Populate the bad character shift table by iterating through the pattern
    for i in range(m-1, 0, -1):
        # add the index of current character (x) as value of column x at row k
        char = ord(pat[i])
        bad_char_shift[i-1][char] = i
        
    # Fill in the rest of the table with the leftmost occurence of each character
    for i in range(m-2, -1, -1):
        for j in range(TOTAL_CHAR):
            # if the current cell is empty, fill it with the value of the cell below it
            # to maintain the leftmost occurence of each character (greedy method)
            if bad_char_shift[i][j] == -1:
                bad_char_shift[i][j] = bad_char_shift[i+1][j]
    
    return bad_char_shift


def preprocess_good_prefix(pattern):
    """
    Preprocesses the good prefix and matched suffix arrays for Galil's optimization.
    
    This function operates on 0-based index.
    
    Step1: Find z array
    Step2: use it to evalue to find good prefix for [-1 ... m-1] 
    Step3: Find z suffix
    Step4: use it to evaluate matched suffix for [-1 ... m-1]
    
    An extra element to the left is needed because we're referring to gp(k-1) and mp(k-1) 
    when a mismatch in k occurs in the algorithm.
    
    Time complexity: O(m)
    
    Args:
        pattern (str): The pattern string.
        
    Returns:
        tuple: A tuple containing the good prefix and matched suffix tables.
    """
    

    def compare_explicitly(string, k, z=None):
        
        """
        Compares characters explicitly between two positions in a string.
        Used to find the z value / z suffix of a character.
        
        Args:
            string (str): The string to compare.
            k (int): The starting index of substring to compare.
            z (int, optional): The starting index of another substring to compare with. Defaults to None.
            
        Returns:
            int: The count of matching characters.
        """
        count = 0
        
        # compare k with z, z is set to prefix index if not explicitly mentioned
        s = 0 if z is None else z
        
        while k<len(string) and string[k] == string[s]:
            count += 1
            k += 1
            s += 1
            
        return count

    def gusfield(string, z_val):
        """
        Constructs the Z array for a given string.
        
        z_val[i]: length of longest substring starting from i which is also a prefix of string
        
        Time complexity: O(m)
        
        Args:
            string (str): The string to analyze.
            z_val (list): The list to store Z values.
        """
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
                # case 2a: z value of previous k lies within z-box (z_val[k-left] < -k+1)
                if z_val[k-l] < r-k+1:
                    # its z value is the same as z value of k-left
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
    def good_prefix_generator(z_val, gp, m):
        """
        This function constructs the good prefix array using the Z values obtained from the Z array.
        
        Gp[i]: index of next occurence of substring (to the right of i) that matches prefix from 0..i
        
        Uses 0-based index implementation.
        
        Time complexity: O(m)
        
        Args:
            z_val (list): The list containing Z values.
            gp (list): The list to store the good prefix array.
            m (int): The length of the pattern.
        """
        # loop from right to left of z value to get the leftmost occurence of prefix
        for i in range(m-1, 0, -1):
            gp[z_val[i]] = i
            
    def matched_suffix_generator (z_suffix, ms, m):
        """
        This function constructs the matched suffix array using the Z suffix array.
        
        ms[i]: longest prefix from [1..i] (good prefix) that matches suffix of pattern
        
        Time complexity: O(m)
        
        Args:
            z_suffix (list): The list containing Z suffix values.
            ms (list): The list to store the matched suffix array.
            m (int): The length of the pattern.
        """
        
        # loop though each z suffix, if it is a prefix, means it is a 
        # prefix which also matches the suffix, so we store it as matched suffix             
        for i in range(m):
            if z_suffix[i] == i+1:
            # dont need to compare with the previous matched suffix to find the max length of valid prefix
            # as valid prefix will only get longer as you move to the right
                ms[i+1] = z_suffix[i]
            else:
        # if it is not a prefix, we copy ms from the previous one
                ms[i+1] = ms[i]
                
        ms[m] = m
    
    m = len(pattern)
    z_val = [0] * m  # Initialize Z values
    good_prefix = [0] * (m + 1)  # Initialize good prefix array
    z_suffix = [0] * m  # Initialize Z suffix values
    matched_suffix = [0] * (m + 1)  # Initialize matched suffix array
      
    # Calculate Z suffix values by revrsing pattern as input and reversing its output
    gusfield(pattern[::-1], z_suffix)
    z_suffix = z_suffix[::-1]
    
    # Calculate Z values for the pattern
    gusfield(pattern, z_val)
    
    # Generate the good prefix array
    good_prefix_generator(z_val, good_prefix, m)
    
    # Generate the matched suffix array
    matched_suffix_generator(z_suffix, matched_suffix, m)
    
    return good_prefix, matched_suffix


def reversed_boyermoore_galils(text, pattern):
    """
    Applies the reversed Boyer-Moore's algorithm to find all occurrences of a pattern in a text.
    
    Implemented using galil's optimization, extended bad character rule and good "prefix" rule. 
    (Changed name since it is reversed)
    Use galil's optimazation while comparing text and pattern, when a mismatch is found, use bad 
    char and good prefix rule to determine the maximum number of shift
    
    Worst case time complexity: O(m+n)
        - m: length of pattern
        - n: length of text
        - Galil's optimizationa allow us the skip the comparison of the pattern and text when we 
        know the character is already matched
        - Hence, max comparison btw text and pat is o(n)
        - preprocessing the pattern requires calculating the z value and z suffix, which is O(m)
        - Other than that, there are some loops / list initialization that are O(m) or O(n)
    
    Definition of reversed Boyer-Moore:
    Boyer-Moore that runs in the opposite direction, where the pattern is shifted leftwards 
    under the text between iterations,
    from the rightmost end of the text towards the left. 
    While doing so, in each iteration the scanning of characters between pattern and text proceeds 
    from left to right. Specifically, in the first iteration, pat[1 ...m] and txt[n 

    Args:
        text (str): The text string to search in.
        pattern (str): The pattern string to search for.

    Returns:
        str: A string containing the indices of all occurrences of the pattern in the text.
            If no occurrences are found, an empty string is returned.
    """
    
    # conduct input validation
    assert len(text) >= len(pattern), "Pattern length should be less than or equal to text length"
    if len(pattern) == 0:
        return []
    
    output = []  # Initialize list to store indices of pattern occurrences
    m, n = len(pattern), len(text)  # Lengths of pattern and text

    bc = preprocess_bad_char(pattern)  # Preprocess bad character shift table
    gp, ms = preprocess_good_prefix(pattern)  # Preprocess good prefix and matched suffix tables

    start, stop = m, m  # Initialize start and stop indices

    j = n - m  # Initialize index for pattern comparison in text

    while j >= 0:
        k = 0  # Initialize index for pattern comparison

        while k < m:
            if k <= stop and k >= start:
                # Skip comparison if character is confirmed to be matched
                k += 1
                continue
            else:
                # Compare characters
                if pattern[k] == text[j + k]:
                    # Increment index if characters match
                    k += 1
                else:
                    # Found a mismatch, exit loop
                    break
            
        if k == m:
            # Pattern found at index j+1
            output.append(j + 1)

            # Update start and stop indices for next iteration
            shift = m - ms[m - 1]
            j -= shift
            stop = m
            start = m - ms[m - 1]
                    
        else:
            # determine shift based on bad char and good prefix rule
            # update bad char start and stop based on bad char value
            
            # if no occurence of bad char to the right of k
            if bc[k][ord(text[j+k])] == -1:
                # shift everything pass bad char, hence we cannot guarantee 
                # any character matches in next comparison
                shiftbc = m
                bcstart = m
                bcstop = m
            else:
                # else, we shift so that the bad character matches its nxt occurence in pat,
                # we can update start and stop so that we skip comparing this position in the next iteration
                shiftbc = bc[k][ord(text[j+k])]-k
                bcstart = bc[k][ord(text[j+k])]
                bcstop = bc[k][ord(text[j+k])]
                
                   
            if gp[k]:
                # if gp[k] > 0 
                # Since gp has one element more than pat, gp[k] is actually gp[k-1] 
                # which means the gp of last matching character in the matched prefix
                shiftgs = gp[k]
                gpstart = gp[k]
                # error prevention in case k is too small
                gpstop = max(gpstart + k - 1, gpstart)
                
                
            else:
                # else, find matched suffix
                shiftgs = m - ms[k]
                # update start and stop for matched prefix
                gpstop = m
                gpstart = m - ms[k]
                
            # calculate the u;timate shift and start stop by comparing resuly of shift by bc and ms  
            if shiftbc > shiftgs:
                shift = shiftbc
                stop = bcstop
                start = bcstart
            elif shiftbc <= shiftgs:
                shift = shiftgs
                stop = gpstop  
                start = gpstart
                    
            j -= shift
            
    return "\n".join(map(str, output))


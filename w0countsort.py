def counting_sort(arr):
    # Find the maximum element in the array
    max_element = max(arr)
    
    # Create a count array to store the count of each element
    count = [0] * (max_element + 1)
    
    # Count the occurrences of each element
    for num in arr:
        count[num] += 1
        
    print(f"Count array: {count}")
    
    # Modify the count array to store the position of each element in the sorted array
    for i in range(1, max_element + 1):
        count[i] += count[i - 1]
        
    print(f"Count array: {count}")
    
    # Create a temporary array to store the sorted elements
    sorted_arr = [0] * len(arr)
    
    # Build the sorted array by placing each element in its correct position
    for num in arr:
        print(f"num: {num}, count[num]: {count[num]}")
        sorted_arr[count[num] - 1] = num
        count[num] -= 1
        print(f"sorted_arr: {sorted_arr}, count: {count}")
    
    return sorted_arr

# Example usage:
arr = [4, 2, 2, 8, 3, 3, 1]
sorted_arr = counting_sort(arr)
print("Sorted array:", sorted_arr)

# Count array: [0, 1, 2, 2, 1, 0, 0, 0, 1]
# Count array: [0, 1, 3, 5, 6, 6, 6, 6, 7]
# num: 4, count[num]: 6
# sorted_arr: [0, 0, 0, 0, 0, 4, 0], count: [0, 1, 3, 5, 5, 6, 6, 6, 7]
# num: 2, count[num]: 3
# sorted_arr: [0, 0, 2, 0, 0, 4, 0], count: [0, 1, 2, 5, 5, 6, 6, 6, 7]
# num: 2, count[num]: 2
# sorted_arr: [0, 2, 2, 0, 0, 4, 0], count: [0, 1, 1, 5, 5, 6, 6, 6, 7]
# num: 8, count[num]: 7
# sorted_arr: [0, 2, 2, 0, 0, 4, 8], count: [0, 1, 1, 5, 5, 6, 6, 6, 6]
# num: 3, count[num]: 5
# sorted_arr: [0, 2, 2, 0, 3, 4, 8], count: [0, 1, 1, 4, 5, 6, 6, 6, 6]
# num: 3, count[num]: 4
# sorted_arr: [0, 2, 2, 3, 3, 4, 8], count: [0, 1, 1, 3, 5, 6, 6, 6, 6]
# num: 1, count[num]: 1
# sorted_arr: [1, 2, 2, 3, 3, 4, 8], count: [0, 0, 1, 3, 5, 6, 6, 6, 6]
# Sorted array: [1, 2, 2, 3, 3, 4, 8]

def count_sort(bwt):
    max_ord = 127
    position = [0] * (max_ord + 1)
    for char in bwt:
        position[ord(char)] += 1
    for i in range(1, max_ord + 1):
        position[i] += position[i-1]
        
    rank = [0] * 127
    for i in range(1, max_ord + 1):
        rank[i] = position[i-1]
        
    return rank
    # sorted_bwt = [0] * len(bwt)
    
    # for i, char in enumerate(bwt):
    #     sorted_bwt[position[ord(char)]-1] = char
    #     position[ord(char)] -= 1
    # return "".join(sorted_bwt)
    


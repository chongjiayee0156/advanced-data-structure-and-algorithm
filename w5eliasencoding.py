import bitarray

def elias_omega_encode(n: int) -> str:
    output = bitarray.bitarray()
    minimal_binary_code = bin(n)[2:]
    output.extend(minimal_binary_code)
    
    n = len(minimal_binary_code) - 1
        
    while n>0:
        binary_code = bin(n)[2:]
        
        n = len(binary_code)-1
        
        # make most significant bit 0
        musk = bitarray.bitarray(len(binary_code))
        musk[0] = 1
        musk = ~musk
        
        binary_code = bitarray.bitarray(binary_code)
        binary_code = binary_code & musk
        
        output = binary_code + output
    
    return output

def elias_omega_decode(encoded: bitarray) -> int:
    pointer = 0
    length = 1
    
    while encoded[pointer] == 0:
        new_length = encoded[pointer: pointer + length]
        
        # switch new length most significant bit to 1
        new_length[0] = 1
        
        # change new_length to integer
        new_length = int(new_length.to01(), 2)
        new_length += 1
        
        # update pointer and length
        pointer = pointer + length
        length = new_length
        
    component = encoded[pointer: pointer + length]
    component = int(component.to01(), 2)
    return component
    

# for i in range(1, 17):
#     oo = elias_omega_encode(i)
#     print(f'{i}: {elias_omega_encode(i)}')
    
#     print(elias_omega_decode(oo))
import os

x = bitarray.bitarray(elias_omega_encode(32))
print(x, len(x))

# Write code to output file
output_file_path = "elias_code.bin"
with open(output_file_path, "wb") as file:
    file.write(x)

# Get file size
file_size = os.path.getsize(output_file_path)
print("File size:", file_size, "bytes")

# pad 0 to the end make it multiple of 8
x = x + bitarray.bitarray((8 - len(x) % 8) % 8)
print(x, len(x))
# Write code to output file
with open(output_file_path, "wb") as file:
    file.write(x)

# Get file size
file_size = os.path.getsize(output_file_path)
print("File size:", file_size, "bytes")
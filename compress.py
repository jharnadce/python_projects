# Import package for compressing files
import zlib
# import library to encode compressed data
import base64


def compress(input_file, output_file):
    input_data = open(input_file, 'r').read()
    # Convert string into bytes
    data_bytes = bytes(input_data, 'utf-8')
    
    # Compress the bytes data and encode
    compressed_bytes = base64.b64encode(zlib.compress(data_bytes, level=9))
    
    # Decode the bytes data into string so that it can be written to a file
    decoded_data = compressed_bytes.decode('utf-8')
    
    compressed_file = open(output_file, 'w')
    compressed_file.write(decoded_data)
    compressed_file.close()
    
    
def decompress(input_file, output_file):

    decoded_data = open(input_file, 'r').read()
    # convert the string data into bytes
    decoded_bytes = bytes(decoded_data, 'utf-8')
    # Reverse the compression steps
    # Decode compressed data in string format into bytes, then decompress
    # print(base64.b64decode(compressed_data))
    decompressed_bytes = zlib.decompress(base64.b64decode(decoded_bytes))

    # Convert bytes data into string
    decompressed_data = decompressed_bytes.decode('utf-8')
    
    # Write to file
    decompressed_file = open(output_file, 'w')
    decompressed_file.write(decompressed_data)
    decompressed_file.close()


# # Step 1: Read input file, compress and write to file


# compress(input_file="file_compressor_app/demo.txt", 
#          output_file="file_compressor_app/compressed.txt")


# # Step 2: Read compressed data file, decompress and write to file 


# decompress(input_file="file_compressor_app/compressed.txt", 
#            output_file="file_compressor_app/decompressed_data.txt")

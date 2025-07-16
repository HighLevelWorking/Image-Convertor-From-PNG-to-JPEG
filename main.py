import os
import zlib

storage = b""
image = None
varification = None
data = None
chunktype = None
width = None
height = None
bit_depth = None
color_type = None
bit_per_pixel = None

def decompression():
    global storage
    Storage_taken = zlib.decompress(storage)
    return(Storage_taken)

def idat_chunk_checker():
    global storage
    if chunktype == b'IDAT':
        print("IDAT chunk found. Processing...")
        storage += data
        return storage

def image_chooser():
    global image
    image = open(r"C:\Users\highl\OneDrive\Pictures\Screenshots\Screenshot 2025-07-14 201528.png", "rb")


def ihdr_checker(length):
    global width, height, bit_depth, color_type, bit_per_pixel
    if chunktype == b'IHDR' and length == 13:
        print("IHDR chunk found. Processing...")
        ihdr_data = data
        width = int.from_bytes(ihdr_data[0:4], 'big')
        height = int.from_bytes(ihdr_data[4:8], 'big')
        bit_depth = ihdr_data[8]
        color_type = ihdr_data[9]
        bit_per_pixel = color_type * bit_depth
        print(f"Image Width: {width}, Height: {height}, Bit Depth: {bit_depth}, Color Type: {color_type}, Bits per Pixel: {bit_per_pixel}")

def signature_checking():
    global varification
    varification = image.read(8)
    expected_signature = b'\x89PNG\r\n\x1a\n'
    if varification != expected_signature:
        print("Invalid image signature. Not a correct png file.")
    else:
        print("Image signature is valid. Proceeding with the image.")

def image_opener():
    os.system("explorer C:\\Users\\highl\\OneDrive\\Pictures\\Screenshots\\Screenshot 2025-07-14 201528.png")

def convert_to_jpg():
    # Placeholder for conversion logic
    pass

def main():
    global data, chunktype
    image_chooser()
    signature_checking()
    while True:
        #length tells how big the data chunk is lmao
        length = image.read(4)
        if not length:
            break
        chunktype = image.read(4)
        length_checker = int.from_bytes(length, 'big')
        data = image.read(length_checker)
        ihdr_checker(length_checker)
        idat_chunk_checker()
        crc = image.read(4)    
    decompression()

if __name__ == "__main__":
    main()
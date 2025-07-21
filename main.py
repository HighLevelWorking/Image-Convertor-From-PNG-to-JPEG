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
        if color_type == 0:   # Grayscale
            channels = 1
        elif color_type == 2: # RGB
            channels = 3
        elif color_type == 3: # Indexed
            channels = 1
        elif color_type == 4: # Grayscale + Alpha
            channels = 2
        elif color_type == 6: # RGBA
            channels = 4
        else:
            raise ValueError("Unsupported color type")
        bit_per_pixel = channels * bit_depth
        print(f"Image Width: {width}, Height: {height}, Bit Depth: {bit_depth}, Color Type: {color_type}, Bits per Pixel: {bit_per_pixel}")

def signature_checking():
    global varification
    varification = image.read(8)
    expected_signature = b'\x89PNG\r\n\x1a\n'
    if varification != expected_signature:
        print("Invalid image signature. Not a correct png file.")
    else:
        print("Image signature is valid. Proceeding with the image.")

def unfiltering(decom_data):
    global width, height, bit_per_pixel
    bytes_per_pixel = bit_per_pixel // 8
    filtered_data = b""
    index = 0
    scanline_bytes = 1 + (width * bytes_per_pixel)
    prev_scanline = bytearray([0] * (width * bytes_per_pixel))

    for i in range(height):
        if index + scanline_bytes > len(decom_data):
            raise ValueError("Scanline exceeds available data.")

        filter_byte = decom_data[index]
        rest = decom_data[index + 1:index + scanline_bytes]

        if filter_byte == 0:
            print("Filter 0 (None) applied")
            filtered_data += rest

        elif filter_byte == 1:
            print("Filter 1 (Sub) applied")
            recon = bytearray()
            for x in range(len(rest)):
                left = recon[x - bytes_per_pixel] if x >= bytes_per_pixel else 0
                val = (rest[x] + left) % 256
                recon.append(val)
            filtered_data += bytes(recon)
            
        elif filter_byte == 2:
            print("Filter 2 (Up) applied")
            recon = bytearray()
            for x in range(len(rest)):
                above = prev_scanline[x] if prev_scanline else 0
                val = (rest[x] + above) % 256
                recon.append(val)
            filtered_data += bytes(recon)
            prev_scanline = recon

        elif filter_byte == 3:
            print("Filter 3 (Average) applied")
            recon = bytearray()
            for d in range(len(rest)):
                left = recon[d - bytes_per_pixel] if d >= bytes_per_pixel else 0
                above = prev_scanline[d] if prev_scanline else 0
                avg = (left + above)//2
                val = (rest[d]+avg) % 256
                recon.append(val)
            filtered_data += bytes(recon)
            prev_scanline = recon

        elif filter_byte == 4:
            print("Filter 4 (Paeth) applied")
            recon = bytearray()
            for z in range(len(rest)):
                left = recon[z - bytes_per_pixel] if z >= bytes_per_pixel else 0
                above = prev_scanline[z] if prev_scanline else 0
                upper_left = prev_scanline[z-bytes_per_pixel] if (z >= bytes_per_pixel and prev_scanline) else 0

                p = left + above - upper_left
                pa = abs(p - left)
                pb = abs(p - above)
                pc = abs(p - upper_left)

                if pa <= pb and pa <= pc:
                    predictor = left
                elif pb <= pc:
                    predictor = above
                else:
                    predictor = upper_left
                val = (rest[z] + predictor) % 256
                recon.append(val)
            filtered_data += bytes(recon)
            prev_scanline  = recon

        index += scanline_bytes
    return filtered_data



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
    values_of_decompression = decompression()
    raw_pixels = unfiltering(values_of_decompression)

if __name__ == "__main__":
    main()
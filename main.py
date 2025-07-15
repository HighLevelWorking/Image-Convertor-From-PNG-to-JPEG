import os

image = None
varification = None
data = None
chunktype = None

def chunk():
    None

def image_chooser():
    global image
    image = open(r"C:\Users\highl\OneDrive\Pictures\Screenshots\Screenshot 2025-07-14 201528.png", "rb")


def ihdr_checker():
    pass
    #if chunktype == b'IHDR':
        #if len(data) == 13:
        #    print("This follows the specifications to be a PNG file.")
        #else:
        #    print("This does not follow the specifications to be a PNG file. It doesn't have a valid IHDR format.")

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
        length = image.read(4)
        checker = str(length)
        if checker == "":
            break
        chunktype = image.read(4)
        ihdr_checker()
        crc = image.read(4)    
    #image_opener()
    #print("Image opened successfully.")


if __name__ == "__main__":
    main()
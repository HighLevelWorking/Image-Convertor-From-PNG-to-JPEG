import os

image = None
varification = None
chunktype, data, crc, length = None, None, None, None

def chunk():
    None


def image_chooser():
    global image
    image = open(r"C:\Users\highl\OneDrive\Pictures\Screenshots\Screenshot 2025-07-14 201528.png", "rb")


def reader():
        global chunktype, data, crc, length
        length = image.read(4)
        chunktype = image.read(4)
        data = image.read(13)
        crc = image.read(4)

def ihdr_checker():
    if len(data) == 13:
        print("This follows the specifications to be a PNG file.")
    else:
        print("This does not follow the specifications to be a PNG file. It doesn't have a valid IHDR format.")

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
    image_chooser()
    signature_checking()
    while image != EOFError:
        ihdr_checker()
        reader()
    #image_opener()
    #print("Image opened successfully.")


if __name__ == "__main__":
    main()
import os

image = None
varification = None

def chunk():
    None

def image_chooser():
    global image
    global varification
    image = open(r"C:\Users\highl\OneDrive\Pictures\Screenshots\Screenshot 2025-07-14 201528.png", "rb")
    varification = image.read(8)


def signature_checking():
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
    #image_opener()
    #print("Image opened successfully.")


if __name__ == "__main__":
    main()
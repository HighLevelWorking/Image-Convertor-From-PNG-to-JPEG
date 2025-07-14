import os

image = None

def image_chooser():
    global image
    image = open(r"C:\Users\highl\OneDrive\Pictures\Screenshots\Screenshot 2025-07-14 201528.png", "rb")

def image_opener():
    os.system("explorer C:\\Users\\highl\\OneDrive\\Pictures\\Screenshots\\Screenshot 2025-07-14 201528.png")

def convert_to_jpg():
    # Placeholder for conversion logic
    pass

def main():
    image_chooser()
    image_opener()
    print("Image opened successfully.")
    print(image.read())


if __name__ == "__main__":
    main()
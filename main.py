import os
import zlib

storage = b""
image = None
verification = None
data = None
chunktype = None

# Will be filled by IHDR
width = None
height = None
bit_depth = None
color_type = None
bit_per_pixel = None

def decompression():
    global storage
    return zlib.decompress(storage)

def idat_chunk_checker():
    global storage
    if chunktype == b'IDAT':
        print("IDAT chunk found. Processing...")
        storage += data

def image_chooser():
    global image
    image = open(r"C:\Users\highl\OneDrive\Pictures\Screenshots\Screenshot 2025-07-14 201528.png", "rb")

def ihdr_checker(length):
    global width, height, bit_depth, color_type, bit_per_pixel
    if chunktype == b'IHDR' and length == 13:
        print("IHDR chunk found. Processing...")
        ihdr_data   = data
        width       = int.from_bytes(ihdr_data[0:4], 'big')
        height      = int.from_bytes(ihdr_data[4:8], 'big')
        bit_depth   = ihdr_data[8]
        color_type  = ihdr_data[9]
        # Determine channels
        if color_type == 0:   channels = 1   # Grayscale
        elif color_type == 2: channels = 3   # RGB
        elif color_type == 3: channels = 1   # Indexed
        elif color_type == 4: channels = 2   # Grayscale+Alpha
        elif color_type == 6: channels = 4   # RGBA
        else:
            raise ValueError(f"Unsupported color type: {color_type}")
        bit_per_pixel = channels * bit_depth
        print(f"→ Width={width}, Height={height}, BitDepth={bit_depth}, ColorType={color_type}, BitsPerPixel={bit_per_pixel}")

def signature_checking():
    global verification
    verification = image.read(8)
    if verification != b'\x89PNG\r\n\x1a\n':
        print("Invalid PNG signature.")
        raise SystemExit
    print("Valid PNG signature.")

def unfiltering(decom_data):
    global width, height, bit_per_pixel
    bpp = bit_per_pixel // 8
    recon_bytes = bytearray()
    prev_line   = bytearray(width * bpp)
    idx = 0
    scanlen = 1 + width * bpp

    for row in range(height):
        if idx + scanlen > len(decom_data):
            raise ValueError("Corrupt: scanline too long.")
        f = decom_data[idx]
        chunk = decom_data[idx+1 : idx+scanlen]

        if f == 0:
            print("Filter 0 (None)")
            recon = chunk
        elif f == 1:
            print("Filter 1 (Sub)")
            recon = bytearray()
            for i, v in enumerate(chunk):
                left = recon[i - bpp] if i >= bpp else 0
                recon.append((v + left) & 0xFF)
        elif f == 2:
            print("Filter 2 (Up)")
            recon = bytearray((chunk[i] + prev_line[i]) & 0xFF for i in range(len(chunk)))
        elif f == 3:
            print("Filter 3 (Average)")
            recon = bytearray()
            for i, v in enumerate(chunk):
                left  = recon[i - bpp] if i >= bpp else 0
                above = prev_line[i]
                recon.append((v + ((left + above)//2)) & 0xFF)
        elif f == 4:
            print("Filter 4 (Paeth)")
            recon = bytearray()
            for i, v in enumerate(chunk):
                left    = recon[i - bpp] if i >= bpp else 0
                above   = prev_line[i]
                upleft  = prev_line[i - bpp] if i >= bpp else 0
                p = left + above - upleft
                pa, pb, pc = abs(p-left), abs(p-above), abs(p-upleft)
                pred = left if pa<=pb and pa<=pc else (above if pb<=pc else upleft)
                recon.append((v + pred) & 0xFF)
        else:
            raise ValueError(f"Unknown filter {f}")

        recon_bytes.extend(recon)
        prev_line = recon
        idx += scanlen

    return bytes(recon_bytes)

def structured_pixel_data(raw):
    global color_type, bit_per_pixel, width, height
    # support 0,2,4,6 by dropping any alpha
    if color_type not in (0,2,4,6):
        print(f"Unsupported color type: {color_type}")
        return None

    bpp = bit_per_pixel // 8
    rowlen = width * bpp
    pixels = []

    for y in range(height):
        row_start = y * rowlen
        row = []
        for x in range(0, rowlen, bpp):
            px = raw[row_start + x : row_start + x + bpp]
            if color_type == 0:
                row.append((px[0],))
            else:
                # RGB, Gray+Alpha, or RGBA → drop alpha if present
                row.append((px[0], px[1], px[2]))
        pixels.append(row)

    print(f"Structured: {len(pixels)} rows × {len(pixels[0])} cols (first pixel: {pixels[0][0]})")
    return pixels

def rgb_to_ycbcr(pixels):
    h, w = len(pixels), len(pixels[0])
    for i in range(h):
        for j in range(w):
            pix = pixels[i][j]
            # debug each pixel format
            print(f"rgb_to_ycbcr() → pixel[{i},{j}] = {pix}")
            r, g, b = pix
            y  =  0.299*r + 0.587*g + 0.114*b
            cb = -0.168736*r - 0.331264*g + 0.5*b + 128
            cr =  0.5*r - 0.418688*g - 0.081312*b + 128
            pixels[i][j] = (int(round(y)), int(round(cb)), int(round(cr)))
    print("RGB→YCbCr conversion completed for all pixels.")
    return pixels

def subsample_420(pixels):
    height = len(pixels)
    width = len(pixels[0])

    Y  = [[0]*width for _ in range(height)]
    Cb = [[0]*((width+1)//2) for _ in range((height+1)//2)]
    Cr = [[0]*((width+1)//2) for _ in range((height+1)//2)]

    # Fill Y channel
    for i in range(height):
        for j in range(width):
            y_val, _, _ = pixels[i][j]
            Y[i][j] = y_val

    # Subsample Cb and Cr channels (2x2 average)
    for i in range(0, height, 2):
        for j in range(0, width, 2):
            cb_sum = cr_sum = count = 0
            for di in range(2):
                for dj in range(2):
                    ni, nj = i + di, j + dj
                    if ni < height and nj < width:
                        _, cb_val, cr_val = pixels[ni][nj]
                        cb_sum += cb_val
                        cr_sum += cr_val
                        count += 1
            out_i = i // 2
            out_j = j // 2
            Cb[out_i][out_j] = cb_sum // count
            Cr[out_i][out_j] = cr_sum // count

    print("Chroma subsampling (4:2:0) completed.")
    return Y, Cb, Cr



def main():
    global data, chunktype
    image_chooser()
    signature_checking()

    # Read PNG chunks
    while True:
        length = image.read(4)
        if not length:
            break
        chunktype   = image.read(4)
        size        = int.from_bytes(length, 'big')
        data        = image.read(size)
        ihdr_checker(size)
        idat_chunk_checker()
        _crc        = image.read(4)

    # Decompress + defilter
    decompressed = decompression()
    raw_pixels   = unfiltering(decompressed)

    # Build pixel matrix
    structured = structured_pixel_data(raw_pixels)
    if structured is None:
        print("Cannot proceed: unsupported color type.")
        return

    print("Calling RGB→YCbCr converter…")
    _ = rgb_to_ycbcr(structured)
    y, cb, cr = subsample_420(structured)

if __name__ == "__main__":
    main()

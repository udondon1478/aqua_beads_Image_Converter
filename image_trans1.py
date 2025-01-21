from PIL import Image, ImageDraw
import math

def create_hexagon(size):
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.radians(angle_deg)
        x = size * math.cos(angle_rad)
        y = size * math.sin(angle_rad)
        points.append((x, y))
    return points

def dottify_hexagon(image_path, num_rows, hexagon_size, spacing, black_threshold=30): # Added black_threshold
    img = Image.open(image_path)
    input_width, input_height = img.size

    hex_width = hexagon_size * 2
    hex_height = int(hexagon_size * math.sqrt(3))

    num_cols = int(math.ceil(num_rows * (hex_width / hex_height)))
    num_cols = (num_cols // 2) * 2 + (num_cols % 2)

    output_width = num_cols * (hexagon_size * 2 + spacing)
    output_height = num_rows * (hex_height + spacing)

    honeycomb = Image.new("RGB", (output_width, output_height), "white")
    draw = ImageDraw.Draw(honeycomb)

    x_scale = input_width / output_width
    y_scale = input_height / output_height

    for y in range(num_rows):
        for x in range(num_cols):
            center_x = x * (hexagon_size * 2 + spacing) + hexagon_size
            center_y = y * (hex_height + spacing) + hex_height // 2
            if y % 2 != 0:
                center_x += hexagon_size + spacing // 2

            input_x = int(center_x * x_scale)
            input_y = int(center_y * y_scale)

            input_x = max(0, min(input_x, input_width - 1))
            input_y = max(0, min(input_y, input_height - 1))

            color = img.getpixel((input_x, input_y))

            # Convert near-black pixels to white
            if sum(color) < black_threshold * 3: #Check if the sum of RGB is below the threshold
                color = (255, 255, 255)

            points = [(center_x + p[0], center_y + p[1]) for p in create_hexagon(hexagon_size)]
            draw.polygon(points, fill=color)

    return honeycomb

num_rows = 19
best_honeycomb = None
best_resolution = 0

for hexagon_size in range(10, 31, 5):
    for spacing in range(1, 16):
        honeycomb = dottify_hexagon("input.jpg", num_rows, hexagon_size, spacing)
        honeycomb.thumbnail((int(honeycomb.width * 0.4), int(honeycomb.height * 0.4)), Image.ANTIALIAS) #縮小処理
        resolution = honeycomb.width * honeycomb.height
        if resolution > best_resolution:
            best_resolution = resolution
            best_honeycomb = honeycomb

if best_honeycomb:
    best_honeycomb.save("honeycomb_hexagon_optimized.png")
else:
    print("No suitable honeycomb found.")
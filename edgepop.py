from PIL import Image, ImageDraw, ImageFilter
from math import sqrt

SPECIAL_SAUCE = 3

# Load image:
input_image = Image.open("inputs/x.jpg")
smoothed_input = input_image.filter(ImageFilter.GaussianBlur(radius=SPECIAL_SAUCE))
input_pixels = smoothed_input.load()

# Calculate pixel intensity as the average of red, green and blue colors.
intensity = [[sum(input_pixels[x, y]) / 3 for y in range(smoothed_input.height)] for x in range(smoothed_input.width)]

# Sobel kernels
kernelx = [[-1, 0, 1],
           [-2, 0, 2],
           [-1, 0, 1]]
kernely = [[-1, -2, -1],
           [0, 0, 0],
           [1, 2, 1]]



# Create output image
output_image = Image.new("RGBA", smoothed_input.size)

draw = ImageDraw.Draw(output_image)

# Compute convolution between intensity and kernels
for x in range(1, smoothed_input.width - 1):
    for y in range(1, smoothed_input.height - 1):
        magx, magy = 0, 0
        for a in range(3):
            for b in range(3):
                xn = x + a - 1
                yn = y + b - 1
                magx += intensity[xn][yn] * SPECIAL_SAUCE * kernelx[a][b]
                magy += intensity[xn][yn] * SPECIAL_SAUCE * kernely[a][b]

        # Draw in black and white the magnitude
        color = int(sqrt(magx**2 + magy**2))
        draw.point((x, y), (color, color, 0, color))

output_image.save("edges/xedge.png")

input_image.paste(output_image, (0, 0), output_image);
input_image.save("results/x.png");

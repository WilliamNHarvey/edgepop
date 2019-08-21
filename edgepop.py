from PIL import Image, ImageDraw, ImageFilter
from math import sqrt
import argparse
import ntpath

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="input image name", required=True)
parser.add_argument("-r", "--red", type=float, help="percent red", default=1.0)
parser.add_argument("-g", "--green", type=float, help="percent green", default=1.0)
parser.add_argument("-b", "--blue", type=float, help="percent blue", default=1.0)
parser.add_argument("-s", "--radius", type=int, help="line thickness radius", default=3)
args = parser.parse_args()

SPECIAL_SAUCE = args.radius
FILENAME = ntpath.splitext(ntpath.basename(args.input))[0]
RED = args.red
GREEN = args.green
BLUE = args.blue

# Load image:
input_image = Image.open(args.input)
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

full_size = (smoothed_input.width - 1) * (smoothed_input.height - 1)

# Compute convolution between intensity and kernels
for x in range(1, smoothed_input.width - 1):
  for y in range(1, smoothed_input.height - 1):
    percent = round(((x * smoothed_input.height - 2) + y) / full_size * 100, 2)
    print("\r{:.2f}% complete".format(percent), end = '')
    magx, magy = 0, 0
    for a in range(3):
        for b in range(3):
            xn = x + a - 1
            yn = y + b - 1
            magx += intensity[xn][yn] * kernelx[a][b] * SPECIAL_SAUCE
            magy += intensity[xn][yn] * kernely[a][b] * SPECIAL_SAUCE

    # Cast to magnitude
    color = int(sqrt(magx**2 + magy**2))
    draw.point((x, y), (int(RED * color), int(GREEN * color), int(BLUE * color), color))

print("")

output_image.save("edges/{}.png".format(FILENAME))

input_image.paste(output_image, (0, 0), output_image)
input_image.save("results/{}.png".format(FILENAME))

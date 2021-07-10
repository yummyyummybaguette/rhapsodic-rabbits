from blessed import Terminal
from PIL import Image

IMAGE_WIDTH = 100
IMAGE_HEIGHT = 50

# Filepaths for images
# Text overlays have the same filepath, with "_overlay" appended
# All images are .png files and are saved in a "Resources" directory
# Images have a pixel size of 100x50
MENU_IMAGE_PATH = 'menu'

def main():
    terminal = Terminal()

    menu_image = Image.open('Resources/' + MENU_IMAGE_PATH + '.png')
    pixels = [[menu_image.getpixel((x, y)) for x in range(IMAGE_WIDTH)] for y in range(IMAGE_HEIGHT)]
    for row in pixels:
        line = ''
        for pixel in row:
            #Double spaces to compensate for rectangular pixels
            line += terminal.on_color_rgb(*pixel) + '  '
        print(line + terminal.normal)

if __name__ == '__main__':
    main()
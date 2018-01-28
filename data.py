from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def generate_data():
    """
    Generate the character descriptions required for the textify script.
    """

    font_size = 50
    font = ImageFont.truetype('consola.ttf', font_size);

    # We need that only to draw sample text and figure out font size.
    # It will be discarded.
    image = Image.new('RGB', (1, 1), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Figure out the width of the font
    # Font is monotype, so each letter has the same width.
    letter_w, letter_h = draw.textsize('a', font)

    # Real image
    image = Image.new('RGB', (letter_w * 30, font_size * 4), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Print all letters
    letter_x = 0
    letter_y = 0
    in_row = 0
    for i in range(33, 127):
        draw.text((letter_x, letter_y), chr(i), (0, 0, 0), font)

        in_row += 1
        if in_row == 30:
            in_row = 0
            letter_x = 0
            letter_y += font_size
        else:
            letter_x += letter_w

    # No reason really, but let's just keep it.
    image.save('output.png', 'PNG')

    """
    Write the densities of all the letters into a file.
    """

    rgb = image.convert('RGB')
    file = open('chars.txt', 'w')

    # We can use space as an "empty" character (0 density)
    file.write('13 0\n')

    letter_x = 0
    letter_y = 0
    in_row = 0

    # Iterate all the letters
    for i in range(33, 127):
        # Calculate density of current letter
        all_pixels = 0
        black_pixels = 0
        for h in range(font_size):
            for w in range(letter_w):
                color = rgb.getpixel((letter_x + w, letter_y + h))
                all_pixels += 1

                # Let's assume anything not completely white is covered
                # in color and is a part of the character.
                if (color != (255, 255, 255)):
                    black_pixels += 1

        # Write information about density to the file
        density = black_pixels / (all_pixels * 1.0)
        file.write('%d %f\n' % (i, density))

        # Move the current position to the next letter
        in_row += 1
        if in_row == 30:
            in_row = 0
            letter_x = 0
            letter_y += font_size
        else:
            letter_x += letter_w

def main():
    generate_data()

if __name__ == '__main__':
    main()

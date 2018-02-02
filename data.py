from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
import sys

class DataGenerator:
    # Characters
    chars = None
    densities = []

    # Fonts
    font = None
    font_size = 50
    letter_width = None
    letter_height = None

    # Image
    image = None
    draw = None

    def __init__(self):
        self.load_allowed_chars()
        self.calc_letter_sizes()
        self.prepare_canvas()
        self.draw_letters()
        self.calc_densities()
        self.save_densities()

    def load_allowed_chars(self):
        """
        File allowed_chars.txt contains all the characters that can be used
        when converting images to ASCII "art".
        """

        file = open('allowed_chars.txt', 'r', encoding='utf8')
        self.chars = file.read()
        file.close()

    def calc_letter_sizes(self):
        """
        While we can explicitly set the font height, we don't know what the width
        of the letter will be.
        This method creates a "fake" image, draws a letter and measures it.
        """

        self.font = ImageFont.truetype('consola.ttf', self.font_size);

        # We need that only to draw sample text and figure out font size.
        # It will be discarded.
        image = Image.new('RGB', (1, 1), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        # Figure out the width of the font
        # Font is monotype, so each letter has the same width.
        self.letter_width, self.letter_height = draw.textsize('a', self.font)

    def prepare_canvas(self):
        """
        Instantiate the object we'll draw characters on.
        """

        self.image = Image.new('RGB', (self.letter_width * len(self.chars), self.font_size), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

    def draw_letters(self):
        """
        Draw all allowed characters on an image to measure their densities.
        """

        # First character is for some reason 65k+, I don't know what that is
        # or what it means.
        for i in range(1, len(self.chars)):
            self.draw.text(((i - 1) * self.letter_width, 0), self.chars[i], (0, 0, 0), self.font)

        # Save on disk
        # Not necessary for anything, but just to visually inspect if it looks ok.
        self.image.save('allowed_chars.png')

    def calc_densities(self):
        """
        Measure densities of all characters.
        Density is just the proportion of all non-white pixels in the area
        occupied by the character.
        """

        canvas = self.image.convert('RGB')

        for i in range(1, len(self.chars)):
            pos = i - 1

            # Iterate over all pixels of a given letter
            all_pixels = 0
            black_pixels = 0
            for h in range(self.letter_height):
                for w in range(self.letter_width):
                    all_pixels += 1

                    color = canvas.getpixel(((pos * self.letter_width) + w, h))
                    if (color != (255, 255, 255)):
                        black_pixels += 1

            self.densities.append((self.chars[i], black_pixels / all_pixels))

    def save_densities(self):
        """
        Save calculated densities in a file the main script will use.
        """

        file = open('densities', 'wb')

        for density in self.densities:
            line = '%s %f\n' % (density[0], density[1])
            file.write(line.encode('utf8'))

        file.close()

def densities_stats():
    """
    Print what generally the distribution of densities looks like.
    """

    file = Path('densities')
    if not file.is_file():
        print('Densities file does not exist.')
        print('Try generating the character data first.')

        return

    file = open('densities', 'r', encoding='utf8')

    densities = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    for line in file:
        # File contains densities in format:
        # [character] [density]
        split = line.split(' ')
        density = split[len(split) - 1]

        # Count how many characters are in each 10th
        density = float(density)
        index = int(density * 10)
        if (index > 9):
            index = 9

        densities[index] += 1

    file.close()

    print(densities)

def main():
    if (len(sys.argv) > 1):
        param = sys.argv[1]

        if (param == 'stats'):
            densities_stats()

        else:
            print('Unknown command')

    else:
        DataGenerator()

if __name__ == '__main__':
    main()

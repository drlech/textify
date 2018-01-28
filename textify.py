from PIL import Image
from pathlib import Path
import sys

class Textifier:
    chars = []
    image = None

    letter_w = 9
    letter_h = 16

    def __init__(self, filename):
        """
        Args:
            filename (string): Name of the input image file.
        """

        # Instance of the input image
        self.image = Image.open(filename)

        # Load character data
        characters_file = open('chars', 'r')
        for line in characters_file:
            split = line.split(' ')

            # First element is a character number, second is density
            split[0] = int(split[0])
            split[1] = float(split[1].rstrip())

            self.chars.append((split[0], split[1]))

        characters_file.close()

        # Sort characters by density
        self.chars.sort(key = lambda char: char[1])

        # Normalize densities to 0-1
        highest_density = self.chars[-1][1];
        ratio = 1 / highest_density

        self.chars = list(map(lambda char: (char[0], char[1] * ratio), self.chars))

        # Run the image processing
        self.process()

    def process(self):
        # Ouput file
        output = open('output.txt', 'w')

        width, height = self.image.size
        rgb = self.image.convert('RGB')

        x = 0
        y = 0
        letters = 0
        while x + self.letter_w < width or y + self.letter_h < height:
            letters += 1
            brightness = 0

            # Iterate over the range of one letter and figure out its density.
            # We define density of color image as just the average
            # of the inverse of brightness.
            for h in range(self.letter_h):
                for w in range(self.letter_w):
                    current_x = x + w
                    current_y = y + h

                    # Check if the current pixel is in the image
                    if current_x < width and current_y < height:
                        color = rgb.getpixel((x + w, y + h))
                        brightness += (1 - self.get_brightness(color))

            # Average brightness
            brightness /= (self.letter_w * self.letter_h)
            output.write('o')

            # Move current position to the next letter
            x += self.letter_w
            if x > width:
                x = 0
                y += self.letter_h

                output.write('\n')

        output.close()

    def get_brightness(self, color):
        """
        Get luminosity of a given RGB color, normalized to 0 - 1.

        Args:
            color (tuple): RGB color.

        Returns:
            int: Color luminosity.
        """

        r, g, b = color
        return (0.299 * r + 0.587 * g + 0.114 * b) / 255;

def main():
    # Check if characters data file exist
    characters_file = Path('chars')
    if not characters_file.is_file():
        print('File with character data does not exist.')
        print('Did you run data generating script?')
        return

    # Check if file was passed as argument
    if len(sys.argv) < 2:
        print('Pass image name as an argument.')
        return

    # Check if image file exists
    filename = sys.argv[1]
    file = Path(filename)
    if not file.is_file():
        print('Image does not exist')
        return

    Textifier(filename)

if __name__ == '__main__':
    main()
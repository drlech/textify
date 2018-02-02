from PIL import Image
from pathlib import Path
import sys

class Textifier:
    chars = [(' ', 0)]
    image = None

    letter_w = 5
    letter_h = 9

    def __init__(self, filename):
        """
        Args:
            filename (string): Name of the input image file.
        """

        # Instance of the input image
        self.image = Image.open(filename)

        # Load character data
        characters_file = open('densities', 'r', encoding='utf8')
        for line in characters_file:
            split = line.split(' ')

            # First element is a character, second is density
            split[1] = float(split[1].rstrip())

            self.chars.append((split[0], split[1]))

        characters_file.close()

        # Sort characters by density
        self.chars.sort(key = lambda char: char[1])

        # Run the image processing
        self.process()

    def process(self):
        # Ouput file
        output = open('output.txt', 'wb')

        width, height = self.image.size
        rgb = self.image.convert('RGB')

        x = 0
        y = 0
        brightness = 0
        while x + self.letter_w < width or y + self.letter_h < height:
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
            output.write(self.find_closest_char(brightness).encode())

            brightness -= 1;

            # Move current position to the next letter
            x += self.letter_w
            if x > width:
                x = 0
                y += self.letter_h

                output.write('\n'.encode())

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

    def find_closest_char(self, density):
        """
        Find the character that has density closest to the given density.

        Args:
            density (float): Density to match.

        Returns:
            int: Character code of the matched character.
        """

        chosen_char = None
        chosen_dens = None
        closest_density = 99999;
        for char in self.chars:
            diff = abs(char[1] - density)

            if diff < closest_density:
                closest_density = diff
                chosen_char = char[0]
                chosen_dens = char[1]

        return chosen_char

def main():
    # Check if characters data file exist
    characters_file = Path('densities')
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

from PIL import Image, ImageFont, ImageDraw

def image():
    font_size = 50
    font = ImageFont.truetype('consola.ttf', font_size, encoding="unic");

    image = Image.new('RGB', (640, 480), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), u'░', (0, 0, 0), font)

    image.save('test.png')

def text():
    file = open('test.txt', 'wb')
    file.write('░'.encode('utf8'))
    file.close()

def main():
    image()

if __name__ == '__main__':
    main()

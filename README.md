# Textify

Attempts to convert raster images into something somewhat similar to ASCII art. Esentially redraws the raster image as a textfile.

## Usage

allowed_chars.txt contains characters allowed to draw the output image.

Run:
```
py data.py
```
to generate data required for the main script to work. Running:
```
py data.py stats
```
will display some info about the generated data.

Run:
```
py textify.py {image}
```
to generate the output.

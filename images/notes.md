Supported Image Types for the image Field:
In the current script, the images are loaded using the Pillow library (PIL). The supported image types depend on the formats that Pillow can handle, which include:

JPEG (.jpg, .jpeg)
PNG (.png)
GIF (.gif) (static images only, not animated GIFs)
BMP (.bmp)
TIFF (.tiff) (if libtiff is available)
When specifying the image path in the image column of the CSV file, ensure that the file path points to one of the supported formats listed above.

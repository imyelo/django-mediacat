from .jpeg import is_jpeg, JPEGFile
from .png import is_png, PNGFile


def extract_xmp_data(image):
    image.seek(0)

    if is_jpeg(image):

        # Read in input file
        try:
            jpeg_file = JPEGFile.read(image)
        except ValueError:
            return ''

        # Loop through segments and search for XMP packet
        for segment in jpeg_file.segments:
            if segment.type == 'APP1':
                if segment.bytes[4:32] == b'http://ns.adobe.com/xap/1.0/':
                    return segment.bytes[32:]

        # No XMP data was found
        return ''

    elif is_png(image):

        # Read in input file
        try:
            png_file = PNGFile.read(image)
        except ValueError:
            return ''

        # Loop through chunks and search for XMP packet
        for chunk in png_file.chunks:
            if chunk.type == 'iTXt':
                if chunk.data.startswith(b'XML:com.adobe.xmp'):
                    return chunk.data[22:]

        # No XMP data was found
        return ''

    else:

        contents = image.read()

        try:
            start = contents.index(b"<?xpacket begin=")
            end = contents.index(b"</x:xmpmeta>") + 12
        except ValueError:
            return ''

        return contents[start:end]

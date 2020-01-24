import struct
import os
import os.path
from io import BytesIO
from typing import BinaryIO, List

from .jbig2 import JBIG2StreamReader, JBIG2StreamWriter
from .layout import LTImage
from .pdfcolor import LITERAL_DEVICE_CMYK
from .pdfcolor import LITERAL_DEVICE_GRAY
from .pdfcolor import LITERAL_DEVICE_RGB
from .pdftypes import LITERALS_DCT_DECODE
from .pdftypes import LITERALS_JBIG2_DECODE


def align32(x):
    return ((x + 3) // 4) * 4


class BMPWriter(object):
    def __init__(self, fp, bits, width, height):
        self.fp = fp
        self.bits = bits
        self.width = width
        self.height = height
        if bits == 1:
            ncols = 2
        elif bits == 8:
            ncols = 256
        elif bits == 24:
            ncols = 0
        else:
            raise ValueError(bits)
        self.linesize = align32((self.width * self.bits + 7) // 8)
        self.datasize = self.linesize * self.height
        headersize = 14 + 40 + ncols * 4
        info = struct.pack('<IiiHHIIIIII', 40, self.width, self.height, 1, self.bits, 0, self.datasize, 0, 0, ncols, 0)
        assert len(info) == 40, str(len(info))
        header = struct.pack('<ccIHHI', b'B', b'M', headersize + self.datasize, 0, 0, headersize)
        assert len(header) == 14, str(len(header))
        self.fp.write(header)
        self.fp.write(info)
        if ncols == 2:
            # B&W color table
            for i in (0, 255):
                self.fp.write(struct.pack('BBBx', i, i, i))
        elif ncols == 256:
            # grayscale color table
            for i in range(256):
                self.fp.write(struct.pack('BBBx', i, i, i))
        self.pos0 = self.fp.tell()
        self.pos1 = self.pos0 + self.datasize

    def write_line(self, y, data):
        self.fp.seek(self.pos1 - (y + 1) * self.linesize)
        self.fp.write(data)


def is_jpeg(image: LTImage) -> bool:
    """Checks if the image is encoded in the JPEG format."""
    filters = image.stream.get_filters()
    return len(filters) == 1 and filters[0][0] in LITERALS_DCT_DECODE


def is_jbig2(image: LTImage) -> bool:
    """Checks if the image is encoded in the JBIG2 format."""
    for name, _ in image.stream.get_filters():
        if name in LITERALS_JBIG2_DECODE:
            return True
    return False


def image_filename(image: LTImage) -> str:
    """Returns a filename for the image, based on its name and encoding."""
    if is_jpeg(image):
        return f'{image.name}.jpg'
    if is_jbig2(image):
        return f'{image.name}.jb2'
    width, height = image.srcsize
    if (image.bits == 1 or image.bits == 8 and
            (LITERAL_DEVICE_RGB in image.colorspace or LITERAL_DEVICE_GRAY in image.colorspace)):
        ext = f'.{width}x{height}.bmp'
    else:
        ext = f'.{image.bits}.{width}x{height}.img'
    return image.name + ext


def dump_image(image: LTImage, fp: BinaryIO):
    """Write the image to a file-like object.

    Args:
        image: An LTImage component from a PDF.
        fp: A binary file-like object, such as the result of `open(.., 'wb')` or a BytesIO.
    """
    width, height = image.srcsize
    if is_jpeg(image):
        raw_data = image.stream.get_rawdata()
        if LITERAL_DEVICE_CMYK in image.colorspace:
            from PIL import Image
            from PIL import ImageChops
            ifp = BytesIO(raw_data)
            i = Image.open(ifp)
            i = ImageChops.invert(i)
            i = i.convert('RGB')
            i.save(fp, 'JPEG')
        else:
            fp.write(raw_data)
    elif is_jbig2(image):
        input_stream = BytesIO()
        input_stream.write(image.stream.get_data())
        input_stream.seek(0)
        reader = JBIG2StreamReader(input_stream)
        writer = JBIG2StreamWriter(fp)
        writer.write_file(reader.get_segments())
    elif image.bits == 1:
        bmp = BMPWriter(fp, 1, width, height)
        data = image.stream.get_data()
        i = 0
        width = (width + 7) // 8
        for y in range(height):
            bmp.write_line(y, data[i:i + width])
            i += width
    elif image.bits == 8 and LITERAL_DEVICE_RGB in image.colorspace:
        bmp = BMPWriter(fp, 24, width, height)
        data = image.stream.get_data()
        i = 0
        width = width * 3
        for y in range(height):
            bmp.write_line(y, data[i:i + width])
            i += width
    elif image.bits == 8 and LITERAL_DEVICE_GRAY in image.colorspace:
        bmp = BMPWriter(fp, 8, width, height)
        data = image.stream.get_data()
        i = 0
        for y in range(height):
            bmp.write_line(y, data[i:i + width])
            i += width
    else:
        fp.write(image.stream.get_data())


class ImageWriter(object):
    """Writes images from a PDF to files in some directory."""

    def __init__(self, outdir: str):
        """Initialize an ImageWriter with an output directory.

        Args:
            outdir: The directory to which image files are written.
        """
        self.outdir = outdir
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)

    def export_image(self, image: LTImage) -> str:
        """Save the image to a file in outdir

        Args:
            image: An LTImage component from a PDF.

        Returns:
            The filename of the new image file (excluding the directory).
        """
        filename = image_filename(image)
        with open(os.path.join(self.outdir, filename), 'wb') as fp:
            dump_image(image, fp)
        return filename


class ImageCollector(object):
    """Collects LTImage's during PDF interpretation.

    This class lets you collect images from a PDF in a converter, such as pdfminer.converter.TextConverter
    but avoid writing them straight to files, as the original ImageWriter does.
    """

    def __init__(self):
        self.images: List[LTImage] = []

    def export_image(self, image: LTImage):
        """Add the image to the collection.

        Args:
            image: An LTImage component from a PDF.
        """
        self.images.append(image)

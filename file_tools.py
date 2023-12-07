import exifread
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import os
import json
directory = os.path.join(os.path.dirname(__file__), 'static')
file_name = 'exif_dict.json'
file_path = os.path.join(directory, file_name)
with open(file_path, 'r') as json_file:
    ExifDict = json.load(json_file)


def get_exif(uploaded_file):
    image = Image.open(uploaded_file)

    uploaded_file.seek(0, os.SEEK_END)
    b = uploaded_file.tell()
    mib = uploaded_file.tell() / 1024 / 1024
    mp = (image.width * image.height) / 1000000

    PillowDict = {
        'Filename': [str(uploaded_file.filename), 'The current name of the uploaded image file.'],
        'File Format': [str(image.format), 'The current file extension of the uploaded image.'],
        'File Size (Bytes)': [str(b), 'The current size of the uploaded image file in bytes.'],
        'File Size (Mebibytes)': [str(mib), 'The current size of the uploaded image file in mebibytes.'],
        'Width': [str(image.width), 'The width of the uploaded image file, in pixels.'],
        'Height': [str(image.height), 'The height of the uploaded image file, in pixels.'],
        'Megapixels': [str(mp), 'Identifies how big the image is in megapixels, which is equal to one million pixels.'],
        'Mode': [str(image.mode), 'Image mode. This is a string specifying the pixel format used by the image.'],
        'Pillow Version': [str(Image.__version__), 'The version of the Pillow module used to gather certain image information.']

    }

    tags = exifread.process_file(uploaded_file, details=False)

    # if image does not contain exif data
    if len(tags) == 0:
        return PillowDict
    # else continue writing report with exif information
    else:
        coords = {}
        exif_table = {}
        if str(image.format) != 'TIFF':
            for k, v in image._getexif().items():
                tag = TAGS.get(k, k)
                exif_table[tag] = v

                if tag == 'GPSInfo':
                    gps_info = {}
                    for geok, geov in exif_table['GPSInfo'].items():
                        geo_tag = GPSTAGS.get(geok, geok)
                        gps_info[geo_tag] = geov

                    # in some instances, .jpg files contain the GPSInfo tag, but not necessarily GPSLatitude or GPSLongitude, which we utilize for map creation. this exits the location information section
                    if 'GPSLatitude' not in gps_info:
                        continue

                    lat = gps_info['GPSLatitude']
                    long = gps_info['GPSLongitude']

                    # degrees minutes seconds -> decimal
                    lat = float(lat[0] + (lat[1]/60) + (lat[2]/(3600)))
                    long = float(long[0] + (long[1]/60) + (long[2]/(3600)))

                    # Negative if LatitudeRef:S or LongitudeRef:W
                    if gps_info['GPSLatitudeRef'] == 'S':
                        lat = -lat
                    if gps_info['GPSLongitudeRef'] == 'W':
                        long = -long

                    coords.update({"Latitude": '{0:.10f}'.format(lat)})
                    coords.update({"Longitude": '{0:.10f}'.format(long)})

        # exifread version
        exifreadVersion = exifread.__version__

        # exif data
        presentTags = {}
        for tag in tags.keys():
            res = tag.split(' ', 1)[1]

            if tag.split(' ', 1)[0] == 'Thumbnail':
                continue

            if res == 'Tag 0xA460':
                res = 'CompositeImage'
            elif res == 'Tag 0x001F':
                res = 'GPSHPositioningError'
            elif res == 'Tag 0x000B':
                res = 'ProcessingSoftware'
            elif res == 'Tag 0xEA1C':
                continue

            presentTags.update({res: tags[tag]})

    return (PillowDict, coords, exifreadVersion, tags, presentTags, ExifDict)

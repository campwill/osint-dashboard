import exifread
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import folium
import os


ExifDict = {
  #interoperability tag information
  'InteroperabilityIndex'      :['INTEROP Tag ID:','0x0001','Indicates the identification of the Interoperability rule.'],
  'InteroperabilityVersion'    :['INTEROP Tag ID:','0x0002','Interoperability version.'],
  'RelatedImageFileFormat'     :['INTEROP Tag ID:','0x1000','File format of image file.'],
  'RelatedImageWidth'          :['INTEROP Tag ID:','0x1001','Image width.'],
  'RelatedImageLength'         :['INTEROP Tag ID:','0x1002','Image height'],
   
  #gps tags information  
  'GPSVersionID'               :['GPS Tag ID:','0x0000','Indicates the version of GPSInfoIFD. The version is given as byte sequence, for example 2, 2, 0, 0 indicates version 2.2. This tag is mandatory when GPS IFD tag is present. Note that the GPSVersionID tag is written differently from the ExifVersion tag.'],
  'GPSLatitudeRef'             :['GPS Tag ID:','0x0001','Indicates whether the latitude is north or south latitude.<br>\'N\' = North<br>\'S\' = South'],
  'GPSLatitude'                :['GPS Tag ID:','0x0002','Indicates the latitude.<br>[dd, mm, ss]'],
  'GPSLongitudeRef'            :['GPS Tag ID:','0x0003','Indicates whether the longitude is east or west longitude.<br>\'E\' = East<br>\'W\' = West'],
  'GPSLongitude'               :['GPS Tag ID:','0x0004','Indicates the longitude.<br>[dd, mm, ss]'],
  'GPSAltitudeRef'             :['GPS Tag ID:','0x0005','Indicates the altitude used as the reference altitude.<br>0 = Above sea level<br>1 = Below sea level'],
  'GPSAltitude'                :['GPS Tag ID:','0x0006','Indicates the altitude based on the reference in GPSAltitudeRef. The reference unit is in meters.'],
  'GPSTimeStamp'               :['GPS Tag ID:','0x0007','Indicates the time as UTC (Coordinated Universal Time).<br>hh:mm:ss'],
  'GPSSatellites'              :['GPS Tag ID:','0x0008','Indicates the GPS satellites used for measurements. This tag can be used to describe the number of satellites, their ID number, angle of elevation, azimuth, SNR and other information in ASCII notation. The format is not specified.'],
  'GPSStatus'                  :['GPS Tag ID:','0x0009','Indicates the status of the GPS receiver when the image is recorded.<br>\'A\' = Measurement is in progress<br>\'V\' = Measurement is Interoperability'],
  'GPSMeasureMode'             :['GPS Tag ID:','0x000A','Indicates the GPS measurement mode.<br>\'2\' = 2-dimensional measurement<br>\'3\' = 3-dimensional measurement'],
  'GPSDOP'                     :['GPS Tag ID:','0x000B','Indicates the GPS DOP (data degree of precision). An HDOP value is written during two-dimensional measurement, and PDOP during three-dimensional measurement.'],
  'GPSSpeedRef'                :['GPS Tag ID:','0x000C','Indicates the unit used to express the GPS receiver speed of movement.<br>\'K\' = Kilometers per hour<br>\'M\' = Miles per hour<br>\'N\' = Knots'],
  'GPSSpeed'                   :['GPS Tag ID:','0x000D','Indicates the speed of GPS receiver movement.'],
  'GPSTrackRef'                :['GPS Tag ID:','0x000E','Indicates the reference for giving the direction of GPS receiver movement.<br>\'T\' = True direction<br>\'M\' = Magnetic direction'],
  'GPSTrack'                   :['GPS Tag ID:','0x000F','Indicates the direction of GPS receiver movement.<br>0.00 to 359.99'],
  'GPSImgDirectionRef'         :['GPS Tag ID:','0x0010','Indicates the reference for giving the direction of the image when it is captured.<br>\'T\' = True direction<br>\'M\' = Magnetic direction'],
  'GPSImgDirection'            :['GPS Tag ID:','0x0011','Indicates the direction of the image when it was captured.<br>0.00 to 359.99'],
  'GPSMapDatum'                :['GPS Tag ID:','0x0012','Indicates the geodetic survey data used by the GPS receiver. If the survey data is restricted to Japan, the value of this tag is \'TOKYO\' or \'WGS-84\'.'],
  'GPSDestLatitudeRef'         :['GPS Tag ID:','0x0013','Indicates whether the latitude of the destination point is north or south latitude.<br>\'N\' = North<br>\'S\' = South'],
  'GPSDestLatitude'            :['GPS Tag ID:','0x0014','Indicates the latitude of the destination point.<br>[dd, mm, ss]'],
  'GPSDestLongitudeRef'        :['GPS Tag ID:','0x0015','Indicates whether the longitude of the destination point is east or west longitude.<br>\'E\' = East<br>\'W\' = West'],
  'GPSDestLongitude'           :['GPS Tag ID:','0x0016','Indicates the longitude of the destination point.<br>[dd, mm, ss]'],
  'GPSDestBearingRef'          :['GPS Tag ID:','0x0017','Indicates the reference used for giving the bearing to the destination point.<br>\'T\' = True direction<br>\'M\' = Magnetic direction'],
  'GPSDestBearing'             :['GPS Tag ID:','0x0018','Indicates the bearing to the destination point.<br>0.00 to 359.99'],
  'GPSDestDistanceRef'         :['GPS Tag ID:','0x0019','Indicates the unit used to express the distance to the destination point.<br>\'K\' = Kilometers<br>\'M\' = Miles<br>\'N\' = Knots'],
  'GPSDestDistance'            :['GPS Tag ID:','0x001A','Indicates the distance to the destination point.'],
  'GPSProcessingMethod'        :['GPS Tag ID:','0x001B','A character string recording the name of the method used for location finding. The first byte indicates the character code used, and this is followed by the name of the method.'],
  'GPSAreaInformation'         :['GPS Tag ID:','0x001C','A character string recording the name of the GPS area. The first byte indicates the character code used, and this is followed by the name of the GPS area.'],
  'GPSDate'                    :['GPS Tag ID:','0x001D','A character string recording date and time information relative to UTC (Coordinated Universal Time).<br>yyyy:mm:dd'],
  'GPSDifferential'            :['GPS Tag ID:','0x001E','Indicates whether differential correction is applied to the GPS receiver.<br>0 = Measurement without differential correction<br>1 = Differential correction applied'],
  'GPSHPositioningError'       :['GPS Tag ID:','0x001F','Indicates the horizontal error in the GPS position (in meters).'],
  #exif tags informat
  'ProcessingSoftware'         :['EXIF Tag ID:','0x000B','The name and version of the software used to post-process the picture.'],
  'SubfileType'                :['EXIF Tag ID:','0x00FE','A general indication of the kind of data contained in this subfile.<br>0x0 = Full-resolution Image<br>0x1 = Reduced-resolution image<br>0x2 = Single page of multi-page image<br>0x3 = Single page of multi-page reduced-resolution image<br>0x4 = Transparency mask<br>0x5 = Transparency mask of reduced-resolution image<br>0x6 = Transparency mask of multi-page image<br>0x7 = Transparency mask of reduced-resolution multi-page image<br>0x10001 = Alternate reduced-resolution image<br>0xffffffff = invalid'],
  'OldSubfileType'             :['EXIF Tag ID:','0x00FF','A general indication of the kind of data contained in this subfile.<br>1 = Full-resolution image<br>2 = Reduced-resolution image<br>3 = Single page of multi-page image'],
  'ImageWidth'                 :['EXIF Tag ID:','0x0100','The number of columns in the image, i.e., the number of pixels per row.'],
  'ImageLength'                :['EXIF Tag ID:','0x0101','The number of rows of pixels in the image.'],
  'BitsPerSample'              :['EXIF Tag ID:','0x0102','Number of bits per component.'],
  'Compression'                :['EXIF Tag ID:','0x0103','Compression scheme used on the image data.<br>1 = Uncompressed<br>2 = CCITT 1D<br>3 = T4/Group 3 Fax<br>4 = T6/Group 4 Fax<br>5 = LZW<br>6 = JPEG (old-style)<br>7 = JPEG<br>8 = Adobe Deflate<br>9 = JBIG B&W<br>10 = JBIG Color<br>32766 = Next<br>32769 = Epson ERF Compressed<br>32771 = CCIRLEW<br>32773 = PackBits<br>32809 = Thunderscan<br>32895 = IT8CTPAD<br>32896 = IT8LW<br>32897 = IT8MP<br>32898 = IT8BL<br>32908 = PixarFilm<br>32909 = PixarLog<br>32946 = Deflate<br>32947 = DCS<br>34661 = JBIG<br>34676 = SGILog<br>34677 = SGILog24<br>34712 = JPEG 2000<br>34713 = Nikon NEF Compressed<br>65000 = Kodak DCR Compressed<br>65535 = Pentax PEF Compressed'],
  'PhotometricInterpretation'  :['EXIF Tag ID:','0x0106','The color space of the image data.'],
  'Thresholding'               :['EXIF Tag ID:','0x0107','For black and white TIFF files that represent shades of gray, the technique used to convert from gray to black and white pixels.'],
  'CellWidth'                  :['EXIF Tag ID:','0x0108','The width of the dithering or halftoning matrix used to create a dithered or halftoned bilevel file.'],
  'CellLength'                 :['EXIF Tag ID:','0x0109','The length of the dithering or halftoning matrix used to create a dithered or halftoned bilevel file.'],
  'FillOrder'                  :['EXIF Tag ID:','0x010A','The logical order of bits within a byte.'],
  'DocumentName'               :['EXIF Tag ID:','0x010D','The name of the document from which this image was scanned.'],
  'ImageDescription'           :['EXIF Tag ID:','0x010E','A string that describes the subject of the image.'],
  'Make'                       :['EXIF Tag ID:','0x010F','The scanner manufacturer.'],
  'Model'                      :['EXIF Tag ID:','0x0110','The scanner model name or number.'],
  'StripOffsets'               :['EXIF Tag ID:','0x0111','For each strip, the byte offset of that strip.'],
  'Orientation'                :['EXIF Tag ID:','0x0112','The orientation of the image with respect to the rows and columns.<br>1 = Horizontal (normal)<br>2 = Mirrored horizontal<br>3 = Rotated 180<br>4 = Mirrored vertical<br>5 = Mirrored horizontal then rotated 90 CCW<br>6 = Rotated 90 CW<br>7 = Mirrored horizontal then rotated 90 CW<br>8 = Rotated 90 CCW'],
  'SamplesPerPixel'            :['EXIF Tag ID:','0x0115','The number of components per pixel.'],
  'RowsPerStrip'               :['EXIF Tag ID:','0x0116','The number of rows per strip.'],
  'StripByteCounts'            :['EXIF Tag ID:','0x0117','For each strip, the number of bytes in the strip after compression.'],
  'MinSampleValue'             :['EXIF Tag ID:','0x0118','The minimum component value used.'],
  'MaxSampleValue'             :['EXIF Tag ID:','0x0119','The maximum component value used.'],
  'XResolution'                :['EXIF Tag ID:','0x011A','The number of pixels per unit given in the ResolutionUnit tag in the ImageWidth direction.'],
  'YResolution'                :['EXIF Tag ID:','0x011B','The number of pixels per unit given in the ResolutionUnit tag in the ImageLength direction.'],
  'PlanarConfiguration'        :['EXIF Tag ID:','0x011C','How the components of each pixel are stored.'],
  'PageName'                   :['EXIF Tag ID:','0x011D','The name of the page from which this image was scanned.'],
  'XPosition'                  :['EXIF Tag ID:','0x011E','X position of the image. The X offset in ResolutionUnits of the left side of the image, with respect to the left side of the page.'],
  'YPosition'                  :['EXIF Tag ID:','0x011F','Y position of the image. The Y offset in ResolutionUnits of the top of the image, with respect to the top of the page. In the TIFF coordinate scheme, the positive Y direction is down, so that YPosition is always positive.'],
  'GrayResponseUnit'           :['EXIF Tag ID:','0x0122','The precision of the information contained in the GrayResponseCurve.<br>1 = 0.1<br>2 = 0.001<br>3 = 0.0001<br>4 = 1e-05<br>5 = 1e-06'],
  'GrayResponseCurve'          :['EXIF Tag ID:','0x0123','For grayscale data, the optical density of each possible pixel value.'],
  'T4Options'                  :['EXIF Tag ID:','0x0124','Options for Group 3 Fax compression.'],
  'T6Options'                  :['EXIF Tag ID:','0x0125','Options for Group 4 Fax compression.'],
  'ResolutionUnit'             :['EXIF Tag ID:','0x0128','The unit of measurement for XResolution and YResolution.<br>1 = Not Absolute<br>2 = Pixels/Inch<br>3 = Pixels/Centimeter'],
  'PageNumber'                 :['EXIF Tag ID:','0x0129','The page number of the page from which this image was scanned.'],
  'ColorResponseUnit'          :['EXIF Tag ID:','0x012C','Length of the color response unit.'],
  'TransferFunction'           :['EXIF Tag ID:','0x012D','Describes a transfer function for the image in tabular style.'],
  'Software'                   :['EXIF Tag ID:','0x0131','Name and version number of the software package(s) used to create the image.'],
  'DateTime'                   :['EXIF Tag ID:','0x0132','Date and time of image creation.<br>yyyy:mm:dd hh:mm:ss'],
  'Artist'                     :['EXIF Tag ID:','0x013B','Person who created the image.'],
  'HostComputer'               :['EXIF Tag ID:','0x013C','The computer and/or operating system in use at the time of image creation.'],
  'Predictor'                  :['EXIF Tag ID:','0x013D','A mathematical operator that is applied to the image data before an encoding scheme is applied.<br>1 = None<br>2 = Horizontal differencing'],
  'WhitePoint'                 :['EXIF Tag ID:','0x013E','The chromaticity of the white point of the image.'],
  'PrimaryChromaticities'      :['EXIF Tag ID:','0x013F','The chromaticities of the primaries of the image.'],
  'ColorMap'                   :['EXIF Tag ID:','0x0140','A color map for palette color images.'],
  'HalftoneHints'              :['EXIF Tag ID:','0x0141','Conveys to the halftone function the range of gray levels within a colorimetrically-specified image that should retain tonal detail.'],
  'TileWidth'                  :['EXIF Tag ID:','0x0142','The tile width in pixels. This is the number of columns in each tile.'],
  'TileLength'                 :['EXIF Tag ID:','0x0143','The tile length (height) in pixels. This is the number of rows in each tile.'],
  'TileOffsets'                :['EXIF Tag ID:','0x0144','For each tile, the byte offset of that tile, as compressed and stored on disk.'],
  'TileByteCounts'             :['EXIF Tag ID:','0x0145','For each tile, the number of (compressed) bytes in that tile.'],
  'BadFaxLines'                :['EXIF Tag ID:','0x0146','Used in the TIFF-F standard, denotes the number of \'bad\' scan lines encountered by the facsimile device.'],
  'CleanFaxData'               :['EXIF Tag ID:','0x0147','Used in the TIFF-F standard, indicates if \'bad\' lines encountered during reception are stored in the data, or if \'bad\' lines have been replaced by the receiver.<br>0 = Clean<br>1 = Registered<br>2 = Unclean'],
  'SubIFDs'                    :['EXIF Tag ID:','0x014A','Offset to child IFDs.'],
  'ConsecutiveBadFaxLines'     :['EXIF Tag ID:','0x0148','Used in the TIFF-F standard, denotes the maximum number of consecutive \'bad\' scanlines received.'],
  'InkSet'                     :['EXIF Tag ID:','0x014C','The set of inks used in a separated (PhotometricInterpretation=5) image.<br>1 = CMYK<br>2 = Not CMYK'],
  'InkNames'                   :['EXIF Tag ID:','0x014D','The name of each ink used in a separated image.'],
  'NumberofInks'               :['EXIF Tag ID:','0x014E','The number of inks. Usually equal to SamplesPerPixel, unless there are extra samples.'],
  'DotRange'                   :['EXIF Tag ID:','0x0150','The component values that correspond to a 0% dot and 100% dot.'],
  'TargetPrinter'              :['EXIF Tag ID:','0x0151','A description of the printing environment for which this separation is intended.'],
  'ExtraSamples'               :['EXIF Tag ID:','0x0152','Description of extra components. Specifies that each pixel has N extra components whose interpretation is defined by one of the values listed below. When this field is used, the SamplesPerPixel field has a value greater than the PhotometricInterpretation field suggests.<br>0 = Unspecified<br>1 = Associated Alpha<br>2 = Unassociated Alpha'],
  'SampleFormat'               :['EXIF Tag ID:','0x0153','Specifies how to interpret each data sample in a pixel.<br>1 = Unsigned<br>2 = Signed<br>3 = Float<br>4 = Undefined<br>5 = Complex int<br>6 = Complex float'],
  'SMinSampleValue'            :['EXIF Tag ID:','0x0154','Specifies the minimum sample value.'],
  'SMaxSampleValue'            :['EXIF Tag ID:','0x0155','Specifies the maximum sample value.'],
  'TransferRange'              :['EXIF Tag ID:','0x0156','Expands the range of the TransferFunction.'],
  'ClipPath'                   :['EXIF Tag ID:','0x0157','Mirrors the essentials of PostScript\'s path creation functionality.'],
  'JPEGTables'                 :['EXIF Tag ID:','0x015B','JPEG quantization and/or Huffman tables.'],
  'JPEGProc'                   :['EXIF Tag ID:','0x0200','Old-style JPEG compression field. TechNote2 invalidates this part of the specification. This field originally indicated the JPEG process used to produce the compressed data.'],
  'JPEGInterchangeFormat'      :['EXIF Tag ID:','0x0201','Old-style JPEG compression field. TechNote2 invalidates this part of the specification. This field was originally intended to indicate whether a JPEG interchange format bitstream is present in the TIFF file.'],
  'JPEGInterchangeFormatLength':['EXIF Tag ID:','0x0202','Old-style JPEG compression field. TechNote2 invalidates this part of the specification. This field was originally intended to indicate the length of the JPEG stream pointed to by JPEGInterchangeFormat tag.'],
  'YCbCrCoefficients'          :['EXIF Tag ID:','0x0211','The transformation from RGB to YCbCr image data.'],
  'YCbCrSubSampling'           :['EXIF Tag ID:','0x0212','Specifies the subsampling factors used for the chrominance components of a YCbCr image.'],
  'YCbCrPositioning'           :['EXIF Tag ID:','0x0213','Specifies the positioning of subsampled chrominance components relative to luminance samples.<br>1 = Centered<br>2 = Co-sited'],
  'ReferenceBlackWhite'        :['EXIF Tag ID:','0x0214','Specifies a pair of headroom and footroom image data values (codes) for each pixel component.'],
  'ApplicationNotes'           :['EXIF Tag ID:','0x02BC','Also known as XMLPacket, stores XMP Metadata.'],
  'Rating'                     :['EXIF Tag ID:','0x4746','Rating tag used by Windows.'],
  'CFARepeatPatternDim'        :['EXIF Tag ID:','0x828D','Contains two values representing the minimum rows and columns to define the repeating patterns of the color filter array.'],
  'CFAPattern'                 :['EXIF Tag ID:','0x828E','Indicates the color filter array (CFA) geometric pattern of the image sensor when a one-chip color area sensor is used.'],
  'BatteryLevel'               :['EXIF Tag ID:','0x828F','Contains a value of the battery level as a fraction or string.'],
  'Copyright'                  :['EXIF Tag ID:','0x8298','Copyright notice.'],
  'ExposureTime'               :['EXIF Tag ID:','0x829A','Exposure time, given in seconds.'],
  'FNumber'                    :['EXIF Tag ID:','0x829D','The F number, or a measure of the light-gathering ability of the lens.'],
  'IPTC/NAA'                   :['EXIF Tag ID:','0x83BB','Contains an IPTC/NAA record.'],
  'ExifOffset'                 :['EXIF Tag ID:','0x8769','Offset, or pointer, to the Exif Sub Image File Directory (IFD).'],
  'InterColorProfile'          :['EXIF Tag ID:','0x8773','Contains an InterColor Consortium (ICC) format color space characterization/profile.'],
  'ExposureProgram'            :['EXIF Tag ID:','0x8822','The class of the program used by the camera to set exposure when the picture is taken.<br>0 = Undefined<br>1 = Manual<br>2 = Program Normal<br>3 = Aperture Priority<br>4 = Shutter Priority<br>5 = Program Creative<br>6 = Program Action<br>7 = Portrait Mode<br>8 = Landscape Mode'],
  'SpectralSensitivity'        :['EXIF Tag ID:','0x8824','Contains an InterColor Consortium (ICC) format color space characterization/profile.'],
  'GPSInfo'                    :['EXIF Tag ID:','0x8825','Offset, or pointer, to the Exif-related GPS Info Image File Directory (IFD).'],
  'ISOSpeedRatings'            :['EXIF Tag ID:','0x8827','ISO Speed refers to a sensor\'s sensitivity to light. The higher the ISO speed, the more light-sensitive it is.'],
  'OECF'                       :['EXIF Tag ID:','0x8828','Indicates the Opto-Electric Conversion Function (OECF) specified in ISO 14524.'],
  'Interlace'                  :['EXIF Tag ID:','0x8829','Indicates the field number of multifield images.'],
  'TimeZoneOffset'             :['EXIF Tag ID:','0x882A','This optional tag encodes the time zone of the camera clock (relative to Greenwich Mean Time) used to create the DataTimeOriginal tag-value when the picture was taken. It may also contain the time zone offset of the clock used to create the DateTime tag-value when the image was modified.'],
  'SelfTimerMode'              :['EXIF Tag ID:','0x882B','Number of seconds image capture was delayed from button press.'],
  'SensitivityType'            :['EXIF Tag ID:','0x8830','The SensitivityType tag indicates which one of the parameters of ISO12232 is the PhotographicSensitivity tag.<br>0 = Unknown<br>1 = Standard Output Sensitivity<br>2 = Recommended Exposure Index<br>3 = ISO Speed<br>4 = Standard Output Sensitivity and Recommended Exposure Index<br>5 = Standard Output Sensitivity and ISO Speed<br>6 = Recommended Exposure Index and ISO Speed<br>7 = Standard Output Sensitivity, Recommended Exposure Index and ISO Speed'],
  'RecommendedExposureIndex'   :['EXIF Tag ID:','0x8832','This tag indicates the recommended exposure index value of a camera or input device defined in ISO 12232.'],
  'ISOSpeed'                   :['EXIF Tag ID:','0x8833','This tag indicates the ISO speed value of a camera or input device that is defined in ISO 12232.'],
  'ExifVersion'                :['EXIF Tag ID:','0x9000','The version of the supported Exif standard.<br>Value is given in equivalent ASCII, which denotes version number (i.e. 0232 denotes version 2.32).'],
  'DateTimeOriginal'           :['EXIF Tag ID:','0x9003','The date and time when the original image data was generated.<br>yyyy:mm:dd hh:mm:ss'],
  'DateTimeDigitized'          :['EXIF Tag ID:','0x9004','The date and time when the image was stored as digital data.<br>yyyy:mm:dd hh:mm:ss'],
  'OffsetTime'                 :['EXIF Tag ID:','0x9010','Time difference from Universal Time Coordinated including daylight saving time of DateTime tag.'],
  'OffsetTimeOriginal'         :['EXIF Tag ID:','0x9011','Time difference from Universal Time Coordinated including daylight saving time of DateTimeOriginal tag.'],
  'OffsetTimeDigitized'        :['EXIF Tag ID:','0x9012','Time difference from Universal Time Coordinated including daylight saving time of DateTimeDigitized tag.'],
  'ComponentsConfiguration'    :['EXIF Tag ID:','0x9101','Specific to compressed data; specifies the channels and complements of the color space of the image. The channels of each component are arranged in order from the 1st component to the 4th. 4,5,6,0 if RGB uncompressed, 1,2,3,0 otherwise.<br>0 = does not exist<br>1 = Y<br>2 = Cb<br>3 = Cr<br>4 = Red<br>5 = Green<br>6 = Blue'],
  'CompressedBitsPerPixel'     :['EXIF Tag ID:','0x9102','Specific to compressed data; states the compressed bits per pixel.'],
  'ShutterSpeedValue'          :['EXIF Tag ID:','0x9201','Shutter speed. The unit is the APEX (Additive System of Photographic Exposure) setting.'],
  'ApertureValue'              :['EXIF Tag ID:','0x9202','The lens aperture. The unit is the APEX (Additive System of Photographic Exposure) setting.'],
  'BrightnessValue'            :['EXIF Tag ID:','0x9203','The value of brightness. The unit is the APEX (Additive System of Photographic Exposure) setting.<br>-99.99 to 99.99'],
  'ExposureBiasValue'          :['EXIF Tag ID:','0x9204','The exposure bias. The unit is the APEX (Additive System of Photographic Exposure) setting.<br>-99.99 to 99.99'],
  'MaxApertureValue'           :['EXIF Tag ID:','0x9205','The smallest F number of the lens. The unit is the APEX (Additive System of Photographic Exposure) setting.'],
  'SubjectDistance'            :['EXIF Tag ID:','0x9206','The distance to the subject, given in meters.'],
  'MeteringMode'               :['EXIF Tag ID:','0x9207','The metering mode, or the way in which a camera determines exposure.<br>0 = Unidentified<br>1 = Average<br>2 = CenterWeightedAverage<br>3 = Spot<br>4 = MultiSpot<br>5 = Pattern<br>6 = Partial<br>255 = other'],
  'LightSource'                :['EXIF Tag ID:','0x9208','The kind of light source.<br>0 = Unknown<br>1 = Daylight<br>2 = Fluorescent<br>3 = Tungsten (incandescent light)<br>4 = Flash<br>9 = Fine weather<br>10 = Cloudy weather<br>11 = Shade<br>12 = Daylight fluorescent (D 5700 - 7100K)<br>13 = Day white fluorescent (N 4600 - 5400K)<br>14 = Cool white fluorescent (W 3900 - 4500K)<br>15 = White fluorescent (WW 3200 - 3700K)<br>17 = Standard light A<br>18 = Standard light B<br>19 = Standard light C<br>20 = D55<br>21 = D65<br>22 = D75<br>23 = D50<br>24 = ISO studio tungsten<br>255 = other light source'],
  'Flash'                      :['EXIF Tag ID:','0x9209','Indicates the status of flash when the image was shot. Bit 0 indicates the flash firing status, bits 1 and 2 indicate the flash return status, bits 3 and 4 indicate the flash mode, bit 5 indicates whether the flash function is present, and bit 6 indicates "red eye" mode.<br>0 = Flash did not fire<br>1 = Flash fired<br>5 = Strobe return light not detected<br>7 = Strobe return light detected<br>9 = Flash fired, compulsory flash mode<br>13 = Flash fired, compulsory flash mode, return light not detected<br>15 = Flash fired, compulsory flash mode, return light detected<br>16 = Flash did not fire, compulsory flash mode<br>24 = Flash did not fire, auto mode<br>25 = Flash fired, auto mode<br>29 = Flash fired, auto mode, return light not detected<br>31 = Flash fired, auto mode, return light detected<br>32 = No flash function<br>65 = Flash fired, red-eye reduction mode<br>69 = Flash fired, red-eye reduction mode, return light not detected<br>71 = Flash fired, red-eye reduction mode, return light detected<br>73 = Flash fired, compulsory flash mode, red-eye reduction mode<br>77 = Flash fired, compulsory flash mode, red-eye reduction mode, return light not detected<br>79 = Flash fired, compulsory flash mode, red-eye reduction mode, return light detected<br>89 = Flash fired, auto mode, red-eye reduction mode<br>93 = Flash fired, auto mode, return light not detected, red-eye reduction mode<br>95 = Flash fired, auto mode, return light detected, red-eye reduction mode'],
  'FocalLength'                :['EXIF Tag ID:','0x920A','The actual focal length of the lens, in mm.'],
  'FlashEnergy'                :['EXIF Tag ID:','0x920B','Indicates the strobe energy at the time the image is captured, as measured in Beam Candle Power Seconds.'],
  'SpatialFrequencyResponse'   :['EXIF Tag ID:','0x920C','Records the camera or input device spatial frequency table and SFR values in the direction of image width, image height, and diagonal direction, as specified in ISO 12233.'],
  'Noise'                      :['EXIF Tag ID:','0x920D','Noise measurement values.'],
  'ImageNumber'                :['EXIF Tag ID:','0x9211','Number assigned to an image, e.g., in a chained image burst.'],
  'SecurityClassification'     :['EXIF Tag ID:','0x9212','Security classification assigned to the image.'],
  'ImageHistory'               :['EXIF Tag ID:','0x9213','Record of what has been done to the image.'],
  'SubjectArea'                :['EXIF Tag ID:','0x9214','Indicates the location and area of the main subject in the overall scene. The subject location and area are defined by Count values. Coordinate values, width, and height are expressed in relation to the upper left as origin, prior to rotation processing as per the Rotation tag.<br>2 Values: Indicates the location of the main subject as coordinates. The first value is the X coordinate and the second is the Y coordinate.<br>3 Values: The area of the main subject is given as a circle. The circular area is expressed as center coordinates and diameter. The first value is the center X coordinate, the second is the center Y coordinate, and the third is the diameter.<br>4 Values: The area of the main subject is given as a rectangle. The rectangular area is expressed as center coordinates and area dimensions. The first value is the center X coordinate, the second is the center Y coordinate, the third is the width of the area, and the fourth is the height of the area.'],
  'ExposureIndex'              :['EXIF Tag ID:','0x9215','Indicates the exposure index selected on the camera or input device at the time the image is captured.'],
  'TIFF/EPStandardID'          :['EXIF Tag ID:','0x9216','Contains four ASCII characters representing the TIFF/EP standard version of a TIFF/EP file.'],
  'MakerNote'                  :['EXIF Tag ID:','0x927C','Manufacturer specific information.'],
  'UserComment'                :['EXIF Tag ID:','0x9286','Keywords or comments on the image; complements ImageDescription.'],
  'SubSecTime'                 :['EXIF Tag ID:','0x9290','A tag used to record fractions of seconds for the DateTime tag.'],
  'SubSecTimeOriginal'         :['EXIF Tag ID:','0x9291','Indicates the fractional seconds for the DateTimeOriginal tag.'],
  'SubSecTimeDigitized'        :['EXIF Tag ID:','0x9292','Indicates the fractional seconds for the DateTimeDigitized tag.'],
  'XPTitle'                    :['EXIF Tag ID:','0x9C9B','Title tag used by Windows, encoded in UCS2'],
  'XPComment'                  :['EXIF Tag ID:','0x9C9C','Comment tag used by Windows, encoded in UCS2'],
  'XPAuthor'                   :['EXIF Tag ID:','0x9C9D','Author tag used by Windows, encoded in UCS2'],
  'XPKeywords'                 :['EXIF Tag ID:','0x9C9E','Keywords tag used by Windows, encoded in UCS2'],
  'XPSubject'                  :['EXIF Tag ID:','0x9C9F','Subject tag used by Windows, encoded in UCS2'],
  'FlashPixVersion'            :['EXIF Tag ID:','0xA000','The Flashpix format version supported by a FPXR file.<br>Value is given in equivallent ASCII, which denotes version number (i.e. 0100 denotes version 1.0).'],
  'ColorSpace'                 :['EXIF Tag ID:','0xA001','The color space information tag is always recorded as the color space specifier. Normally sRGB is used to define the color space based on the PC monitor conditions and environment. If a color space other than sRGB is used, Uncalibrated is set. Image data recorded as Uncalibrated can be treated as sRGB when it is converted to Flashpix.<br>1 = sRGB<br>2 = Adobe RGB<br>65535 = Uncalibrated'],
  'ExifImageWidth'             :['EXIF Tag ID:','0xA002','Specific to compressed data; the valid width of the meaningful image (in pixels).'],
  'ExifImageLength'            :['EXIF Tag ID:','0xA003','Specific to compressed data; the valid height of the meaningful image (in pixels).'],
  'RelatedSoundFile'           :['EXIF Tag ID:','0xA004','Used to record the name of an audio file related to the image data.'],
  'InteroperabilityOffset'     :['EXIF Tag ID:','0xA005','Offset, or pointer, to the Exif-related Interoperability Image File Directory (IFD).'],
  'FlashEnergy'                :['EXIF Tag ID:','0xA20B','Indicates the strobe energy at the time the image is captured, as measured in Beam Candle Power Seconds'],
  'SpatialFrequencyResponse'   :['EXIF Tag ID:','0xA20C','Records the camera or input device spatial frequency table and SFR values in the direction of image width, image height, and diagonal direction, as specified in ISO 12233.'],
  'FocalPlaneXResolution'      :['EXIF Tag ID:','0xA20E','Indicates the number of pixels in the image width (X) direction per FocalPlaneResolutionUnit on the camera focal plane.'],
  'FocalPlaneYResolution'      :['EXIF Tag ID:','0xA20F','Indicates the number of pixels in the image height (Y) direction per FocalPlaneResolutionUnit on the camera focal plane.'],
  'FocalPlaneResolutionUnit'   :['EXIF Tag ID:','0xA210','Indicates the unit for measuring FocalPlaneXResolution and FocalPlaneYResolution.'],
  'SubjectLocation'            :['EXIF Tag ID:','0xA214','Indicates the location of the main subject in the scene.'],
  'ExposureIndex'              :['EXIF Tag ID:','0xA215','Indicates the exposure index selected on the camera or input device at the time the image is captured.'],
  'SensingMethod'              :['EXIF Tag ID:','0xA217','Indicates the image sensor type on the camera or input device.<br>1 = Not defined<br>2 = One-chip color area<br>3 = Two-chip color area<br>4 = Three-chip color area<br>5 = Color sequential area<br>7 = Trilinear<br>8 = Color sequential linear'],
  'FileSource'                 :['EXIF Tag ID:','0xA300','Indicates the image source.<br>1 = Film Scanner<br>2 = Reflection Print Scanner<br>3 = Digital Camera'],
  'SceneType'                  :['EXIF Tag ID:','0xA301','Indicates the type of scene. If a DSC recorded the image, this tag value shall always be set to 1, indicating that the image was directly photographed.<br>1 = Directly Photographed'],
  'CVAPattern'                 :['EXIF Tag ID:','0xA302','Indicates the color filter array (CFA) geometric pattern of the image sensor when a one-chip color area sensor is used.'],
  'CustomRendered'             :['EXIF Tag ID:','0xA401','Indicates the use of special processing on image data, such as rendering geared to output.<br>0 = Normal<br>1 = Custom'],
  'ExposureMode'               :['EXIF Tag ID:','0xA402','Indicates the exposure mode set when the image was shot. In auto-bracketing mode, the camera shoots a series of frames of the same scene at different exposure settings.<br>0 = Auto Exposure<br>1 = Manual Exposure<br>2 = Auto Bracket'],  
  'WhiteBalance'               :['EXIF Tag ID:','0xA403','Indicates the white balance mode set when the image was shot.<br>0 = Auto<br>1 = Manual'],
  'DigitalZoomRatio'           :['EXIF Tag ID:','0xA404','Indicates the digital zoom ratio when the image was shot. If the numerator of the recorded value is 0, this indicates that digital zoom was not used.'],
  'FocalLengthIn35mmFilm'      :['EXIF Tag ID:','0xA405','Indicates the equivalent focal length assuming a 35mm film camera, in mm. A value of 0 means the focal length is unknown. Note that this tag differs from the FocalLength tag.'],
  'SceneCaptureType'           :['EXIF Tag ID:','0xA406','Indicates the type of scene that was shot. It can also be used to record the mode in which the image was shot. Note that this differs from the SceneType tag.<br>0 = Standard<br>1 = Landscape<br>2 = Portrait<br>3 = Night'],
  'GainControl'                :['EXIF Tag ID:','0xA407','Indicates the degree of overall image gain adjustment.<br>0 = None<br>1 = Low gain up<br>2 = High gain up<br>3 = Low gain down<br>4 = High gain down'],
  'Contrast'                   :['EXIF Tag ID:','0xA408','Indicates the direction of contrast processing applied by the camera when the image was shot.<br>0 = Normal<br>1 = Soft<br>2 = Hard'],
  'Saturation'                 :['EXIF Tag ID:','0xA409','Indicates the direction of saturation processing applied by the camera when the image was shot.<br>0 = Normal<br>1 = Soft<br>2 = Hard'],
  'Sharpness'                  :['EXIF Tag ID:','0xA40A','Indicates the direction of sharpness processing applied by the camera when the image was shot.<br>0 = Normal<br>1 = Soft<br>2 = Hard'],
  'DeviceSettingDescription'   :['EXIF Tag ID:','0xA40B','This tag indicates information on the picture-taking conditions of a particular camera model.'],
  'SubjectDistanceRange'       :['EXIF Tag ID:','0xA40C','Indicates the distance to the subject.'],
  'ImageUniqueID'              :['EXIF Tag ID:','0xA420','Indicates an identifier assigned uniquely to each image.'],
  'CameraOwnerName'            :['EXIF Tag ID:','0xA430','This tag records the owner of a camera used in photography as an ASCII string.'],
  'BodySerialNumber'           :['EXIF Tag ID:','0xA431','This tag records the serial number of the body of the camera that was used in photography as an ASCII string.'],
  'LensSpecification'          :['EXIF Tag ID:','0xA432','Contains information about the lens that captured the image. If the minimum f-stops are unknown, they should be encoded as 0/0.<br>Value 0: Minimum focal length in mm.<br>Value 1: Maximum focal length in mm.<br>Value 2: Minimum (maximum aperture) f-stop at minimum focal length.<br>Value 3: Minimum (maximum aperture) f-stop at maximum focal length.'],
  'LensMake'                   :['EXIF Tag ID:','0xA433','Records the lens manufactor.'],
  'LensModel'                  :['EXIF Tag ID:','0xA434','Records the lens\'s model name and identification information.'],
  'LensSerialNumber'           :['EXIF Tag ID:','0xA435','This tag records the serial number of the interchangeable lens that was used in photography as an ASCII string.'],
  'CompositeImage'             :['EXIF Tag ID:','0xA460','Indicates whether the recorded image is a composite image or not (whether the image is a combination of multiple images or a singular image.<br>0 = Unknown<br>1 = Not a Composite Image<br>2 = General Composite Image<br>3 = Composite Image Captured While Shooting'],
  'Gamma'                      :['EXIF Tag ID:','0xA500','Indicates the value of coefficient gamma.'],
  'PrintIM'                    :['EXIF Tag ID:','0xC4A5','Indicates the value of Print Image Matching,'],
  'BlackLevel'                 :['EXIF Tag ID:','0xC61A','Used in Raw IFD of DNG files. This tag specifies the zero light (a.k.a. thermal black or black current) encoding level, as a repeating pattern.'],
  'Padding'                    :['EXIF Tag ID:','0xEA1C','The amount of padding within an XMP embedded digital file. Appropriate padding is SPACE characters placed anywhere white space is allowed by the general XML syntax and XMP serialization rules, with a linefeed (U+000A) every 100 characters or so to improve human display. The amount of padding is workflow-dependent; around 2000 bytes is often a reasonable amount.'],
  'OffsetSchema'               :['EXIF Tag ID:','0xEA1D','Microsoft\'s ill-conceived maker note offset difference.'],
  'OwnerName'                  :['EXIF Tag ID:','0xFDE8','Generated by Photoshop Camera RAW.'],
  'SerialNumber'               :['EXIF Tag ID:','0xFDE9','Generated by Photoshop Camera RAW.']
  }


def get_exif(uploaded_file):
    image = Image.open(uploaded_file)

    uploaded_file.seek(0, os.SEEK_END)
    b = uploaded_file.tell()
    mib = uploaded_file.tell() / 1024 / 1024
    mp = (image.width * image.height) / 1000000

    PillowDict = {
      'Pillow Version'        :[str(Image.__version__),'The version of the Pillow module used to gather certain image information.'],
      'Filename'              :[str(uploaded_file.filename),'The current name of the uploaded image file.'],
      'File Format'           :[str(image.format),'The current file extension of the uploaded image.'],
      'File Size (Bytes)'     :[str(b),'The current size of the uploaded image file in bytes.'],
      'File Size (Mebibytes)' :[str(mib),'The current size of the uploaded image file in mebibytes.'],
      'Width'                 :[str(image.width),'The width of the uploaded image file, in pixels.'],
      'Height'                :[str(image.height),'The height of the uploaded image file, in pixels.'],
      'Megapixels'            :[str(mp),'Identifies how big the image is in megapixels, which is equal to one million pixels.'],
      'Mode'                  :[str(image.mode),'Image mode. This is a string specifying the pixel format used by the image.']
    }

    tags = exifread.process_file(uploaded_file, details=False)

    #if image does not contain exif data
    if len(tags) == 0:
      return PillowDict
    #else continue writing report with exif information
    else:
      coords={}
      exif_table={}
      if str(image.format) != 'TIFF':
        for k, v in image._getexif().items():
            tag = TAGS.get(k, k)
            exif_table[tag] = v

            if tag == 'GPSInfo':
                gps_info={}
                for geok, geov in exif_table['GPSInfo'].items():
                    geo_tag=GPSTAGS.get(geok, geok)
                    gps_info[geo_tag]=geov

                #in some instances, .jpg files contain the GPSInfo tag, but not necessarily GPSLatitude or GPSLongitude, which we utilize for map creation. this exits the location information section
                if 'GPSLatitude' not in gps_info:
                    continue

                lat=gps_info['GPSLatitude']
                long=gps_info['GPSLongitude']

                #degrees minutes seconds -> decimal
                lat = float(lat[0] + (lat[1]/60) + (lat[2]/(3600)))
                long = float(long[0] + (long[1]/60) + (long[2]/(3600)))

                #Negative if LatitudeRef:S or LongitudeRef:W
                if gps_info['GPSLatitudeRef'] == 'S':
                    lat=-lat
                if gps_info['GPSLongitudeRef'] == 'W':
                    long=-long

                coords.update({"Latitude":'{0:.10f}'.format(lat)})
                coords.update({"Longitude":'{0:.10f}'.format(long)})

                #create map
                m=folium.Map(location=[lat,long],zoom_start=10)
                folium.Marker(location=[lat,long],fill=True, popup=('{0:.10f}'.format(lat) + ",\n" + '{0:.10f}'.format(long)), color='red',fill_color='red').add_to(m)
                m.save('templates/map.html')

                #open map
                foliummap = open('templates/map.html')

      #exifread version
      exifreadVersion = exifread.__version__

      #exif data
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
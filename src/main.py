import fitz
from pprint import pprint

doc = fitz.open("your.pdf")
page = doc[0]  # first page - use 0-based page numbers
pprint(page.get_images())
# [(1114, 0, 1200, 1200, 8, 'DeviceRGB', '', 'Im1', 'FlateDecode')]
# extract the image stored under xref 1114:
# img = doc.extract_image(1114)

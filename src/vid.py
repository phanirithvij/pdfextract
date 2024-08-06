import sys
from pathlib import Path
import fitz
from icecream import ic
import os

out = "out"
os.makedirs(out, exist_ok=True)

doc = fitz.open("your.pdf")
x = 0
for p in range(20):
    page = doc[p]
    annots = list([page.load_annot(x[0]) for x in page.annot_xrefs(page)])
    has_annots = len(annots) > 0
    if not has_annots:
        continue
    print(f"page {p-1} annots")
    for annot in annots:
        print(type(annot))
        if annot.type[0] != fitz.PDF_ANNOT_RICH_MEDIA:
            print(f"Annotation type is {annot.type[1]}")
            print("Only support RichMedia currently")
            sys.exit()

        cont = doc.xref_get_key(annot.xref, "RichMediaContent/Assets/Names")
        if cont[0] != "array":  # should be PDF array
            sys.exit("unexpected: RichMediaContent/Assets/Names is no array")
        array = cont[1][1:-1]  # remove array delimiters
        ic(array)
        array = array.split(" 0 R")[:-1]

        for arr in array:
            x += 1
            print(x)
            # jump over the name / title: we will get it later
            if arr[0] == "(":
                i = arr.find(")")
            else:
                i = arr.find(">")
            xref = int(arr[i + 1 :])  # here is the xref of the actual video stream
            ic(xref)

            video_filename = doc.xref_get_key(xref, "F")[1]
            video_xref = doc.xref_get_key(xref, "EF/F")[1]
            video_xref = int(video_xref.split()[0])
            video_stream = doc.xref_stream_raw(video_xref)
            (Path(out) / f"{p+1}-{video_filename}").write_bytes(video_stream)

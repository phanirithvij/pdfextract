import sys
from pathlib import Path
import fitz
from icecream import ic
import magic
import zlib


def icl(*a):
    ic(*a)


out = Path("out")
out.mkdir(parents=True, exist_ok=True)

doc = fitz.open(sys.argv[1])
x = 0
for p in range(20):
    page = doc[p]
    annots = list([page.load_annot(c[0]) for c in page.annot_xrefs()])
    has_annots = len(annots) > 0
    if not has_annots:
        continue
    icl(f"page {p-1} annots, {len(annots)}")
    for annot in annots:
        # ic(annot.type)
        if annot.type[0] != fitz.PDF_ANNOT_RICH_MEDIA:
            print(f"Annotation type is {annot.type[1]}")
            print("Only support RichMedia currently")
            sys.exit()

        # ic(annot.xref)
        cont = doc.xref_get_key(annot.xref, "RichMediaContent/Assets/Names")
        if cont[0] != "array":  # should be PDF array
            sys.exit("unexpected: RichMediaContent/Assets/Names is no array")
        array = cont[1][1:-1]  # remove array delimiters
        # ic(array)
        array = array.split(" 0 R")[:-1]

        for arr in array:
            x += 1
            # ic(x)
            # jump over the name / title: we will get it later
            if arr[0] == "(":
                i = arr.find(")")
            else:
                i = arr.find(">")
            xref = int(arr[i + 1 :])  # here is the xref of the actual video stream
            # ic(xref)

            video_filename = doc.xref_get_key(xref, "F")[1]
            video_xref = doc.xref_get_key(xref, "EF/F")[1]
            video_xref = int(video_xref.split()[0])
            video_stream = doc.xref_stream_raw(video_xref)

            out_file = out / f"{p+1}-{video_filename}"
            out_stream = video_stream

            fmagic = magic.from_buffer(video_stream[:2048])
            if fmagic == "zlib compressed data":
                icl(f"uncompressing {video_filename}")
                out_stream = zlib.decompress(video_stream)
            elif "Macromedia Flash data" in fmagic:
                icl(f"skipping {video_filename}")
                continue
            icl(f"saving {video_filename}")
            # out_file.write_bytes(out_stream)
    print("\n")

import sys
import fitz


def main():
    doc = fitz.open(sys.argv[1])
    for p in range(20):
        page = doc[p]
        for im in page.get_images():
            img = doc.extract_image(im[0])
            print(dir(img))
            return


if __name__ == "__main__":
    main()

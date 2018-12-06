from argparse import ArgumentParser
from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
import re
import qrcode


def qrcode_to_pdf(data, directory):
    """
    Generate QR code and save it to a PDF file.\n
    data: the string to generate QR.
    directory: the working directory to save the file.
    """
    try:
        os.makedirs(directory)
    except FileExistsError:
        pass
    # generate QR code
    qr = qrcode.QRCode(box_size=6)
    qr.add_data(data)
    qr.make(fit=True)
    img_path = f'{directory}temp.png'
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(img_path)
    # make a pdf and insert the QR image
    pdf, imgTemp = PdfFileWriter(), BytesIO()
    imgDoc = canvas.Canvas(imgTemp, pagesize=A4)
    imgDoc.drawImage(img_path.format(1), 30, 590)
    imgDoc.drawString(30, 580, data)
    imgDoc.save()
    pattern = re.compile('[^a-zA-Z0-9]|_')
    fn = re.sub(pattern, '%', data)
    pdf.addPage(PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0))
    pdf.write(open(f'{directory}qr_code_{fn}.pdf', "wb"))
    os.remove(img_path)  # delete the temporary image


parser = ArgumentParser()
parser.add_argument("-i", help="string to convert into qr code")
parser.add_argument("-o", help="output directory")
args = parser.parse_args()
data, directory = args.i, args.o
qrcode_to_pdf(data, directory)
print('Success!')

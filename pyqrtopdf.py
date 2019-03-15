from argparse import ArgumentParser
from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
import PIL
import re
import qrcode


class PyQRtoPDF:

    def __init__(self, data, directory):
        """
        This class will transform file path string to PDF with QR image.
        :param string (str): data to be converted to qr code
        :param directory (str): save PDF file here
        """
        self.data = data
        self.directory = directory
        self.basename = self.safe_filename(self.data)
        os.makedirs(directory) if not os.path.exists(directory) else ...

    @staticmethod
    def safe_filename(string):
        """
        Convert string to safe filename.
        :param string (str): data
        :returns (str): safe filename
        """
        pattern = re.compile('[^a-zA-Z0-9]|_')
        filename = re.sub(pattern, '_', string)
        return filename

    @staticmethod
    def resize_qr_image(path, basewidth):
        """
        Resize and overwrite QR image.
        :param path (str): full path of png image
        :param basewidth (int): ratio 1:1 as width:height
        :returns (null): no returning value
        """
        Image = PIL.Image
        qr_image = Image.open(path)
        width_percent = (basewidth / float(qr_image.size[0]))
        height_size = int((float(qr_image.size[1]) * float(width_percent)))
        qr_image = qr_image.resize((basewidth, height_size), Image.ANTIALIAS)
        qr_image.save(path)

    def to_qr_image(self):
        """
        Transform data to QR image and save the image as PNG in directory.
        :returns (null): no returning value
        """
        qr_image_basename = f'{self.basename}.png'
        self.qr_image_path = os.path.join(self.directory, qr_image_basename)
        qr = qrcode.QRCode()
        qr.add_data(self.data)
        qr_image = qr.make_image()
        qr_image.save(self.qr_image_path)
        self.resize_qr_image(self.qr_image_path, 200)

    def qr_image_to_pdf(self):
        """
        Convert QR image to PDF file and save.
        :returns (null): no returning value
        """
        bytes_image = BytesIO()
        doc_image = canvas.Canvas(bytes_image, pagesize=A4)
        doc_image.drawImage(self.qr_image_path.format(1), 30, 590)
        doc_image.drawString(45, 580, data)
        doc_image.save()
        qr_pdf_basename = f'{self.basename}.pdf'
        qr_pdf_path = os.path.join(self.directory, qr_pdf_basename)
        with open(qr_pdf_path, 'wb') as file:
            pdf_fw = PdfFileWriter()
            pdf_rd = PdfFileReader(BytesIO(bytes_image.getvalue()))
            pdf_fw.addPage(pdf_rd.getPage(0))
            pdf_fw.write(file)
            # delete QR PNG image
            os.remove(self.qr_image_path)

    def execute(self):
        """
        Execution of the algorithm.
        :returns (null): no returning value
        """
        self.to_qr_image()
        self.qr_image_to_pdf()


parser = ArgumentParser()
parser.add_argument("-data", help="(str) input data")
parser.add_argument("-out", help="(str) PDF save directory")
args = parser.parse_args()
data, directory = args.data, args.out
pyqrtopdf = PyQRtoPDF(data, directory)
pyqrtopdf.execute()
print('Success!')

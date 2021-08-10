import base64
import logging.config
from datetime import datetime

import pdfkit
import win32api
import win32print
from bs4 import BeautifulSoup

from PathResolver import resource_path

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG,
                    filename='logs.log')
logger = logging.getLogger(__name__)
filename = resource_path('render/print.pdf')


def get_image_file_as_base64_data(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read())


def generate_pdf(payment):
    try:
        html = open(resource_path("html/print.html")).read()
        date_time = datetime.now()
        soup = BeautifulSoup(html, "html.parser")
        logo = resource_path('html/img/data-logo.png')
        css = resource_path('html/css/print.css')
        for img in soup.find_all('img'):
            img['src'] = f"data:image/png;base64, {get_image_file_as_base64_data(logo).decode('utf-8')}"

        for td in soup.find_all('td', {'class': 'student'}):
            td.string = payment.studentFullName

        for td in soup.find_all('td', {'class': 'number'}):
            td.string = str(payment.id)

        for td in soup.find_all('td', {'class': 'price'}):
            td.string = payment.price

        for td in soup.find_all('td', {'class': 'type'}):
            td.string = payment.type

        for td in soup.find_all('td', {'class': 'debt'}):
            td.string = str(payment.debt)

        for td in soup.find_all('td', {'class': 'date'}):
            td.string = date_time.strftime("%d-%m-%Y")

        for td in soup.find_all('td', {'class': 'group'}):
            td.string = payment.groupName

        for td in soup.find_all('td', {'class': 'month'}):
            td.string = str(payment.month)

        options = {
            'enable-local-file-access': None,
            'page-height': '115mm',
            'page-width': '80mm',
            'disable-smart-shrinking': '',
            'dpi': 400,
            'margin-top': '0',
            'margin-right': '0',
            'margin-bottom': '0',
            'margin-left': '0',
            'user-style-sheet': css
        }
        pdfkit.from_string(str(soup), filename, options=options)
    except Exception as ex:
        print(f'Error occurred while generate pdf. Error: {ex}')
        logger.error(f'Error occurred while generate pdf. Error: {ex}')


def print_action():
    printer = win32print.GetDefaultPrinter()
    PRINTER_DEFAULTS = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
    pHandle = win32print.OpenPrinter(printer, PRINTER_DEFAULTS)
    level = 2
    properties = win32print.GetPrinter(pHandle, level)
    p_dev_mode = properties["pDevMode"]
    p_dev_mode.PaperSize = 0
    p_dev_mode.PaperLength = 110  # SIZE IN 1/10 mm
    p_dev_mode.PaperWidth = 80  # SIZE IN 1/10 mm
    properties["pDevMode"] = p_dev_mode
    win32print.SetPrinter(pHandle, level, properties, 0)
    logger.debug(f'Default printer selected: {printer}')
    logger.debug(f'File path: {filename}')
    print(f'Default printer selected: {printer}')
    print(f'File path: {filename}')
    try:
        win32api.ShellExecute(0, "print", filename, '"%s"' % printer, ".", 0)
        win32print.ClosePrinter(pHandle)
    except Exception as ex:
        print(f'Error occurred while print cheque. Error: {ex}')
        logger.error(f'Error occurred while print cheque. Error: {ex}')
        return f"Printer bilan bog'liq muammo yuzaga keldi, Error: {ex}"

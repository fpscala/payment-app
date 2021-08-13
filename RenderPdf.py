import base64
import logging.config
from datetime import datetime

import pdfkit
from bs4 import BeautifulSoup

from PathResolver import resource_path

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG,
                    filename='logs.log')
logger = logging.getLogger(__name__)
filename = resource_path('render\print.pdf')


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

        for span in soup.find_all('span', {'class': 'number'}):
            span.string = str(payment.id)

        for td in soup.find_all('td', {'class': 'price'}):
            td.string = payment.price

        for td in soup.find_all('td', {'class': 'type'}):
            td.string = payment.type

        for td in soup.find_all('td', {'class': 'debt'}):
            td.string = str(payment.debt)

        for td in soup.find_all('td', {'class': 'date'}):
            td.string = date_time.strftime("%d.%m.%Y %H:%M:%S")

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
        path_wkthmltopdf = b'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        pdfkit.from_string(str(soup), filename, options=options, configuration=config)
    except Exception as ex:
        print(f'Error occurred while generate pdf. Error: {ex}')
        logger.error(f'Error occurred while generate pdf. Error: {ex}')

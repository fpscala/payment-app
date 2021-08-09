from datetime import datetime

from bs4 import BeautifulSoup
import pdfkit
import base64


def get_image_file_as_base64_data(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read())


def generate_pdf(payment):
    try:
        html = open("html/print.html").read()
        date_time = datetime.now()
        soup = BeautifulSoup(html, "html.parser")
        for img in soup.find_all('img'):
            img['src'] = f"data:image/png;base64, {get_image_file_as_base64_data('html/img/data-logo.png').decode('utf-8')}"

        for td in soup.find_all('td', {'class': 'student'}):
            td.string = payment.studentFullName

        for td in soup.find_all('td', {'class': 'price'}):
            td.string = payment.price

        for td in soup.find_all('td', {'class': 'type'}):
            td.string = payment.type

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
            'user-style-sheet': 'html/css/print.css'
        }
        pdfkit.from_string(str(soup), 'render/print.pdf', options=options)
    except Exception as ex:
        print(ex)

import json
import logging
import logging.config
from collections import namedtuple

from PathResolver import resource_path
from RenderPdf import generate_pdf, print_action
from connections import Connection


def custom_payment_decoder(payment_dict):
    return namedtuple('Payment', payment_dict.keys())(*payment_dict.values())


class JavascriptApi:
    def __init__(self):
        self.connection = Connection()
        self.main_screen = None

    def set_main_screen(self, window):
        self.main_screen = window

    def quit_login(self):
        self.main_screen.set_title("To'lov")
        self.main_screen.load_url('html/index.html')
        self.main_screen.resize(1200, 755)

    def logger(self, text):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG,
                            filename='logs.log')
        logger = logging.getLogger(__name__)
        logger.debug(text)

    def get_directions(self):
        return self.connection.getDirections()

    def get_groups(self):
        return self.connection.getGroups()

    def get_last_payment_id(self):
        return self.connection.getLastPaymentId()

    def get_teachers(self):
        return self.connection.getTeachers()

    def get_students(self, group_id):
        return self.connection.getStudentByGroupId(str(group_id))

    def get_payments(self, student_id):
        return self.connection.getPaymentsByStudentId(str(student_id))

    def add_payment(self, data):
        return self.connection.addPayment(json.dumps(data))

    def print_payment(self):
        return print_action()

    def generate_cheque(self, data):
        json_data = json.dumps(data)
        payment = json.loads(json_data, object_hook=custom_payment_decoder)
        generate_pdf(payment)
        return self.connection.addPayment(json_data)

    def check_user(self, login, password):
        result = self.connection.checkUser(login, password)
        self.logger(result.content)
        if result.status_code == 401:
            return result.content
        else:
            self.quit_login()

import logging
import logging.config

from PathResolver import resource_path
from connections import Connection


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
        logging.config.fileConfig(fname=resource_path('conf/logback.conf'), disable_existing_loggers=False)
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

    def get_students(self, groupId):
        return self.connection.getStudentByGroupId(str(groupId))

    def get_payments(self, studentId):
        return self.connection.getPaymentsByStudentId(str(studentId))

    def add_payment(self, data):
        return self.connection.addPayment(data)

    def check_user(self, login, password):
        result = self.connection.checkUser(login, password)
        self.logger(result.content)
        if result.status_code == 401:
            return result.content
        else:
            self.quit_login()

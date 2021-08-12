import json
import logging
import logging.config
from collections import namedtuple

import requests
from requests import Response


def direction_decoder(direction_dict):
    return namedtuple('Direction', direction_dict.keys())(*direction_dict.values())


def group_decoder(group_dict):
    return namedtuple('Group', group_dict.keys())(*group_dict.values())


def student_decoder(student_dict):
    return namedtuple('Student', student_dict.keys())(*student_dict.values())


def teacher_decoder(teacher_dict):
    return namedtuple('Teacher', teacher_dict.keys())(*teacher_dict.values())


def payment_decoder(payment_dict):
    return namedtuple('Payment', payment_dict.keys())(*payment_dict.values())


class Connection:

    def __init__(self):
        self.cookies = ''
        self.headers = ''
        self.the_response = Response()
        self.the_response.error_type = "unauthorized"
        self.the_response.status_code = 401
        self.server_url = "http://localhost:9000/"
        self.host = 'crm.dataonline.uz'
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG,
                            filename='logs.log')
        self.logger = logging.getLogger(__name__)

    def getDirections(self):
        try:
            response = requests.get(self.server_url + "admin/get-all-directions", headers=self.headers)
            return json.loads(response.text, object_hook=direction_decoder)

        except Exception as ex:
            self.logger.error(f"Error occurred while get direction. Error: {ex}")
            return []

    def getGroups(self):
        try:
            response = requests.get(self.server_url + 'admin/get-all-groups', headers=self.headers)
            return json.loads(response.text, object_hook=group_decoder)

        except Exception as ex:
            self.logger.error(f"Error occurred while get groups. Error: {ex}")
            return []

    def getTeachers(self):
        try:
            response = requests.get(self.server_url + 'admin/get-teachers', headers=self.headers)
            return json.loads(response.text, object_hook=teacher_decoder)

        except Exception as ex:
            self.logger.error(f"Error occurred while get teachers. Error: {ex}")
            return []

    def getStudentByGroupId(self, groupId):
        try:
            response = requests.get(self.server_url + 'admin/students/' + str(groupId), headers=self.headers)
            return json.loads(response.text, object_hook=student_decoder)

        except Exception as ex:
            self.logger.error(f"Error occurred while get student by group-id. Error: {ex}")
            return []

    def getPaymentsByStudentId(self, studentId):
        try:
            response = requests.get(self.server_url + 'admin/get-payment-debt/' + str(studentId), headers=self.headers)
            return json.loads(response.text, object_hook=payment_decoder)

        except Exception as ex:
            self.logger.error(f"Error occurred while get payments by student-id. Error: {ex}")
            return []

    def addPayment(self, data):
        try:
            headers = {
                'Cookie': self.cookies,
                'Content-Type': 'application/json'
            }
            response = requests.post(url=self.server_url + "admin/add-payment", data=data, headers=headers)
            self.logger.debug(response)
            self.logger.debug(response.text)
            if response.status_code == 200:
                self.the_response._content = {
                    'code': 200, "text": response.text
                }
            else:
                self.the_response._content = {
                    'code': response.status_code, "error": response.text
                }
            return self.the_response.content

        except Exception as ex:
            self.logger.error(f"Error occurred while get payments by student-id. Error: {ex}")
            self.the_response._content = {
                'code': 400, "error": "To'lovni ma'lumotlar bazasiga kiritishda xatolik yuz berdi!"
            }
            return self.the_response.content

    def getLastPaymentId(self):
        try:
            response = requests.get(self.server_url + 'admin/get-last-payment-number', headers=self.headers)
            return response.text

        except Exception as ex:
            self.logger.error(f"Error occurred while get student by group-id. Error: {ex}")
            return ""

    def checkAccessPayment(self):
        try:
            return requests.get(self.server_url + 'check-access-payment', headers=self.headers)

        except Exception as ex:
            self.logger.error(f"Error occurred while get last payment id. Error: {ex}")
            return 0

    def checkUser(self, login, password):
        try:
            data = {'login': login, 'password': password}
            headers = {
                'Host': self.host,
                'Referer': self.server_url,
            }
            response = requests.post(url=self.server_url + "login", data=data, headers=headers, allow_redirects=False)
            self.cookies = response.headers['Set-Cookie']
            self.headers = {
                'Cookie': self.cookies,
                'Host': self.host,
                'Referer': self.server_url
            }
            if response.headers['Location'] == '/admin/':
                return self.checkAccessPayment()
            else:
                self.the_response._content = "Sizning to'lov tizimiga kirish uchun huquqingiz yo'q!"
                return self.the_response

        except Exception as ex:
            self.logger.error(f"Error occurred while authentication. Error: {ex}")
            self.the_response._content = "Login yoki parol noto'g'ri kiritildi iltimos tekshirib qaytadan kiriting!"
            return self.the_response

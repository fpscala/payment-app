import json
import logging
import logging.config

import requests
from requests import Response

from PathResolver import resource_path


class Connection:

    def __init__(self):
        self.cookies = ''
        self.headers = ''
        self.the_response = Response()
        self.the_response.error_type = "unauthorized"
        self.the_response.status_code = 401
        self.server_url = "http://192.162.1.17:9000/"
        self.host = 'crm.dataonline.uz'
        logging.config.fileConfig(fname=resource_path('conf/logback.conf'), disable_existing_loggers=False)
        self.logger = logging.getLogger(__name__)

    def getDirections(self):
        try:
            response = requests.get(self.server_url + "admin/get-all-directions", headers=self.headers)
            return json.loads(response.text)

        except Exception as ex:
            self.logger.error(f"Error occurred while get direction. Error: {ex}")
            return []

    def getGroups(self):
        try:
            response = requests.get(self.server_url + 'admin/get-all-groups', headers=self.headers)
            return json.loads(response.text)

        except Exception as ex:
            self.logger.error(f"Error occurred while get groups. Error: {ex}")
            return []

    def getTeachers(self):
        try:
            response = requests.get(self.server_url + 'admin/get-teachers', headers=self.headers)
            return json.loads(response.text)

        except Exception as ex:
            self.logger.error(f"Error occurred while get teachers. Error: {ex}")
            return []

    def getStudentByGroupId(self, groupId):
        try:
            response = requests.get(self.server_url + 'admin/attendance-students/' + groupId, headers=self.headers)
            return json.loads(response.text)

        except Exception as ex:
            self.logger.error(f"Error occurred while get student by group-id. Error: {ex}")
            return []

    def getPaymentsByStudentId(self, studentId):
        try:
            response = requests.get(self.server_url + 'admin/get-payment-debt/' + studentId, headers=self.headers)
            return json.loads(response.text)

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
            return json.loads(response.text)

        except Exception as ex:
            self.logger.error(f"Error occurred while get payments by student-id. Error: {ex}")
            return "To'lovni ma'lumotlar bazasiga kiritishda xatolik yuz berdi!"

    def getLastPaymentId(self):
        try:
            response = requests.get(self.server_url + 'admin/get-last-payment-number', headers=self.headers)
            return json.loads(response.text)

        except Exception as ex:
            self.logger.error(f"Error occurred while get student by group-id. Error: {ex}")
            return []

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
                self.the_response._content = {'code': 401,
                                              "error": "Sizning to'lov tizimiga kirish uchun huquqingiz yo'q!"}
                return self.the_response

        except Exception as ex:
            self.logger.error(f"Error occurred while authentication. Error: {ex}")
            self.the_response._content = {
                'code': 401, "error": "Login yoki parol noto'g'ri kiritildi iltimos tekshirib qaytadan kiriting!"
            }
            return self.the_response

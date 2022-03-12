import pyrebase 
import datetime
import time

class firebase_DB:
    def __init__(self):
        self.auth_data = {
            "apiKey":"개인키 숨김",
            "authDomain": "개인키 숨김",
            "databaseURL": "개인키 숨김",
            "projectId":"개인키 숨김",
            "storageBucket": "개인키 숨김",
            "messagingSenderId": "개인키 숨김",
            "appId": "개인키 숨김"
        } 
        self.DB = pyrebase.initialize_app(self.auth_data).database()
        self.get_data_count = self.get_data_cycle = 20

    def get_data(self, school, grade, Class):
        if self.get_data_count == self.get_data_cycle:
            self.main_data = {data.key():data.val() for data in self.DB.child("oneclickclass").get().each()}
            self.get_data_count = 0
        else:
            self.get_data_count += 1
        return self.main_data[school]['schedule_data'][grade][Class]

    def get_class_time(self, school):
        return self.main_data[school]['class_time']

    def write_visit(self, school, environment):
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f")[:-4]
        self.DB.child("oneclickclass").child(school).child("visit").update({time:environment})

    def add_school(self,school_name, grade, schedule_data):
        self.DB.child("oneclickclass").child(school_name).child('schedule_data').child(grade).update(schedule_data)

    def get_visit_data(self, school):
        all_data = self.DB.child("oneclickclass").child(school).child("visit").get().each()
        result = {}
        for request in [date.key() for date in all_data]:
            if request.split(" ")[0] in result.keys():
                result[request.split(" ")[0]]+=1
            else:
                result[request.split(" ")[0]] = 1

        return [[value.key(), value.val()] for value in all_data][::-1], result

    def get_zooom_count_data(self,school):
        all_data = self.DB.child("oneclickclass").child(school).child("open_zoom_count").get().each()
        result = {}
        for request in [date.key() for date in all_data]:
            if request.split(" ")[0] in result.keys():
                result[request.split(" ")[0]]+=1
            else:
                result[request.split(" ")[0]] = 1

        return [[value.key(), value.val()] for value in all_data][::-1], result

    def open_zoom_count(self, school,grade_class,client_ip, enviroment, subject, zoom_num):
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f")[:-4]
        self.DB.child('oneclickclass').child(school).child("open_zoom_count").update({time:f'{client_ip} {grade_class} {subject} {zoom_num} {enviroment}'})

from flask import Flask, render_template, request
from firebase_handler import firebase_DB

app = Flask(__name__)

db_handler = firebase_DB()

DEBUG_MODE = False

IGNORE_IP = ['220.76.81.127' , '172.30.1.25']

def get_file_name(environment):
    css_file_name = "css/pc.css"
    hyperlink = True
    if not environment == "pc":
        hyperlink = False
    if environment == "mobile" or environment == "iphone":
        css_file_name = "css/mobile.css"
    return css_file_name, hyperlink

def get_environment(request):
    user_info = request.headers.get('User-Agent')
    if 'mobile' in user_info.lower():
        if  'iphone' in user_info.lower():
            environment =  'iphone'
        elif 'ipad' in user_info.lower():
            environment =  'ipad'
        else:
            environment =  'mobile'
    else:
        environment = 'pc'
    
    return environment,user_info, get_client_ip(request)

def get_client_ip(request):
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return  request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']

def get_max_class(data):
    result = 0
    for Class in data['schedule']:
        if len(Class) > result:
            result = len(Class)
    
    return result 

def write_visit(user_info, client_ip,  environment,school, grade, Class, page):
    if not DEBUG_MODE and not client_ip in IGNORE_IP:
        db_handler.write_visit(school, f"{environment} {client_ip} {grade}학년 {Class}반 {page} ({user_info})")

@app.route('/<school>/<int:grade>/<int:Class>')

def main(school, grade, Class):
    schedule_data = db_handler.get_data(school, grade, Class)
    environment, user_info, client_ip = get_environment(request)
    css_file_name, hyperlink = get_file_name(environment)
    write_visit(user_info, client_ip, environment,school, grade, Class, 'main')
    max_class = get_max_class(schedule_data)
    
    return render_template('main.html',data={'grade_class':f'{grade}학년 {Class}반' ,
                                             'school':school,"schedule_data":schedule_data, 
                                             "hyperlink":hyperlink,
                                             "css_file_name":css_file_name, 
                                             'max_class':max_class,
                                             'class_time':db_handler.main_data[school]['class_time']})
    
@app.route('/<school>/<int:grade>/<int:Class>/select/<subject>')

def select(school, grade, Class, subject):

    select_data = db_handler.get_data(school, grade, Class)
    environment, user_info, client_ip = get_environment(request)
    css_file_name, hyperlink = get_file_name(environment)
    write_visit(user_info,client_ip, environment,school, grade, Class, subject)
    
    return render_template("select.html",data={'grade_class':f'{grade}학년 {Class}반',
                                                "schedule_data":select_data['select'][subject],
                                                'school':school, 
                                                "url":select_data['url'], 
                                                "hyperlink":hyperlink,
                                                "css_file_name":css_file_name})

@app.route('/<school>/open_zoom_count')

def open_zoom_count_see(school):

    visit_data,date_data  = db_handler.get_zooom_count_data(school)

    return render_template("visit.html",date_data=date_data, visit_data = visit_data, data_len = len(visit_data))

@app.route('/<school>/open_zoom_count/<grade_class>/<subject>/<zoom_num>')

def open_zoom_count(school,grade_class, subject, zoom_num):
    
    db_handler.open_zoom_count(school,grade_class,get_client_ip(request), request.headers.get('User-Agent'),subject, zoom_num)

    return 'good'

@app.route('/<school>/visit')

def see_visit_data(school):
    
    visit_data,date_data  = db_handler.get_visit_data(school)

    return render_template("visit.html",date_data=date_data, visit_data = visit_data, data_len = len(visit_data))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
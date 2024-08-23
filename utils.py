from questions import title as form
from questions import new_dropdown_question as dropdown
from questions import new_multiplechoice_question as mult_choice
from questions import new_text_question as text
from questions import update_json
from questions import update_form
from CreateDatabase import createDataBase


def dropdown_q():
    boool = 1
    options = []
    while boool:
        options+= input("Add the desired option: ")
        boool = int(input ('''Do you want to add another option?
        1: yes
        0: no? '''))
    req = True if int(input('''The question is required?
    1: yes
    0: no ''')) == 1 else False
    shuff = True if int(input('''The options can appear in any order? 
    1: yes
    0: no ''')) ==1 else False
    return options, req, shuff


def mult_choice_q():
    options, req, shuff = dropdown_q()
    type = True if int(input('''How many options can be selected?
    1: only one
    0: multiple ''')) ==1 else False
    return options, req, shuff, type

def text_q():
    long_ = True if int(input('''The question requires a short answer?
    1: yes
    0: no ''')) == 1 else False
    req = True if int(input('''The question is required?
    1: yes
    0: no ''')) == 1 else False
    return long_, req

def config_form():
    form_name = input("Insert the name of the form: ")
    description = input("Insert the description of the form: ")

    new_form = form(form_name)

    boool = True if int(input('''Do you want to add questions to the form? 
            1: yes
            0: no ''')) == 1 else False
    preg = []

    if boool:
        pos = 0
        
        while boool:
            title = input("Insert the title of the question: ")
            type = int(input('''What type of question? 
            0: dropdown
            1: multiple choice
            2: text '''))
            if type == 0:
                options, req, shuff = dropdown_q()
                q1 = dropdown(title, options, pos, req, shuff)
                preg.append(q1)
                pos +=1
            
            elif type == 1:
                options, req, shuff, type = mult_choice_q()
                q2 = mult_choice(title, options, pos, req, type, shuff)
                preg.append(q2)
                pos+=1
            elif type == 2:
                long_, req = text_q()
                q3 = text(title, pos, req)
                preg.append(q3)
                pos +=1
            else: 
                print(Exception("Invalid input"))
            boool = True if int(input('''Do you want to add  another questions to the form?
            1: yes
            0: no ''')) == 1 else False

    return new_form, preg, description


def create_form(form_service):
    new_form, preg, description = config_form()
    # Creates the initial form
    result = form_service.forms().create(body=new_form).execute()

    #Adding name and id to a json
    id_ = result["formId"]
    name_ = result['info']['title']
    update_json("forms.json", name_, id_)

    question_setting = (
        form_service.forms()
        .batchUpdate(formId=id_, body=update_form(description))
        .execute())
    
    get_form = form_service.forms().get(formId=id_).execute()
    form_link = get_form.get('responderUri')

    # Adds questions to the form
    if preg: 
        question_setting = (
            form_service.forms()
            .batchUpdate(formId=result["formId"],  body={"requests": preg})
            .execute()
        )

    #######################################################################
    #######################################################################
    user = input("To create the PostgreSQL database, insert username: ")
    password = input("password: ")
    host = input("host: ")
    port = input("port: ")
    #Create database
    try:
        createDataBase(name_, user, password, host , port)
    except Exception as e:
        print(e)
    return form_link

import json

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file) 
        loads = []
        for item in data.keys():
            loads.append(f"{data[item]} : {item}")
        return loads
    except FileNotFoundError:
        print(f"El archivo {file_path} no se encontró.")
        return None

import os, json

def title(title: str):
    NEW_FORM = {
        "info": {
            "title": title,
        }
    }

    return NEW_FORM

def update_form(description: str):
    UPDATE_FORM ={
        "requests": [
            {
                "updateFormInfo": {
                    "info": {
                        "description": (description)
                    },
                    "updateMask": "description",
                }
            }
        ]
    }
    return UPDATE_FORM

# Request body to add a multiple-choice question
def new_text_question(title: str, index: int, required: bool = False, long_answer: bool = False ): 
    NEW_QUESTION = {
                "createItem": {
                    "item": {
                        "title": (title),
                        "questionItem": {
                                "question": {
                                    "required": required,
                                    "textQuestion": {
                                        "paragraph": long_answer
                                    }
                                }
                            }
                        },
                    "location": {"index": index},
                }
            }
    return NEW_QUESTION


def new_multiplechoice_question(title: str, options, index: int, required: bool = False, type_: bool = False, shuffle: bool = False):
    type = "RADIO" if type_ else "CHECKBOX"
    NEW_QUESTION = {
                "createItem": {
                    "item": {
                        "title": title,
                        "questionItem": {
                            "question": {
                                "required": required,
                                "choiceQuestion": {
                                    "type": type,
                                    "options": [{"value": option} for option in options],
                                    "shuffle": shuffle
                                }
                            }
                        }
                    },
                    "location": {
                        "index": index 
                    }
                }
            }
    return NEW_QUESTION

def new_dropdown_question(title: str, options, index: int, required: bool= False, shuffle: bool = False):
    NEW_QUESTION ={
                "createItem": {
                    "item": {
                        "title": title,
                        "questionItem": {
                            "question": {
                                "required": required,
                                "choiceQuestion": {
                                    "type": "DROP_DOWN",
                                    "options": [{"value": option} for option in options],
                                    "shuffle": shuffle 
                                }
                            }
                        }
                    },
                    "location": {
                        "index": index  # Cambia según dónde quieres que aparezca la pregunta
                    }
                }
            }
    return NEW_QUESTION

def update_json(path: str, name: str, id: str):

    if os.path.isfile(path):
        with open(path, 'r') as file:
            datos_actuales = json.load(file)
    else:
        datos_actuales = {}
    datos_actuales[id] = name
    with open(path, 'w') as file:
        json.dump(datos_actuales, file)


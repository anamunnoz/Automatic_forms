from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from utils import create_form, load_json
from answers import save_responses_to_csv

from CreateDatabase import createDataBase, insert_db

#######################################################################
#######################################################################

SCOPES = ["https://www.googleapis.com/auth/forms.body", "https://www.googleapis.com/auth/forms.responses.readonly"]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage("token.json")
creds = None
if not creds or creds.invalid:
  flow = client.flow_from_clientsecrets("client_secrets.json", SCOPES)
  creds = tools.run_flow(flow, store)

form_service = discovery.build(
    "forms",
    "v1",
    http=creds.authorize(Http()),
    discoveryServiceUrl=DISCOVERY_DOC,
    static_discovery=False,
)

#######################################################################
#######################################################################

aux = True if (int(input('''Do you want to create a form or update a database associated with a form?
    1: create a form
    0 update a database '''))) == 1 else False

if aux == True: 
    link = create_form(form_service)
    print(link)
else:
    arch = load_json("forms.json")
    mess = "Insert the ID of the form you want to update. Below is a list of the names and IDs of the forms you have created \n"
    for item in arch:
        mess += item + "\n"
    id = input(mess)

    info = form_service.forms().get(formId=id).execute()
    form_title = info['info']['title']

    save_responses_to_csv(form_service, "answers.csv", id)
    user = input("To create the PostgreSQL database, insert username: ")
    password = input("password: ")
    host = input("host: ")
    port = input("port: ")
    insert_db("answers.csv", form_title.replace(" ", ""), form_title, user, password, host, port)





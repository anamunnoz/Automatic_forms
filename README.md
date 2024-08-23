# Automatic_forms
A project for the third-year computer science internship, which involves automatically creating Google Forms and storing the results in a database.
### Requirements:
- Have a project in Google Cloud: [link here](https://developers.google.com/workspace/guides/create-project?hl=en)
- Obtain Google Forms credentials: [link here](https://developers.google.com/forms/api/quickstart/python?hl=en)
  - After obtaining and downloading the *json* file, rename it to *client_secrets.json* and place it in the same project folder.

### To run the project:
Use the following command `python3 main.py` and follow the console instructions correctly.  
The project downloads a *csv* file with the responses and also creates a *PostgreSQL* database with the same name as the form.

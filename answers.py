import csv
def save_responses_to_csv(service, output_file, form_id):
    responses =  service.forms().responses().list(formId=form_id).execute()

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Extraer las respuestas y escribir las cabeceras
        responses_list = responses.get('responses', [])
        if responses_list:

            headers = ['responseId']
            first_response = responses_list[0]
            
            question_headers = []
            for question_id, answer in first_response['answers'].items():
                question_headers.append(f'question_{question_id}')
            
            writer.writerow(headers + question_headers)
            

            for response in responses_list:
                row = [response.get('responseId')]
                for question_id in question_headers:
                    question_key = question_id.split('_')[1]
                    answer = response['answers'].get(question_key, {}).get('textAnswers', {}).get('answers', [{}])[0].get('value', '')
                    row.append(answer)
                writer.writerow(row)

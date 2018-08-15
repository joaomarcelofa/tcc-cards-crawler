import lxml.html
from selenium import webdriver
from lxml import etree
import xlsxwriter

def process_data(data):
    list_len: int = len(data)
    if list_len == 6 or list_len == 7:
        question: str = data[0]
        correct_answer = data[(list_len - 1)]
        alternatives = data[1:-1]

        return dict({
            'question': question,
            'alternatives': alternatives,
            'correct_answer': correct_answer
        })
    else:
        return None

def format(question):
    new_alternatives = []
    for alternative in question['alternatives']:
        new_alternatives.append(alternative[3:])

    new_correct_answer = question['correct_answer'][1]
    index_of_correct_alternative: int

    if new_correct_answer is 'A':
        index_of_correct_alternative = 0
    elif new_correct_answer is 'B':
        index_of_correct_alternative = 1
    elif new_correct_answer is 'C':
        index_of_correct_alternative = 2
    elif new_correct_answer is 'D':
        index_of_correct_alternative = 3
    elif new_correct_answer is 'E':
        index_of_correct_alternative = 4

    if len(new_alternatives) is 5:
        if index_of_correct_alternative is 4:
            new_alternatives = new_alternatives[1:]
            index_of_correct_alternative = index_of_correct_alternative - 1
        else:
            new_alternatives = new_alternatives[:-1]

    return dict({
        'questao': question['question'],
        'opcao1': new_alternatives[0],
        'opcao2': new_alternatives[1],
        'opcao3': new_alternatives[2],
        'opcao4': new_alternatives[3],
        'opcaoCorreta': new_alternatives[index_of_correct_alternative]
    })

def save_in_excel(questions):
    workbook = xlsxwriter.Workbook('teste.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, 'questao')
    worksheet.write(0, 1, 'opcao1')
    worksheet.write(0, 2, 'opcao2')
    worksheet.write(0, 3, 'opcao3')
    worksheet.write(0, 4, 'opcao4')
    worksheet.write(0, 5, 'opcaoCorreta')

    row = 1
    for question in questions:
        worksheet.write(row, 0, question['questao'])
        worksheet.write(row, 1, question['opcao1'])
        worksheet.write(row, 2, question['opcao2'])
        worksheet.write(row, 3, question['opcao3'])
        worksheet.write(row, 4, question['opcao4'])
        worksheet.write(row, 5, question['opcaoCorreta'])
        row += 1

    workbook.close()

#Open WebDriver
driver = webdriver.Firefox(executable_path='./geckodriver/geckodriver.exe')
driver.get('http://www.professor.bio.br/ingles/provas_questoes.asp?section=Adjetivos&curpage=18')
tree = lxml.html.fromstring(driver.page_source)
driver.close()

etree.strip_tags(tree, 'br')

tableIterator = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
questions = []

for iterator in tableIterator:
    current_xpath = f'/html/body/table/tbody/tr/td[1]/table/tbody/tr[8]/td/table/tbody/tr[{iterator}]/td[2]/font/font/text()'
    data_extracted = tree.xpath(current_xpath)
    current_question = []

    for data in data_extracted:
        trim_data = data.strip(" ")
        if ('\n' not in data) and (data is not '') and (len(trim_data) > 0):
            current_question.append(data.strip())

    question = process_data(current_question)
    if question is not None:
        questions.append(format(question))

save_in_excel(questions)

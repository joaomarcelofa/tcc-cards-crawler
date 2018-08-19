import lxml.html
import xlsxwriter
from url import urls
from selenium import webdriver
from lxml import etree


def crawl(root_url, driver):
    row_index = 1
    xpath_first_page = "/html/body/table/tbody/tr/td[1]/table/tbody/tr[11]/td/div/a"
    x_path_other_pages = "/html/body/table/tbody/tr/td[1]/table/tbody/tr[11]/td/div/b/font/a"
    workbook = xlsxwriter.Workbook('teste.xlsx')
    worksheet = workbook.add_worksheet()
    put_excel_headers(worksheet)

    driver.get(root_url)
    try:
        element = driver.find_element_by_xpath(xpath_first_page)
        tree = lxml.html.fromstring(driver.page_source)
        current_questions = get_content(tree)
        save_in_excel(row_index, current_questions, worksheet)
        row_index += len(current_questions)
        element.click()
    except Exception:
        driver.close()
        workbook.close()

    while True:
        try:
            element = driver.find_element_by_xpath(x_path_other_pages)
            tree = lxml.html.fromstring(driver.page_source)
            questions = get_content(tree)
            save_in_excel(row_index, questions, worksheet)
            row_index += len(questions)
            element.click()
        except Exception:
            driver.close()
            workbook.close()


def get_content(tree):
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
    return questions


def process_data(data):
    list_len: int = len(data)
    if len(data[list_len - 1]) is 3 and (list_len is 6 or list_len is 7):
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

def put_excel_headers(worksheet):
    worksheet.write(0, 0, 'questao')
    worksheet.write(0, 1, 'opcao1')
    worksheet.write(0, 2, 'opcao2')
    worksheet.write(0, 3, 'opcao3')
    worksheet.write(0, 4, 'opcao4')
    worksheet.write(0, 5, 'opcaoCorreta')


def save_in_excel(row_index, questions, worksheet):
    for question in questions:
        worksheet.write(row_index, 0, question['questao'])
        worksheet.write(row_index, 1, question['opcao1'])
        worksheet.write(row_index, 2, question['opcao2'])
        worksheet.write(row_index, 3, question['opcao3'])
        worksheet.write(row_index, 4, question['opcao4'])
        worksheet.write(row_index, 5, question['opcaoCorreta'])
        row_index += 1

driver = webdriver.Firefox(executable_path='./geckodriver/geckodriver.exe') #Open WebDriver
url_dict = urls().geturls()
crawl(url_dict["adjetivos"], driver)

import lxml.html
import xlsxwriter
from url import urls
from selenium import webdriver
from lxml import etree


def crawl():
    driver = webdriver.Firefox(executable_path='./geckodriver/geckodriver.exe') #Open WebDriver
    url_dict = urls().geturls()
    row_index = 1
    xpath_first_page = "/html/body/table/tbody/tr/td[1]/table/tbody/tr[11]/td/div/a"
    xpath_other_pages = "/html/body/table/tbody/tr/td[1]/table/tbody/tr[11]/td/div/b/font/a"
    workbook = xlsxwriter.Workbook('teste.xlsx')
    worksheet = workbook.add_worksheet()
    put_excel_headers(worksheet)

    for key in url_dict.keys():
        tag = key
        driver.get(url_dict[key])
        try:
            tree = lxml.html.fromstring(driver.page_source)
            current_questions = get_content(tree)
            number_of_pages = get_number_of_pages(tree)
            save_in_excel(row_index, tag, current_questions, worksheet)
            row_index += len(current_questions)
            element = driver.find_element_by_xpath(xpath_first_page)
            element.click()

            for index in range(2, number_of_pages):
                element = driver.find_element_by_xpath(xpath_other_pages)
                tree = lxml.html.fromstring(driver.page_source)
                questions = get_content(tree)
                save_in_excel(row_index, tag, questions, worksheet)
                row_index += len(questions)
                element.click()

        except Exception:
            print("Erro, mas continua ai!")

    driver.close()
    workbook.close()




def get_number_of_pages(tree):
    xpath_qtd_pages = "/html/body/table/tbody/tr/td[1]/table/tbody/tr[11]/td/div/font"
    qtd_pages_element = tree.xpath(xpath_qtd_pages)
    trim_data = (qtd_pages_element[0].text).strip(" ")
    total_of_pages = trim_data[-2:]
    return int(total_of_pages)


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
    worksheet.write(0, 0, 'tag')
    worksheet.write(0, 1, 'questao')
    worksheet.write(0, 2, 'opcao1')
    worksheet.write(0, 3, 'opcao2')
    worksheet.write(0, 4, 'opcao3')
    worksheet.write(0, 5, 'opcao4')
    worksheet.write(0, 6, 'opcaoCorreta')


def save_in_excel(row_index, tag, questions, worksheet):
    for question in questions:
        worksheet.write(row_index, 0, tag)
        worksheet.write(row_index, 1, question['questao'])
        worksheet.write(row_index, 2, question['opcao1'])
        worksheet.write(row_index, 3, question['opcao2'])
        worksheet.write(row_index, 4, question['opcao3'])
        worksheet.write(row_index, 5, question['opcao4'])
        worksheet.write(row_index, 6, question['opcaoCorreta'])
        row_index += 1


crawl()
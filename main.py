import lxml.html
from selenium import webdriver
from lxml import etree

driver = webdriver.Firefox(executable_path='./geckodriver/geckodriver.exe')
driver.get('http://www.professor.bio.br/ingles/provas_questoes.asp?section=Adjetivos')
tree = lxml.html.fromstring(driver.page_source)
driver.close()

etree.strip_tags(tree, 'br')
results = tree.xpath('/html/body/table/tbody/tr/td[1]/table/tbody/tr[8]/td/table/tbody/tr[2]/td[2]/font/font/text()')
teste = []

for result in results:
    trim_result = result.strip(" ")
    if ('\n' not in result) and (result is not '') and (len(trim_result) > 0):
        teste.append(result.strip())

print(teste)

#TODO: Implemetar uma interface que cospe em TXT
#TODO: Lógica pra fazer essa caralha é verificar a resposta se tem [A], [B] e etc, só assim ele poe no txt
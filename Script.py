import csv
import os
import requests
import yagmail
from pathlib import Path
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()  # faz load do ficheiro de variaveis de ambiente

yag = yagmail.SMTP(user=os.getenv('EMAIL_YAGMAIL'),
                   password=os.getenv('PSWD_YAGMAIL'))  # incializa uma conta para ser possivel enviar email


def get_different_rows(notas_prov, csv_notas):
    list_diferent = [[]]
    for new_rows in notas_prov:
        exists = False
        for old_rows in csv_notas:
            if new_rows == old_rows:
                exists = True
        if not exists:  # significa que uma linha da nova tabela nao existe na velha
            list_diferent.append(new_rows)
    list_diferent.pop(0)
    return list_diferent


def write_table_to_file(name_of_file, table):
    with open(name_of_file, 'w', newline='') as myfile:
        for row in table:
            for item in row:
                myfile.write(item)
                if item != row[-1]:
                    myfile.write(',')
            myfile.write('\n')


def read_csv_to_list(name_of_file):
    with open(name_of_file, newline='') as f:
        reader = csv.reader(f)
        my_list = list(reader)
    return my_list


def tableDataText(table):
    def rowgetDataText(tr, coltag='td'):
        return [td.get_text(strip=True) for td in tr.find_all(coltag)]

    rows = []
    trs = table.find_all('tr')
    headerow = rowgetDataText(trs[0], 'th')
    if headerow:  # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs:  # for every table row
        rows.append(rowgetDataText(tr, 'td'))  # data row
    return rows


def operations(table_notas, path_name, tipo):
    global note
    notas = tableDataText(table_notas)  # list of lines that contain the course and their final grade
    notas.pop(0)  # retira primeiro valor que contem o cabecalho dad tabela
    my_file = Path(path_name)
    # se nao existir quer dizer que é primeira vez que se corre o script
    # ou a primeira vez que se corre e existe dados na tabela notas_provisorias
    if my_file.exists():

        csv_notas = read_csv_to_list(path_name)
        # se as listas nao sao iguais significa que o novo scrapp detetou novas
        # entradas na tabela notas_provisorias
        if notas != csv_notas:
            list_of_differences = get_different_rows(notas, csv_notas)
            print("NEW GRADES")
            print(list_of_differences)

            for note in list_of_differences:

                mensagem = "Recebida nova nota: " + tipo + \
                           "\n\nModelo: " + str(note[0]).replace('avaliaÃ§Ã£o', 'avaliação').replace('AvaliaÃ§Ã£o','Avaliação').replace('ContÃ\xadnua', 'Continua').replace('contÃ\xadnua', 'continua').replace('ExcepÃ§Ã£o','Excepção').replace('InvestigaÃ§Ã£o', 'Investigação') + \
                           "\nUnidade Curricular: " + str(note[1]).replace('MultimÃ©dia', 'Multimédia').replace('InvestigaÃ§Ã£o', 'Investigação').replace('ProgramaÃ§Ã£o', 'Programação').replace('LaboratÃ³rio','Laboratório') + \
                           "\nElemento: " + str(note[2]).replace('1Âº', '1º').replace('2Âº', '2º').replace('3Âº','3º').replace('TeÃ³rico-PrÃ¡tica', 'Teorico-Prática').replace('TeÃ³rico', 'Teorico').replace('prÃ¡tica','prática').replace('PrÃ¡tica', 'Prática').replace('prÃ¡tico', 'prático').replace('Ã¢mbito', 'Âmbito').replace('ProgramaÃ§Ã£o', 'Programação').replace('FrequÃªncia', 'Frequência') + \
                           "\nNota: " + str(note[3]) + \
                           "\nLancado por: " + str(note[4]).replace('JosÃ©', 'José') + \
                           "\nData: " + str(note[5])
                yag.send(os.getenv('EMAIL_FOR_SENDING_NOTIFICATIONS'), 'UFP grades notification', mensagem)

                write_table_to_file(path_name,notas)
        else: print("Nao existem novas notas submetidas")        
    else:
        write_table_to_file(path_name, notas)


number = os.getenv('USER_LOGIN')
pswd = os.getenv('USER_PSWD')
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/81.0.4044.122 Chrome/81.0.4044.122 Safari/537.36'}
login_data = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    'ctl00$ContentPlaceHolder1$Accordion1_AccordionExtender_ClientState': '0',
    'ctl00$ContentPlaceHolder1$AccordionPane1_content$txtLogin': number,
    'ctl00$ContentPlaceHolder1$AccordionPane1_content$Button1': 'Validar',
    'ctl00$ContentPlaceHolder1$AccordionPane1_content$txtPassword': pswd,
    'ctl00$ContentPlaceHolder1$AccordionPane1_content$ddlIMG': 'pt'
}

# guarda a sessao em SIUFP
with requests.Session() as s:
    print("Fetching data from SIUFP...")
    url = "https://portal.ufp.pt/authentication.aspx"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    login_data['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
    login_data['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']
    login_data['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
    page = s.post(url, data=login_data, headers=headers)

    # guarda as notas parciais ou seja as notas de testes
    notas_p = s.get("https://portal.ufp.pt/Notas/Parcial.aspx", headers=headers)
    # guarda as notas finais lancadas provisoriamente
    notas_f_p = s.get("https://portal.ufp.pt/Notas/FinalProv.aspx", headers=headers)
    # guarda as notas finais recentes (do ano letivo presente) de cada disciplina
    notas_f = s.get("https://portal.ufp.pt/Notas/Recente.aspx", headers=headers)

notas_p_soup = BeautifulSoup(notas_p.content, "html.parser")
table_notas_p = notas_p_soup.find(lambda tag: tag.name == 'div' and tag.has_attr('id') and tag[
    'id'] == "ctl00_ContentPlaceHolder1_AccordionPane1_content_TabContainer1_TabPanel1")

notas_f_p_soup = BeautifulSoup(notas_f_p.content, "html.parser")
table_notas_f_p = notas_f_p_soup.find(lambda tag: tag.name == 'div' and tag.has_attr('id') and tag[
    'id'] == "ctl00_ContentPlaceHolder1_AccordionPane1_content_TabContainer1_TabPanel1")

notas_f_soup = BeautifulSoup(notas_f.content, "html.parser")
table_notas_f = notas_f_soup.find(lambda tag: tag.name == 'div' and tag.has_attr('id') and tag[
    'id'] == "ctl00_ContentPlaceHolder1_AccordionPane1_content_TabContainer1_TabPanel1")

# apenas realiza tasks se a tabela obtida da web tiver notas de testes
if table_notas_p is not None:
    operations(table_notas_p, "notas_provisorias.csv", "provisoria")

if table_notas_f_p is not None:
    operations(table_notas_f_p, "notas_fimais_provisorias.csv", "final provisoria")

if table_notas_f is not None:
    operations(table_notas_f, "notas_finais.csv", "final")

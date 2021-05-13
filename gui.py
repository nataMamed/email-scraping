from PySimpleGUI import PySimpleGUI as sg
import pandas as pd
from extractor import Extractor


# Layout
class GUI:

    sg.theme('Reddit')

    welcome = """Bem-vindo a ferramenta de extração de e-mails e rgs.\
Abaixo, você terá que escolher se irá procurar o usuário de e-mail
a partir de uma URL ou se irá utilizar um arquivo específico.
Utilize a URL abaixo como exemplo: 

link: https://github.com/nataMamed/WebScraping/blob/main/data/emails_rgs.csv"""

    layout = [
        [sg.Text(welcome, enable_events=True)],
        [sg.Text('Url ou Diretório do arquivo:'), sg.Input(key='input')],
        [sg.Checkbox('Url', key='url'), sg.Checkbox('Aquivo', key='file')],
        [sg.Text(' '*50, key='warning', text_color='red')],
        [sg.Text('Usuário a ser procurado'), sg.Input(key='user')],
        [sg.Button('Procurar')],
        [sg.Text('Resultados:')],
        [sg.Text('Server:'), sg.Text(
            ' '*30, auto_size_text=True, key='server')],
        [sg.Text('Resultados:'), sg.Text(' '*30, key='rg')],
        [sg.Text('Quantidade de digitos do RG:'),
         sg.Text(' '*10, key='len_rg')],
    ]

    window = sg.Window('Demo - User finder', layout)


    @staticmethod
    def fetch_data(email:str):

        emails_rgs = pd.read_csv('data/emails_rgs.csv')
        emails_rgs['server'] = [email.split('@')[1] for email in emails_rgs.email]
        emails_rgs['user'] = [email.split('@')[0] for email in emails_rgs.email]

        data = emails_rgs[emails_rgs['email'] == email]
        server = data['server'].values[0]
        rg = data['rg'].values[0]
        len_rg = len(rg.replace('.', '').replace('-', ''))

        return (server, rg, len_rg)

    def run(self):

        while True:
            events, values = self.window.read()
            if events == sg.WIN_CLOSED:
                break
            if events == 'Procurar':

                regex_user = values['user'] + '@\w+\.{1}\w+'
                extractor = Extractor(regex_user)

                if values['url'] != values['file']:
                    try:
                        if values['url']:
                            extractor.extract_from_url(values['input'])
                        elif values['file']:
                            extractor.extract_from_file(values['input'])

                        email = list(extractor.elements)[0]
                        server, rg, len_rg = self.fetch_data(email)

                        self.window['server'].update(server)
                        self.window['rg'].update(rg)
                        self.window['len_rg'].update(len_rg)

                    except:
                        self.window['warning'].update('Endereço não encontrado')

                elif not values['input'] or not values['user']:
                    self.window['warning'].update('Preencha todos os campos')

                else:
                    self.window['warning'].update('Escolha uma opções')

        self.window.close()



if __name__ == '__main__':
    gui = GUI()
    gui.run()

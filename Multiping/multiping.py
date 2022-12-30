import os
from PySimpleGUI import PySimpleGUI as sg

sep = f'\n'+'-'*80+'\n'


def ping():
    if os.path.exists('ip_list.txt'):
        if os.stat('ip_list.txt').st_size == 0:
            sg.Popup('Adicione os IPs')
            os.startfile('ip_list.txt')
        else:
            with open('ip_list.txt') as file:
                ip_list = file.read()
                ip_list = ip_list.splitlines()
                for i in ip_list:
                    host = i.split()[0]
                    ip = i.split()[1]
                    res = os.popen(f'ping {ip} -n 2').read()
                    if 'Esgotado o tempo limite' in res:
                        sg.Print(res+sep)
                        print(str(host)+'\t' +
                              '['+str(ip)+']'+'\t'+'SEM CONEXÃO'+'\n')
                    elif 'Host de destino' in res:
                        sg.Print(res+sep)
                        print(str(host)+'\t' +
                              '['+str(ip)+']'+'\t'+'SEM CONEXÃO'+'\n')
                    else:
                        sg.Print(res+sep)
                        print(str(host)+'\t'+'['+str(ip)+']'+'\t'+'OK'+'\n')
    else:
        save('')


def save(ips):
    f = open('ip_list.txt', 'a')
    if ips != '':
        f.write(ips+'\n')
    f.close()


sg.theme('DarkBlue14')
layout = [
    [sg.Output(size=(55, 20))],
    [sg.Button('Ping'), sg.Button('Create')]
]

window = sg.Window('MultiPing', layout)

while True:
    events, values = window.read()
    if events == sg.WINDOW_CLOSED:
        break

    if events == 'Create':
        # ips = values['ips']
        save('')

    if events == 'Ping':
        ping()
        sg.easy_print_close()

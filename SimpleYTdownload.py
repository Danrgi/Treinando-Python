import os
import datetime
from pytube import YouTube
from PySimpleGUI import PySimpleGUI as sg

sep = f'\n'+'-'*140+'\n'
file_path = os.path.expanduser('~')+'\Downloads'


def progress(chunk, file_handle, remaining):
    percent = (100*(file_size-remaining))/file_size
    sg.Print("{:00.0f}% concluido".format(percent))


def download(yturl):
    print(yturl)
    print("Acessando URL...")

    try:
        video = YouTube(yturl, on_progress_callback=progress)
    except:
        print('ERRO: Não foi possivel fazer o download do video!')

    video_type = video.streams.filter(
        progressive=True, file_extension="mp4").get_highest_resolution()
    title = video.title
    sg.Print(format(title))
    print(f"Video: {format(title)} - {str(datetime.timedelta(seconds=video.length))} - {round(video_type.filesize/1048576, 1)}MB")
    forbstr = ['<', '>', ':', '"', '/', '|', '?', '*', '\\']
    for i in forbstr:
        title = title.replace(i, '')
    path = file_path+'\\'+title+'.mp4'
    if os.path.exists(path):
        sg.easy_print_close()
        print('Este video já foi baixado!'+sep)
    else:
        global file_size
        file_size = video_type.filesize
        video_type.download(file_path)
        sg.easy_print_close()
        print(f'Download Concluido!'+sep)


sg.theme('Material1')
layout = [
    [sg.Text('YouTube URL: '), sg.Input(key='yturl'),
     sg.Button('Download'), sg.Button('Abrir Pasta')],
    [sg.Output(size=(80, 10), font=('Helvetica 10'))]
]

window = sg.Window('Simple YouTube Downloader', layout)

while True:
    events, values = window.read()
    if events == sg.WINDOW_CLOSED:
        break
    if events == 'Download':
        download(values['yturl'])
    if events == 'Abrir Pasta':
        os.startfile(file_path)


file_size = 0

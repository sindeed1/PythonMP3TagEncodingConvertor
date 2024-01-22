import sys
import os
import glob
from textwrap import indent
from token import ENCODING



from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

def convert_to_utf8(file_path):
    audio = MP3(file_path, ID3=EasyID3)
    print('Type of audio=' + str(type(audio)))
    for key in audio.keys():
        print('     Key=' + key + '; Type="'+ str(type(key)) + '"')
        #print('     Type=' + str(type(key)))
        if isinstance(audio[key], list):
            for i in range(len(audio[key])):
                print('         i=' + str(i) + '; Type=' + str(type(i)))
                print('         Key[' + str(i) + ']=' + audio[key][i])

                #print('encode(latin1)=')
                enco=audio[key][i].encode('latin1')
                print('         encode(latin1)=' + str(enco) + '; Type=' + str(type(enco)))

                #print('decode(cp1256)=')
                deco=enco.decode('cp1256') #Windows Arabic
                print('         decode(cp1256)=' + deco + ';Type=' + str(type(deco)))


                #print('         encode(cp1256)=')
                #enco=deco.encode('cp1256')
                #print(enco)
                
                #print('         decode(utf-8)=')
                #deco=enco.decode('utf-8')
                #print(deco)
                
                audio[key][i] = deco #audio[key][i].encode('latin1').decode('cp1256')
                #audio[key][i] = audio[key][i].encode('cp1256').decode('utf-8')
                tag=audio[key][i]
                print('         audio[key][i]=' + tag)
                #print('         audio[key][i]=' + audio[key][i])
        else:
            tag=audio[key]
            print('         Tag=' + tag)
            audio[key] = audio[key].encode('latin1').decode('cp1256')
            
    audio.save()
    #DEBUG:
    for key in audio.keys():
        print('DEBUG     Key=' + key)
        if isinstance(audio[key], list):
            for i in range(len(audio[key])):
                print('DEBUG    audio[key][i]=' + audio[key][i])
        else:
            tag=audio[key]
            print('         Tag=' + tag)
            audio[key] = audio[key].encode('latin1').decode('cp1256')
    

def search_and_convert(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.mp3'):
                file_path = os.path.join(root, file)
                print('File to convert:'+ file_path)
                convert_to_utf8(file_path)
                print()

print('Default system encoding='+sys.getdefaultencoding())
folder_path = 'C:\\Ammar\\Programming\\Projects\\PythonConvertID3ToUTF-8\\TestSongs'

print('Folder to search and convert=' + folder_path)
search_and_convert(folder_path)

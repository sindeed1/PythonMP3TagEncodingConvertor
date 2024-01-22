import os
import eyed3
import chardet
import sys

def convert_to_utf8(file):
        # Öffnen der Datei als Mp3AudioFile-Objekt
        audiofile = eyed3.Mp3AudioFile(file)
        # Zugriff auf das Tag-Objekt
        tag = audiofile.getTag()
        # Lesen des Titels aus dem Tag
        title = tag.getTitle()
        # Erkennen der Kodierung des Titels mit chardet
        encoding = chardet.detect(title)["encoding"]
        # Überprüfen, ob die Kodierung nicht UTF-8 ist
        if encoding != "utf-8":
            # Konvertieren des Titels in UTF-8
            title = title.decode(encoding).encode("utf-8")
            # Schreiben des Titels zurück in den Tag
            tag.setTitle(title)
            # Speichern der Änderungen in der Datei
            tag.update()
 
def search_and_convert(folder_path):
    # Durchlaufen aller Dateien im Ordner
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.mp3'):
                file_path = os.path.join(root, file)
                print('File to convert:'+ file_path)
                convert_to_utf8(file_path)
                print()

# Definieren des Ordners, der durchsucht werden soll
print('Default system encoding='+sys.getdefaultencoding())
folder_path = 'C:\\Ammar\\Programming\\Projects\\PythonConvertID3ToUTF-8\\TestSongs'

print('Folder to search and convert=' + folder_path)
search_and_convert(folder_path)

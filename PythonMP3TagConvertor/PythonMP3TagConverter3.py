
import os
import mutagen.id3

def findMP3s(path):
    for child in os.listdir(path):
        child= os.path.join(path, child)
        if os.path.isdir(child):
            for mp3 in findMP3s(child):
                yield mp3
        elif child.lower().endswith(u'.mp3'):
            yield child

musicroot= 'C:\\Ammar\\Programming\\Projects\\PythonConvertID3ToUTF-8\\TestSongs'
tryencodings= 'cp1256', 'gb18030', 'cp1252'
  
for path in findMP3s(musicroot):
    id3= mutagen.id3.ID3(path)
    for key, value in id3.items():
        if value.encoding!=3 and isinstance(getattr(value, 'text', [None])[0], unicode):

            if value.encoding==0:
                bytes= '\n'.join(value.text).encode('iso-8859-1')
                for encoding in tryencodings:
                    try:
                        bytes.decode(encoding)
                    except UnicodeError:
                        pass
                    else:
                        break
                else:
                    raise ValueError('None of the tryencodings work for %r key %r' % (path, key))
                for i in range(len(value.text)):
                    value.text[i]= value.text[i].encode('iso-8859-1').decode(encoding)

            value.encoding= 3
    id3.save()

import os
from tokenize import String
import mutagen.id3


def findMP3s(path):
    for child in os.listdir(path):
        child = os.path.join(path, child)
        if os.path.isdir(child):
            for mp3 in findMP3s(child):
                yield mp3
        elif child.lower().endswith(".mp3"):
            yield child


#musicroot = "C:\\Ammar\\Programming\\Projects\\PythonConvertID3ToUTF-8\\TestSongs"
#musicroot = "\\\\SINDEEDFLIX\\Media\\Music\\ConvertorTest"
musicroot = "\\\\SINDEEDFLIX\\Media\\Music"

tryencodings = "cp1256", "gb18030", "cp1252"

fileCounter = 0 #Counter of the files checked.
saveCounter = 0 #Counter of the files converted.
for path in findMP3s(musicroot):
    try:
        id3 = mutagen.id3.ID3(path)
    except mutagen.MutagenError:
        continue
        pass
    fileCounter = fileCounter + 1
    print('#'+ str(fileCounter) + ' - ' + path)
    changed = 0
    for key, value in id3.items():
        print("   Type(value)=" + str(type(value)))
        # if value.encoding!=3 and isinstance(getattr(value, 'text', [None])[0], unicode):
        if isinstance(value,  mutagen.id3.TextFrame):
            if value.encoding == 0: #If the encoding is LATIN1
                #Check if the encoding and decoding possible and without errors:
                for txt in value.text:
                    #bytes = "\n".join(value.text).encode("iso-8859-1")
                    if isinstance(txt, str):
                        bytes = txt.encode("iso-8859-1")
                        for encoding in tryencodings:
                            try:
                                bytes.decode(encoding)
                            except UnicodeError:
                                pass
                            else:
                                break
                        else:
                            raise ValueError(
                                "None of the tryencodings work for %r key %r" % (path, key)
                            )
                #No errors have been found. Lets convert the encoding for each text int value.text:
                for i in range(len(value.text)):
                    oldValue = value.text[i]
                    if isinstance(oldValue, str):
                        newValue = oldValue.encode("iso-8859-1").decode(encoding)
                        print('    Old value=' + oldValue + ', New Value=' + newValue)
                        value.text[i] = newValue # value.text[i].encode("iso-8859-1").decode(encoding)
                        changed = changed + 1
                    else:
                        print('    Subtext "' + str(oldValue) + '" is NOT a string. It is a ' + str(type(oldValue)))

            value.encoding = 3 #UTF-8
    if changed > 0:
        id3.save()
        saveCounter = saveCounter + 1
        print('   Values saved! #' + str(saveCounter))

### https://superuser.com/questions/90449/repair-encoding-of-id3-tags
# The above script makes a few assumptions:
#
#   Only the tags marked as being in encoding 0 are wrong. (Ostensibly encoding 0 is ISO-8859-1, but in practice it is often a Windows default code page.)

#   If a tag is marked as being in UTF-8 or a UTF-16 encoding it's assumed to be correct, and simply converted to UTF-8 if it isn't already. Personally I haven't seen ID3s marked as UTF (encodings 1-3) in error before. Luckily encoding 0 is easy to recover into its original bytes since ISO-8859-1 is a 1-to-1 direct mapping of the ordinal byte values.

# When an encoding 0 tag is met, the script attempts to recast it as GB18030 first, then if it's not valid falls back to code page 1252. Single-byte encodings like cp1252 will tend to match most byte sequences, so it's best to put them at the end of the list of encodings to try.

# If you have other encodings like cp1251 Cyrillic, or a lot of cp1252 filenames with multiple accented characters in a row, that get mistaken for GB18030, you'll need a cleverer guessing algorithm of some sort. Maybe look at the filename to guess what sort of characters are likely to be present?
###
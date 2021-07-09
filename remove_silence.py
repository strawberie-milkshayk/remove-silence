from pydub import AudioSegment
from pydub.silence import split_on_silence

def main():
    input('press enter to select a file . . .')
    try:
        file_in = get_file()
        assert file_in
    except:
        print('no file selected!')
        input('press enter to close the program . . .')
        return
    file_name = file_in.split('/')
    file_dir = file_name[0:len(file_name)-1]
    file_name = file_name[len(file_name) - 1]
    file_type = get_file_type(file_name)
    while True:
        try:
            min_silence_len = int(input('minimum silence length in ms [int > 0]: '))
            assert min_silence_len > 0
            break
        except:
            print('invalid value! please try again')
    while True:
        try:
            silence_thresh = float(input('silence threshold in dB [float < 0]: '))
            assert silence_thresh < 0
            break
        except:
            print('invalid value! please try again')
    needs_conversion = False
    if file_type != 'wav':
        print('file not a .wav file! converting to .wav . . .')
        needs_conversion = True
        try:
            file_in = convert_to_wav(file_in, file_type, file_name)
            file_name = file_in.split('/')
            file_name = file_name[len(file_name) - 1]
            print('conversion success!', file_name, 'has been created')
        except:
            print('conversion failed! quitting program')
    split_files = split_audio(file_in, min_silence_len, silence_thresh)
    temp1 = file_name.split('.')
    temp2 = temp1[0:len(temp1) - 1]
    temp3 = "".join(temp2)
    temp4 = temp3 + '_SILENCE_REMOVED.wav'
    temp5 = temp3 + '_SILENCE_REMOVED.' + str(file_type)
    merged_file = merge_files(split_files, temp4)
    if needs_conversion:
        print('converting '+ temp4 +' to ' + temp5)
        wav_to_infile_type(temp4, 'mp3')
        nf = move_file(temp5, file_dir)
        delete_files([temp4, file_name])
    else:
        nf = move_file(temp4, file_dir)
    delete_files(split_files)
    print('done! check for the file in:', nf)
    input('press any key to exit . . .')
    

def get_file_type(file_name):
    file = file_name.split('.')
    if len(file) <= 1:
        return False
    else:
        return file[len(file)-1]


def convert_to_wav(file_path_in, file_type, file_name):
    supported_types = ['mp3', 'm4a']
    supported_file = False
    print(file_name)
    new_file_name = file_name.replace('.' + file_type, '.wav')
    for each_type in supported_types:
        if file_type == each_type:
            supported_file = True
    if not supported_file:
        return False
    if file_type.lower() == 'mp3':
        sound = AudioSegment.from_mp3(file_path_in)
        sound.export(new_file_name, format="wav")
        return new_file_name
    elif file_type.lower() == 'm4a':
        sound = AudioSegment.from_file(file_path_in, 'm4a')
        sound.export(wav_path, format='wav')
        return new_file_name
    else:
        print('unknown conversion error!')
        return False
    




def split_audio(file_name, min_silence_len, silence_thresh):
    chunks = []
    sound_file = AudioSegment.from_wav(file_name)
    print('creating chunks. this may take a while . . .')
    audio_chunks = split_on_silence(sound_file, min_silence_len, silence_thresh)
    chunk_ct = len(audio_chunks)
    print('chunks created! exporting chunks . . .')
    for i, chunk in enumerate(audio_chunks):
        out_file = "temp_chunk{0}.wav".format(i)
        chunks.append(out_file)
        chunk.export(out_file, format="wav")
    print('all chunks have been exported!')
    return chunks


def merge_files(chunks, out_file_name):
    first = True
    print('merging files . . .')
    for chunk in chunks:
        if first:
            combined = AudioSegment.from_wav(chunk)
            first = False
        else:
            combined += AudioSegment.from_wav(chunk)
    print('exporting merged file . . .')
    combined.export(out_file_name, format="wav")


def wav_to_infile_type(file_name, file_type):
    supported_types = ['mp3', 'm4a']
    new_file_name = file_name.replace('.wav', '.' + file_type)
    if file_type.lower() == 'mp3':
        sound = AudioSegment.from_wav(file_name)
        sound.export(new_file_name, format="mp3")
        return new_file_name
    elif file_type.lower() == 'm4a':
        print('m4a export not available. this file will be exported as', file_name.replace('.wav', '.mp3'))
        sound = AudioSegment.from_wav(file_name)
        sound.export(new_file_name, format="mp3")
        return new_file_name
    else:
        return False


def get_file():
    from tkinter import Tk     # from tkinter import Tk for Python 3.x
    from tkinter.filedialog import askopenfilename

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filename)
    return filename

def move_file(cf, nd):
    import os
    try:
        nf = '/'.join(nd) + '/' + cf
        in_file = open(cf, 'rb')
        data = in_file.read()
        in_file.close()
        out_file = open(nf, 'wb')
        out_file.write(data)
        out_file.close()
        os.remove(cf)
        return nf
    except:
        print('UNABLE TO MOVE FILE!')
        return False

def delete_files(list1):
    import os
    failed = []
    for file in list1:
        try:
            os.remove(file)
        except:
            failed.append(file)
    return failed

if __name__ == '__main__':
    main()

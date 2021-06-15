import time
import os
import shutil
from hashlib import sha256
from config import home_dir


def pbar(piece:str, number:int, text:str=None, before=None, after=None)->str:
    bartext = piece * number
    if before:
        print(before)
    if text:
        text = f' {text.strip()} '
        width = len(text)
        startpos = int((len(bartext) - width) / 2)
        endpos = startpos + width
        print(bartext[:startpos] + text + bartext[endpos:])
    else:
        print(bartext)
    if after:
        print(after)


class Duplython:
    def __init__(self):
        self.home_dir = home_dir
        self.file_hashes = []
        self.cleaned_dirs = []
        self.total_bytes_saved = 0
        self.block_size = 65536
        self.count_cleaned = 0

    def welcome(self)->'Duplython':
        pbar('*', 80)
        pbar('*', 80, text='Duplython')
        pbar('*', 80, after='\n\n')
        return self

    def generate_hash(self, filename:str)->str:
        filehash = sha256()
        try:
            with open(filename, 'rb') as file:
                fileblock = file.read(self.block_size)
                while len(fileblock)>0:
                    filehash.update(fileblock)
                    fileblock = file.read(self.block_size)
                filehash = filehash.hexdigest()
            return filehash
        except:
            return False

    def clean(self)->'Duplython':
        all_dirs = [path[0] for path in os.walk(self.home_dir)]
        for path in all_dirs:
            os.chdir(path)
            all_files =[file for file in os.listdir() if os.path.isfile(file)]
            for file in all_files:
                filehash = self.generate_hash(file)
                if not filehash in self.file_hashes:
                    if filehash:
                        self.file_hashes.append(filehash)
                        #print(file)
                else:
                    byte_saved = os.path.getsize(file)
                    self.count_cleaned+=1
                    self.total_bytes_saved+=byte_saved
                    os.remove(file)
                    filename = file.split('/')[-1]
                    print(filename, '.. cleaned ')
            os.chdir(self.home_dir)
        return self

    def cleaning_summary(self)->None:
        mb_saved = self.total_bytes_saved/1048576
        mb_saved = round(mb_saved, 2)
        pbar('-', 80, text='FINISHED CLEANING', before='\n\n')
        print('File cleaned  : ', self.count_cleaned)
        print('Total Space saved : ', mb_saved, 'MB')
        pbar('-', 80)

    def main(self)->None:
        self.welcome().clean().cleaning_summary()


if __name__ == '__main__':
    app = Duplython()
    app.main()

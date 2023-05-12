from bs4 import BeautifulSoup
import os
import re
                
class HTMLparser: 
    def __init__(self,
                 input_path: str = './input/',
                 output_filepath: str = './output/comments_ru.txt',
                 ) -> None:
        self.input_path = input_path
        self.output_filepath = output_filepath
        self.list_comments = list()
    
    def parse_input_dir(self) -> list:
        for path in os.listdir(self.input_path):
            if '.html' in path:
                with open(file=f'{self.input_path}{path}', encoding='utf-8', mode='r') as f:
                    html = '\n'.join(f.readlines())
                    soup = BeautifulSoup(str(html), 'html.parser')
                    try:
                        for i in range(2,100):
                            comments = str(soup).split('Комментарий')[i].split(' ')[0].split('</div> <div><span class=')[1].split('>')[1].replace('\n','').replace('...','').replace('..','')
                            result = re.sub('[^\x00-\x7Fа-яА-Я]', '', comments)
                            self.list_comments.append(result)
                    except Exception:
                        pass
        return self.list_comments
    
    def write_comments_to_file(self) -> None:
        with open(self.output_filepath,'w',encoding='utf-8') as f_ru:
            for comment in self.list_comments:
                f_ru.write(str(comment) + '\n')
import re
from googletrans import Translator
from google_trans_new import google_translator  

class CommentsTranslater:
    def __init__(self,
                 comments: list = None,
                 input_filepath: str = './output/comments_ru.txt',
                 output_filepath: str = './output/comments_en.txt',
                 input_lang: str = 'ru',
                 output_lang: str = 'en'
                 ) -> None:
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        self.list_comments = comments if comments else self.__load_comments()
        self.input_lang = input_lang
        self.output_lang = output_lang
    
    def __load_comments(self) -> list:
        list_comments = list()
        f_ru = open(self.input_filepath,'r',encoding='utf-8')
        reader_ru = f_ru.read().split('\n')
        for i in range(len(reader_ru)):
            if reader_ru[i] != "":
                list_comments.append(reader_ru[i])
        f_ru.close()
        return list_comments
    
    def translate(self) -> list:
        self.list_translated_comments = list()
        translator = Translator(service_urls=[
            'translate.google.com'
        ])

        for i in range(len(self.list_comments)):

            try:
                result = re.sub('[^\x00-\x7Fа-яА-Я]', '', self.list_comments[i])
                translate_result = translator.translate(text=result,src=self.input_lang,dest=self.output_lang)
                
                self.list_translated_comments.append(translate_result.text)
                # print('translate result',translate_result)

            except Exception as e:
                print('Ошибка перевода, комментарий #' + str(i) ,str(e))
                pass

            
        
        return self.list_translated_comments

    def write_to_file(self) -> None:
        f_en = open(self.output_filepath,"w",encoding="utf-8")
        for k in range(len(self.list_translated_comments)):
            f_en.write(str(self.list_translated_comments[k]) + "\n")
        print("Комментариев переведено:",len(self.list_translated_comments))
        f_en.close()
from textblob import TextBlob
from statistics import mean
from collections import Counter
import math
import matplotlib.pyplot as plt

class CommentAnalyzer():
    def __init__(self,
                 comments_en: list = None,
                 comments_ru: list = None,
                 input_ru_filepath: str = './output/comments_ru.txt',
                 input_en_filepath: str = './output/comments_en.txt',
                 output_polarity_filepath: str = './output/polarity.txt',
                 output_subjectivity_filepath: str = './output/subjectivity.txt'
                 ) -> None:
        self.input_ru_filepath = input_ru_filepath
        self.input_en_filepath = input_en_filepath
        self.output_polarity_filepath = output_polarity_filepath
        self.output_subjectivity_filepath = output_subjectivity_filepath
        self.comments_ru = comments_ru if comments_ru else self.__load_comments(self.input_ru_filepath)
        self.comments_en = comments_en if comments_en else self.__load_comments(self.input_en_filepath)

        self.polarity = list()
        self.subjectivity = list()
    
    def __load_comments(self,filepath:str) -> list:
        list_comments = list()
        f = open(filepath,'r',encoding='utf-8')
        reader = f.read().split('\n')
        for i in range(len(reader)):
            if reader[i] != '':
                list_comments.append(reader[i])
        f.close()
        return list_comments

    def get_polarity(self) -> list:
        for i in range(len(self.comments_en)):
            polarity = TextBlob(self.comments_en[i]).polarity
            if polarity != 0.0:
                self.polarity.append(polarity)
        return self.polarity
    
    def get_subjectivity(self) -> list:
        for i in range(len(self.comments_en)):
            subjectivity = TextBlob(self.comments_en[i]).subjectivity
            if subjectivity != 0.0:
                self.subjectivity.append(subjectivity)
        return self.subjectivity
    
    def write_file(self) -> None:
        polarity_file = open(self.output_polarity_filepath,'w')
        polarity_file.write(str(self.polarity))
        polarity_file.close()

        subjectivity_file = open(self.output_subjectivity_filepath,'w')
        subjectivity_file.write(str(self.subjectivity))
        subjectivity_file.close()
    
    def printStats(self) -> None:
        print('Комментариев обработано:',len(self.comments_en))
        print('Положительность комментариев:',mean(self.polarity))
        print('Насыщенность комментариев:',mean(self.subjectivity))


    def collectWords(self,comments) -> Counter:
        words_list = list()
        for comment in comments:
            collector = TextBlob(comment).words
            for coll in collector:
                words_list.append(coll)
        counter = Counter(words_list)
        return counter
    
    def mandelbrot(self,counter) -> dict:
        counter_sorted = dict(sorted(counter.items(), key=lambda x: x[1]))
        result_list = list()
        list_result_diagram = list()
        list_words_diagram = list()
        
        for key, value in counter_sorted.items():

            b = math.fabs(math.log(len(key),(1*0.1)/value))
            result_list.append(b)
            if b >= 0.5:
                list_result_diagram.append(b)
                list_words_diagram.append(key.lower())

        result = sum(result_list) / len(result_list)
        print(f"Естественность Языка: {result} из 1")
        return {
            'naturalness': result,
            'diagram': {
                'results': list_result_diagram[:10],
                'words': list_words_diagram[:10]
            }
        }
        
    
    def first_Zipf_law(self,counter) -> None:
        dict_1 = dict()
        list_1 = list()
        counter_sorted = dict(sorted(counter.items(), key=lambda x: x[1]))

        for key in counter_sorted.keys():
            dict_1[key] = len(key)
            list_1.append(len(key))

        sorted_tuples = sorted(dict_1.items(), key=lambda item: item[1])
        sorted_dict = {k: v for k, v in sorted_tuples}

        sorted_list_keys = list(sorted_dict.keys())
        sorted_list_value = list(sorted_dict.values())
        list_values = list()

        for key in sorted_list_keys:
            list_values.append(counter_sorted[key])

        return {
            'sorted-values': sorted_list_value,
            'list-values': list_values
        }

    def second_Zipf_law(self,counter) -> None:
        counter_len = list()
        for j in range(len(counter)):
            counter_len.append(j)

        return counter_len[::-1]
    
    def plot(self) -> None:

        counter_en = self.collectWords(self.comments_en)
        counter_ru = self.collectWords(self.comments_ru)


        

        # Первый закон Ципфа
        first_Zipf_law_result = self.first_Zipf_law(counter_ru)
        plt.title("Первый закон Ципфа")
        plt.xlabel("Значение слова")
        plt.ylabel("Частота")
        plt.plot(first_Zipf_law_result['sorted-values'],first_Zipf_law_result['list-values'])
        plt.show()

        # Второй закон Ципфа
        counter_ru_list = list(counter_ru.values())
        counter_en_list = list(counter_en.values())

        counter_ru_list.sort()
        counter_en_list.sort()

        second_Zipf_law_ru = self.second_Zipf_law(counter_ru)
        second_Zipf_law_en = self.second_Zipf_law(counter_en)
        plt.title("Второй закон ципфа")
        plt.xlabel("Частота")
        plt.ylabel("Количество слов")
        plt.plot(second_Zipf_law_ru,counter_ru_list,label=f"Русский язык")
        plt.plot(second_Zipf_law_en,counter_en_list,label=f"Английский язык")
        plt.legend()
        plt.show()

        mandelbrot_ru = self.mandelbrot(counter_ru)

        # Круговая диаграмма
        fig = plt.figure(figsize=(6,4))
        ax = fig.add_subplot()
        ax.pie(mandelbrot_ru['diagram']['results'], labels = mandelbrot_ru['diagram']['words'], autopct='%.2f%%',pctdistance = 0.7,radius=1.3)
        ax.grid()
        plt.show()
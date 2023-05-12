from HTMLparser import HTMLparser
from CommentsTranslater import CommentsTranslater
from CommentAnalyzer import CommentAnalyzer

if __name__ == '__main__':

    # Получение комментариев
    parser = HTMLparser()
    comments = parser.parse_input_dir()
    parser.write_comments_to_file()
    
    # Перевод на англ. язык
    translator = CommentsTranslater(comments)
    translated_comments = translator.translate()
    translator.write_to_file()

    # Анализ комментариев
    analyzer = CommentAnalyzer(translated_comments,comments)
    polarity = analyzer.get_polarity()
    subjectivity = analyzer.get_subjectivity()
    analyzer.write_file()
    analyzer.printStats()
    analyzer.plot()

    
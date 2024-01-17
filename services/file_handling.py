import os
import sys

BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}

# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    punctuation_endings = {'...', ',', '.', '!', ':', ';', '?'}

    end = min(start + page_size, len(text))

    # Находим индекс последнего знака препинания в диапазоне [start:end]
    last_punctuation_index = max(
        (i for i in range(end -1, start - 1, -1) if text[i] in punctuation_endings),
        default=end
    )

    # Если последний знак препинания находится в пределах максимального размера страницы
    if last_punctuation_index < start + page_size:
        page_text = text[start:last_punctuation_index + 1].lstrip()
        page_size = len(page_text)
    else:
        # Если последний знак препинания выходит за пределы максимального размера страницы
        next_char = text[last_punctuation_index + 1]
        if next_char.isspace():
            page_text = text[start:last_punctuation_index + 2].lstrip()
            page_size = len(page_text)
        else:
            # Убираем последний знак препинания, чтобы не превышать максимальный размер страницы
            page_text = text[start:last_punctuation_index].rstrip()
            page_size = len(page_text)

    return page_text, page_size


text = '— Я всё очень тщательно проверил, — сказал компьютер, — и со всей определённостью заявляю, что это и есть ответ. Мне кажется, если уж быть с вами абсолютно честным, то всё дело в том, что вы сами не знали, в чём вопрос.'
print(*_get_part_text(text, 54, 70), sep='\n')

# Функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    with open(file=path, mode='r', encoding='utf-8') as file:
        text = file.read()
    start, page_number = 0, 1
    while start < len(text):
        page_text, page_size = _get_part_text(text, start, PAGE_SIZE)
        start += page_size
        book[page_number] = page_text.strip()
        page_number += 1

# Чтобы путь был понятен всем операционным системам
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))



import string

def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    punctuation_endings = {',', '.', '!', ':', ';', '?'}

    end = min(start + page_size, len(text))

    # Находим индекс последнего знака препинания в диапазоне [start:end]
    last_punctuation_index = max(
        (i for i in range(end, start - 1, -1) if text[i] in punctuation_endings),
        default=end
    )

    # Обработка многоточия и других сочетаний символов
    multi_punctuation = ['...', '?!', '?!..', '?..', '!..', '!!', '!!..', '!.', '!..', '..']
    for mp in multi_punctuation:
        if text[last_punctuation_index - len(mp) + 1:last_punctuation_index + 1] == mp:
            last_punctuation_index -= len(mp) - 1
            break

    # Формирование текста страницы
    if last_punctuation_index < start + page_size:
        page_text = text[start:last_punctuation_index + 1].lstrip()
        page_size = len(page_text)
    else:
        next_char = text[last_punctuation_index + 1]
        if next_char.isspace():
            page_text = text[start:last_punctuation_index + 2].lstrip()
            page_size = len(page_text)
        else:
            page_text = text[start:last_punctuation_index].rstrip()
            page_size = len(page_text)

    return page_text, page_size

# Пример использования
text = '— Я всё очень тщательно проверил, — сказал компьютер, — и со всей определённостью заявляю, что это и есть ответ. Мне кажется, если уж быть с вами абсолютно честным, то всё дело в том, что вы сами не знали, в чём вопрос...!'
print(*_get_part_text(text, 54, 70), sep='\n')

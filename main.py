from __future__ import print_function, unicode_literals, absolute_import
from pyreadline.rlmain import Readline

import sys
import requests
import jellyfish
import string
import codecs
import subprocess
import json
import random
import datetime
import re
import pyreadline
import colorama
import platform
import time as t
import xml.etree.ElementTree as ET
from alive_progress import alive_bar
from colorama import Fore
from statistics import mode
from datetime import date
from collections import Counter
from bs4 import BeautifulSoup
from textwrap import wrap
from art import *

known_file_path = 'known.txt'
learning_file_path = 'learning.txt'
mp3_file_path = 'mp3.txt'
examples_file_path = 'examples.txt'
for_anki_file_path = 'forAnki.txt'
checked_file_path = 'checked.txt'
text_file_path = 'text.txt'
today_date_file_path = 'today.txt'
today_count_file_path = 'count.txt'
transcription_file_path = 'transcription.txt'
words_from_text_file_path = 'words_from_text.txt'
count_file_path = 'count.txt'
token_file_path = 'token.txt'
token_starts_file_path = 'token_start.txt'
eng_with_eng_file_path = 'eng_with_eng.txt'
rus_with_engfile_path = 'rus_with_eng.txt'
eng_with_rus_file_path = 'eng_with_rus.txt'
mixed_letters_file_path = 'mixed_letters.txt'
queue_file_path = 'queue.txt'
pc_token_file_path = 'pc_token.txt'

word, main_definition, second_word, examp_word, example = "", "", "", "", ""
transcription, next_word, example_translation, old_word = "", "", "", ""
new_examp_word, new_main_definition, new_rus_ex, today_date, today_count = "", "", "", "", ""
added_list, definitions, equality_list = [], [], []
ch_dict = {}
random_mode = False

repeat = 0
jelly_index = 0.75
platform_type = str(platform.machine())
IAM_TOKEN = ""


def token():
    """Подтягивает токен яндекса с текстового файла."""
    global IAM_TOKEN
    if platform_type == "AMD64":
        with open(pc_token_file_path, 'r', encoding="utf-8") as file:
            line = file.read()
            if line == "":
                line = '{\n"iamToken": "t1"\n}'
            with open(pc_token_file_path, 'w', encoding='utf-8') as file:
                file.write(line + '\n')
        IAM_TOKEN = json.loads(line)["iamToken"]
    elif platform_type == "aarch64":
        with open(token_file_path, 'r', encoding="utf-8") as file:
            line = file.read()
        IAM_TOKEN = line


def file_to_list(file_path, l, is_low):
    """Передает данные файла в список."""
    file = codecs.open(file_path, 'r', "utf-8")
    while True:
        line = file.readline()
        if not line:
            break
        if is_low:
            l.append(line.lower().strip("\n"))
        else:
            l.append(line.strip("\n"))
    file.close()


for_anki_list = []
file_to_list(for_anki_file_path, for_anki_list, False)
for_anki_list = [line.rstrip() for line in for_anki_list]
learning_list = []
file_to_list(learning_file_path, learning_list, True)
learning_list = [line.rstrip() for line in learning_list]
mp3_list = []
file_to_list(mp3_file_path, mp3_list, False)
mp3_list = [line.rstrip() for line in mp3_list]
known_list = []
file_to_list(known_file_path, known_list, True)
known_list = [line.rstrip() for line in known_list]
ex_list = []
file_to_list(examples_file_path, ex_list, False)
checked_list = []
file_to_list(checked_file_path, checked_list, True)
checked_list = [line.rstrip() for line in checked_list]
queue_list = []
file_to_list(queue_file_path, queue_list, True)
queue_list = [line.rstrip() for line in queue_list]


def checking():
    """Сверяет новые слова со списком известных и изучаемых слов (учитывая разные словоформы) и удаляет повторы.
Также удаляет все имена и названия."""
    ex_list = []
    file_to_list(examples_file_path, ex_list, False)
    ex_list = [line.rstrip() for line in ex_list]
    new_list = []
    file_to_list(words_from_text_file_path, new_list, False)
    new_list = [line.rstrip() for line in new_list]
    trash_cap_list = []  # сюда пойдут слова с заглавными буквами, чтобы убрать их из new_list до начала проверки
    print("\nУдаляются имена и названия...")
    with alive_bar(len(ex_list)) as bar:
        for e in ex_list:
            bar()
            for n in new_list:
                e2 = e.strip(string.punctuation)
                list1 = e2.split()
                if n.istitle() == True and n in e2 and n != list1[0]:
                    trash_cap_list.append(n)
    new_list = list(set(new_list) - set(trash_cap_list))
    for n in new_list:
        new_list[new_list.index(n)] = n.lower()
    print("\nПроизводится проверка слов...")

    def check(list1, list2, not_first_checking):
        """Непосредственно выполняет сравнение слов внутри функции checking()."""
        result_list = []
        with alive_bar(len(list1)) as bar:
            for i in list1:
                bar()
                for j in list2:
                    if not_first_checking and i == j:
                        result_list.append(i)
                    if i == j + 'ed':
                        result_list.append(i)
                    if i == j + 's':
                        result_list.append(i)
                    if i == j + 'ing':
                        result_list.append(i)
                    if i == j + 'd':
                        result_list.append(i)
                    if i == j + 'es':
                        result_list.append(i)
                    if i == j + '\'s':
                        result_list.append(i)
                    if i == j[:-1] + 'ing':
                        result_list.append(i)
                    if i == j[:-1] + 'ied':
                        result_list.append(i)
                    if i == j[:-1] + 'ies':
                        result_list.append(i)
                    if i == j + 'ting':
                        result_list.append(i)
                    if i == j + 'ping':
                        result_list.append(i)
                    if i == j + 'sing':
                        result_list.append(i)
                    if i == j + 'ning':
                        result_list.append(i)
                    if i == j + 'ding':
                        result_list.append(i)
                    if i == j + 'ging':
                        result_list.append(i)
                    if i == j + 'ped':
                        result_list.append(i)
                    if i == j + 'ged':
                        result_list.append(i)
                    if i == j + "g":
                        result_list.append(i)
                    if i == j + "est":
                        result_list.append(i)
                    if i == "in" + j:
                        result_list.append(i)
                    if i == "im" + j:
                        result_list.append(i)
                    if i == "un" + j:
                        result_list.append(i)
                    if i == "non-" + j:
                        result_list.append(i)
        return result_list

    known_list = []
    file_to_list(known_file_path, known_list, True)
    known_list = [line.rstrip() for line in known_list]
    learning_list = []
    file_to_list(learning_file_path, learning_list, True)
    learning_list = [line.rstrip() for line in learning_list]
    print("\nШаг 1 из 3...")
    matchnew_list = check(new_list, new_list, False)

    new_list = list(set(new_list) - set(matchnew_list))
    print("\nШаг 2 из 3...")
    match_known_list = check(new_list, known_list, True)
    print("\nШаг 3 из 3...")
    match_learning_list = check(new_list, learning_list, True)

    res_list = list(set(new_list) - set(match_known_list + match_learning_list))

    with open(checked_file_path, 'w', encoding='utf-8') as file:
        for line in res_list:
            if not "'s" in line:
                file.write(line + '\n')

    print("\nСлова проверены. Нет совпадений у", len(res_list), "слов(-а) из", len(new_list))
    print("\nОтобразить список? (y/n)\n")
    response = str(input(Fore.GREEN))
    print(Fore.RESET)
    if response == 'y':
        print(*res_list, sep="\n", end="\n\n")
    print("""\nЗакончить программу - 0.
    Перейти к добавлению - 1.""")
    answer = input(Fore.GREEN)
    print(Fore.RESET)
    if answer == "1":
        print()
        return None
    elif answer == "0":
        sys.exit()


def split_text():
    """Делит исходный текст на слова, разбив его построчно. Формирует список примеров. Удаляет мусорные слова."""
    print(Fore.RESET)
    print("""Текст уже разделен построчно - Enter.
Текст требуется разделить построчно - 0.""")
    response = str(input(Fore.GREEN))
    print(Fore.RESET)
    if response == '0':
        with open(text_file_path, "r", encoding="utf-8") as file:
            a = file.read()
            s = a.replace('\n', '')
        sub_string = re.sub(r'[!?\.]+ *', lambda m: f"{m.group()}\n", s)
        with open(text_file_path, 'w', encoding="utf-8") as file:
            file.write(sub_string)
    text_file = open(text_file_path, 'r', encoding="utf-8")
    ex_list = []
    w_list = []
    while True:
        line = text_file.readline()
        if not line:
            break
        new_line = line.replace(line[0], line[0].capitalize(), 1)
        ex_list.append(new_line)  # делаем список с примерами
        line2 = line.strip(string.punctuation)
        w_list.append(line2.split())  # делаем список со списками из слов
    text_file.close()
    with open(examples_file_path, 'w', encoding='utf-8') as file:
        for line in ex_list:
            file.write(line)
    word_list = []
    for i in w_list:
        word_list.extend(i)  # превращаем всё в один список
    # удаляем знаки препинания:
    word_list2 = []
    d_list = ["...", "♪", "/", "\\", ":", "…", "}", "+", "(", ")", "≥", "<", ">", "‘", "]", "[", "$",
              "’", "{", "=", "_", "@", "'", "”", "»", "«", "0", "1",
              "2", "3", "4", "5", "6", "7", "8", "9"]
    for i in word_list:
        sss = i.strip(string.punctuation).strip("”").strip("“").strip("’").strip("-")
        for j in d_list:
            sss = sss.strip(j)
        word_list2.append(sss)
    # убираем дубликаты:
    dicti = tuple(word_list2)
    word_list3 = list(dict.fromkeys(dicti))
    word_list4 = []
    for c in word_list3:
        if len(c) > 2 and not any((i in c) for i in d_list):
            if not Counter(c).get("-", 0) > 1:
                word_list4.append(c)
    with open(words_from_text_file_path, 'w', encoding='utf-8') as file:
        for line in word_list4:
            file.write(line + '\n')
    print("Текст успешно разделен на слова. Получилось ", len(word_list4), " слов(-а).")
    print("Также добавлено", len(ex_list), "предложений(-я) в качестве примеров.")
    print("""\nЗакончить программу - 0.
Перейти к проверке - 1.""")
    answer = input(Fore.GREEN)
    print(Fore.RESET)
    if answer == "1":
        checking()
    elif answer == "0":
        sys.exit()


def rando():
    """Позволяет вводить любое случайное слово не из списка."""
    global word, example, second_word, random_mode
    print(Fore.RESET)
    print("\nВведите слово:\n")
    word = input(Fore.GREEN)
    print("\n", Fore.RESET, Fore.CYAN, get_yandex_definition(word))
    print("\n", get_multitran_definition(word))
    print(Fore.RESET, "\nВведите пример (1) или найдите примеры (2)\n")
    answer = input(Fore.GREEN)
    print(Fore.RESET)

    if answer == "1":
        example = input(Fore.GREEN)
        print(Fore.RESET, "\nВведите second word, если необходимо:\n")
        reply = input(Fore.GREEN)
        if reply != "":
            print(Fore.RESET, "\nВторое слово -", Fore.CYAN, reply, Fore.RESET, " Верно? (y/n)\n")
            answer = input(Fore.GREEN)
            if answer == "y":
                second_word = reply
                print(Fore.RESET)
            if answer == "n":
                print(Fore.RESET)
        else:
            second_word = word
            print(Fore.RESET)
        added_today()
        first_menu()
    elif answer == "2":
        search_for_ex()
        check_yandex_token()
        added_today()
        first_menu()


def search_for_ex():
    """Ищет примеры на context.reverso.net для введенных случайных слов."""
    global example, word, second_word
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.31'
    }
    url = "https://context.reverso.net/перевод/английский-русский/"
    r = requests.get(url + word, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    ex_dict = {}
    count = 0
    for ex in soup.findAll('span', lang="en"):
        count += 1
        ex_dict[count] = ex.text.strip()
    for key, value in ex_dict.items():
        print(Fore.CYAN, key, ':', value)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.31'
    }
    url = "https://context.reverso.net/перевод/английский-русский/"
    r = requests.get(url + word, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    ru_def = []
    count = 0
    for a in soup.findAll('a', rel='nofollow'):
        count += 1
        ru_def.append(str(count) + ": " + a.text.strip())
    print("\n", ru_def)

    while True:
        print("\nВыберите один пример.\n", Fore.GREEN)
        ex_key = int(input())
        print(Fore.RESET, "\nВыбран пример:\n\n " + Fore.CYAN, str(ex_key) + ": " + str(ex_dict[ex_key]), Fore.RESET)
        print("\nПодтверждаете? (y/n)\n")
        answer = input(Fore.GREEN)
        if answer == "y":
            example = str(ex_dict[ex_key])
            print(Fore.RESET, "\nВведите second word, если необходимо:\n")
            reply = input(Fore.GREEN)
            if reply != "":
                print(Fore.RESET, "\nВторое слово - ", Fore.CYAN, reply, Fore.RESET, " Верно? (y/n)\n")
                answer = input(Fore.GREEN)
                if answer == "y":
                    second_word = reply
                    print(Fore.RESET)
                    break
                if answer == "n":
                    print(Fore.RESET)
                    continue
            else:
                second_word = word
                print(Fore.RESET)
                break
        elif answer == "n":
            print(Fore.RESET)
            continue


def file_write(file_path, l):
    """Записывает список в файл."""
    with codecs.open(file_path, 'w', 'utf-8') as file:
        for line in l:
            if not "\n" in line:
                file.write(line + '\n')
            elif "\n" in line:
                file.write(line)


def fuck_excel(string_1):
    """Формирует записи для импорта в Anki."""

    def anki_master(string_1):
        """Обрабатывает строки и расставляет нужные html теги внутри функции fuck_excel()."""

        list_1 = string_1.strip("\n").split("*")
        en_word_1 = list_1[0]
        en_word_2 = list_1[1]
        transcription = list_1[2]
        rus_word1 = list_1[3]
        rus_word2 = list_1[4]
        en_sen = list_1[5]
        ru_sen = list_1[6]
        en_sen_list = en_sen.split()
        ru_sen_list = ru_sen.split()

        count = 0
        if ' ' in rus_word2:
            count = 1
        else:
            for word in ru_sen_list:
                if word.strip(string.punctuation).lower() == rus_word2:
                    count += 1
        if en_word_2.title() == en_sen_list[0].strip(string.punctuation):
            if en_word_1 != en_word_2:
                edited_rus_word = "<u>" + en_word_2.title() + "</u>" + " <sup><b>(" + en_word_1 + ")</b></sup>"
            else:
                edited_rus_word = "<b>" + en_word_2.title() + "</b>"
            rus_with_eng = (ru_sen.replace(rus_word2.title(), edited_rus_word, count)).strip("\n")
        if en_word_2.title() != en_sen_list[0].strip(string.punctuation):
            if en_word_1 != en_word_2:
                edited_rus_word = "<u>" + en_word_2 + "</u>" + " <sup><b>(" + en_word_1 + ")</b></sup>"
            else:
                edited_rus_word = "<b>" + en_word_2 + "</b>"
            rus_with_eng = (ru_sen.replace(rus_word2, edited_rus_word, count)).strip("\n")

        count = 0
        for word in en_sen_list:
            if word.strip(string.punctuation).lower() == en_word_2:
                count += 1
        if en_word_2.title() == en_sen_list[0].strip(string.punctuation):
            if en_word_1 != en_word_2:
                edited_en_word = "<u>" + en_word_2.title() + "</u>" + " <sup><b>(" + en_word_1 + ")</b></sup>"
            else:
                edited_en_word = "<b>" + en_word_2.title() + "</b>"
            eng_with_eng = en_sen.replace(en_word_2.title(), edited_en_word, count)
        if en_word_2.title() != en_sen_list[0].strip(string.punctuation):
            if en_word_1 != en_word_2:
                edited_en_word = "<u>" + en_word_2 + "</u>" + " <sup><b>(" + en_word_1 + ")</b></sup>"
            else:
                edited_en_word = "<b>" + en_word_2 + "</b>"
            eng_with_eng = en_sen.replace(en_word_2, edited_en_word, count)

        count = 0
        for word in en_sen_list:
            if word.strip(string.punctuation).lower() == en_word_2:
                count += 1
        if en_word_2.title() == en_sen_list[0].strip(string.punctuation):
            if rus_word1 != rus_word2:
                edited_en_word = "<u>" + rus_word2.title() + "</u>" + " <sup><b>(" + rus_word1 + ")</b></sup>"
            else:
                edited_en_word = "<b>" + rus_word2.title() + "</b>"
            eng_with_rus = en_sen.replace(en_word_2.title(), edited_en_word, count)
        elif en_word_2.title() != en_sen_list[0].strip(string.punctuation):
            if rus_word1 != rus_word2:
                edited_en_word = "<u>" + rus_word2 + "</u>" + " <sup><b>(" + rus_word1 + ")</b></sup>"
            else:
                edited_en_word = "<b>" + rus_word2 + "</b>"
            eng_with_rus = en_sen.replace(en_word_2, edited_en_word, count)

        result1 = eng_with_eng + "*" + transcription + " " + "&nbsp;&nbsp;♫[sound:" + "en_" + en_word_1 + ".mp3" + "]&nbsp;♫" + "*" + rus_word1
        result2 = rus_with_eng + "*" + transcription + " " + "&nbsp;&nbsp;♫[sound:" + "en_" + en_word_1 + ".mp3" + "]&nbsp;♫" + "*" + rus_word1
        result3 = eng_with_rus + "*" + en_word_1
        sound_before = "&nbsp;&nbsp;♫[sound:en_"
        sound_after = ".mp3]&nbsp;♫"
        before_letter = '<div <="" div="" style="border: 1px solid grey; display: inline; padding: 5px">'
        after_letter = '</div>'
        br_br = '<br><br>'
        anki_copyright = '<div><br><div><i><sub><font color="#dadada">vk.com/ankiplace</font></sub></i><br></div></div>'
        l = list(en_word_1)
        random.shuffle(l)
        mixed_word = ''.join(l)
        mixed_list = list(mixed_word)
        count = -1
        new_list = []
        for letter in mixed_list:
            count += 1
            new_list.append(before_letter + mixed_word[count] + after_letter)
        char_block = ''.join(new_list)
        result4 = rus_word1 + br_br + char_block + br_br + "*" + en_word_1 + "*" + transcription + " " + sound_before + en_word_1 + sound_after + anki_copyright
        return [result1, result2, result3, result4]

    eng_with_eng_list = []
    rus_with_eng_list = []
    _list = []
    mixed_letters = []
    file_to_list(eng_with_eng_file_path, eng_with_eng_list, False)
    file_to_list(rus_with_engfile_path, rus_with_eng_list, False)
    file_to_list(eng_with_rus_file_path, _list, False)
    file_to_list(mixed_letters_file_path, mixed_letters, False)
    result = anki_master(string_1)
    eng_with_eng_list.append(result[0].strip("\n"))
    rus_with_eng_list.append(result[1].strip("\n"))
    _list.append(result[2].strip("\n"))
    mixed_letters.append(result[3].strip("\n"))
    file_write(eng_with_eng_file_path, eng_with_eng_list)
    file_write(rus_with_engfile_path, rus_with_eng_list)
    file_write(eng_with_rus_file_path, _list)
    file_write(mixed_letters_file_path, mixed_letters)
    print("\nЗаписи успешно сформированы.")
    print("\nЗапись eng with eng:\n", Fore.CYAN)
    print(result[0].strip("\n"), Fore.RESET)
    print("\nЗапись rus with eng:\n", Fore.CYAN)
    print(result[1].strip("\n"), Fore.RESET)
    print("\nЗапись eng with rus:\n", Fore.CYAN)
    print(result[2].strip("\n"), Fore.RESET)


def how_many():
    """Показывает количественную справку по словам."""
    with open(known_file_path) as file1:
        count1 = sum(1 for line in file1 if line.rstrip('\n'))
    with open(learning_file_path) as file2:
        count2 = sum(1 for line in file2 if line.rstrip('\n'))
    print()
    print("Добавлено сегодня:", today_count)
    print('Известных слов всего:', count1)
    print('Изучаемых слов всего:', count2)
    print("Готовых для экспорта слов:", len(for_anki_list))


def get_transcription(wordy):
    """Парсит транскрипцию с Wordhunt."""
    url = 'https://wooordhunt.ru/word/'
    try:
        r = requests.get(url + wordy)
        soup = BeautifulSoup(r.text, 'lxml')
        transcription = soup.find(class_='transcription').text
    except AttributeError:
        return " [null]"
    return transcription


def get_yandex_definition(aword):
    """Получает русские значения с yandex.dictionary через API."""
    url = 'https://dictionary.yandex.net/api/v1/dicservice/lookup?key=ВАШ API-КЛЮЧ&lang=en-ru&text='
    r = requests.get(url + aword)
    root = ET.fromstring(r.content)
    definitions1 = []
    for text in root.iter("text"):
        definitions1.append(text.text)
    alphabet = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о",
                "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]
    def_list = []
    for d in definitions1:
        if bool(set(alphabet).intersection(set(d.lower()))) == True:
            def_list.append(d)
    return def_list


def get_multitran_definition(aword):
    """Парсит русские значения с Multitran."""
    url = "https://www.multitran.com/c/M.exe?a=3&&s=" + aword + "&sc=10000&l1=1&l2=2&ex=1"
    r = requests.get(url + aword)
    soup = BeautifulSoup(r.text, 'lxml')
    s = ''
    list2 = []
    list3 = []
    for n in soup.find_all(class_='phraselist2'):
        s += (n.text + "\n")
    list1 = s.split("\n")
    for item in list1:
        new = item
        if '(' in item:
            new = item.split(" (")[0]
        list2.append(new)
    for i in list2:
        if " " in i:
            list3.append(i)
        if i == "":
            list3.append(i)
    res_list = list(set(list2) - set(list3))
    return res_list


def get_example_translation(an_example):
    """Получает перевод текста (примера) с yandex.translator через API."""
    folder_id = 'ВАШ FOLDER ID'
    target_language = 'ru'
    if not an_example:
        return ""
    texts = [an_example]
    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
        "folderId": folder_id,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }
    resp = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                         json=body,
                         headers=headers
                         )
    trans_data = resp.json()["translations"]
    text_dict = trans_data[0]
    translation = text_dict.get('text')
    return translation


def find_example(aword, exampList):
    """Находит английские примеры в списке примеров по английскому слову."""
    found_example = ""
    for e in exampList:
        f = e.lower()
        for s in f.split():
            a = s.strip(string.punctuation)
            if aword == a:
                found_example = e.strip('\n')
                break
        for s in f.split():
            a = s.strip(string.punctuation)
            if jellyfish.jaro_distance(aword, a) > 0.96:
                found_example = e.strip('\n')
                break
    return found_example


def find_equal(ex_tran_string, defin_list):
    global jelly_index, repeat
    """Возвращает основное слово и слово примера по русскому примеру и списку значений."""
    word_list = []
    percentage_list = []
    frequency_list = []
    max_perc_dict = {}
    # делим пример на слова и очищаем их от всякой шняги
    for piece in ex_tran_string.lower().split(' '):
        s = piece.strip('\n').strip('\r').strip(string.punctuation)
        word_list.append(s)
    # проверяем каждое значение на полное совпадение с одним из слов примера
    w1, w2 = "", ""
    exit_flag = False
    count = 0
    for d in defin_list:
        for w in word_list:
            if d == w:
                return [d, d]  # основное слово и слово примера
            if ' ' in d:  # на случай если слово составное:
                if w != word_list[0] and w != word_list[-1]:
                    w1 = word_list[word_list.index(w) - 1] + " " + w
                    w2 = w + " " + word_list[word_list.index(w) + 1]
                elif w == word_list[0]:
                    w1 = w + " " + word_list[word_list.index(w) + 1]
                elif w != word_list[-1]:
                    w1 = word_list[word_list.index(w) - 1] + " " + w
            if d == w1 or d == w2:
                return [d, d]  # основное слово и слово примера
            elif d != w:
                count += 1
                if count == len(word_list):
                    exit_flag == True
                    break
        if exit_flag:
            break
        # если полного совпадения нет
        count = 0
        for d in defin_list:
            for w in word_list:
                # получаем для каждого d процент совпадения с каждым w
                percentage_list.append(jellyfish.jaro_distance(d, w))
                # добавляем в список слово примера, если с ним совпадение > jelly_index
                if jellyfish.jaro_distance(d, w) > jelly_index:
                    frequency_list.append(w)
            # после каждого прохода d по t добавляем в словарь пару "макс. % совпадения : слово, соотв. этому проценту"
            max_perc_dict[(max(percentage_list))] = d
            percentage_list = []
            # из словаря пар "% : значение"" находим макс.% и его пару - значение, кот. будет считаться основным словом
    main_word = max_perc_dict.get(max(max_perc_dict.keys()))
    # чтобы определить слово примера, находим слово, с которым чаще всего был процент совпадения > jelly_index
    if frequency_list == []:
        while (repeat < 25):
            repeat += 1
            jelly_index += 0.01
        return [main_word, "-"]
    else:
        ex_word = mode(frequency_list)
    return [main_word, ex_word]


# код из интернета, чтоб работал редактируемый ввод

__all__ = ['set_startup_hook']
rl = Readline()
if rl.disable_readline:
    def dummy(completer=""):
        pass
    for funk in __all__:
        globals()[funk] = dummy
else:
    def GetOutputFile():
        return rl.console
    __all__.append("GetOutputFile")
    import pyreadline.console as console
    set_startup_hook = rl.set_startup_hook
    callback_handler_install = rl.callback_handler_install
    callback_handler_remove = rl.callback_handler_remove
    callback_read_char = rl.callback_read_char
    console.install_readline(rl.readline)
__all__.append("rl")

# конец кода из интернета


def editable_input(prefill):
    """Делает возможным редактирование строки прямо при вводе."""
    rl.set_startup_hook(lambda: pyreadline.insert_text(prefill))
    try:
        return input(Fore.GREEN)
    finally:
        rl.set_startup_hook()
        print(Fore.RESET)


def start():
    """Приветственное меню."""
    global random_mode
    art_1 = text2art("AnkiMaster", font="small")
    print(art_1)
    print("""• обработать текст - 1
• проверить слова - 2
• добавить слова из списка - Enter
• добавить отдельное слово - 0""")
    print(Fore.RESET)
    next_step = input(Fore.GREEN)
    if next_step == "1":
        split_text()
    elif next_step == "2":
        checking()
    elif next_step == "0":
        random_mode = True
        rando()


def check_yandex_token():
    """Проверяет токен Yandex Dictionary. Если скрипт запущен на ПК, автоматически обновляется через cmd и curl.
Если скрипт запущен на телефоне, просит ввести новый токен."""
    global IAM_TOKEN
    if platform_type == "AMD64":
        current_datetime = datetime.datetime.now()
        with open(pc_token_file_path, 'r') as file:
            print(Fore.RESET + "Проверка токена...")
        t.sleep(2)
        try:
            get_example_translation("A.")
            with open(token_starts_file_path, 'r') as file:
                token_startstring = file.read()
            token_start_datetime = datetime.datetime.strptime(token_startstring, '%Y-%m-%d %H:%M:%S.%f')
            time_difference = str(current_datetime - token_start_datetime)
            new_time_difference = time_difference.split(":")[0]
            if int(new_time_difference) < 10:
                print("Токен в порядке. Истекает через", 12 - int(new_time_difference), "часа(-ов).")
                t.sleep(2)
            else:
                print("Дата")
                token_starts = str(datetime.datetime.now())
                with open(pc_token_file_path, 'wb', 0) as file:
                    subprocess.run(
                        r'c:\windows\system32\cmd.exe /C curl -d "{\"yandexPassportOauthToken\":\"ВАШ OAUTH-ТОКЕН\"}" "https://iam.api.cloud.yandex.net/iam/v1/tokens"',
                        stdout=file, check=True)
                with open(token_starts_file_path, 'w') as file:
                    file.write(token_starts)
                    print("Новый токен был получен, так как предыдущий скоро устареет.")
                    t.sleep(2)
        except KeyError:
            start_date_time = datetime.datetime.now()
            with open(pc_token_file_path, 'wb', 0) as file:
                subprocess.run(
                    r'c:\windows\system32\cmd.exe /C curl -d "{\"yandexPassportOauthToken\":\"ВАШ OAUTH-ТОКЕН\"}" "https://iam.api.cloud.yandex.net/iam/v1/tokens"',
                    stdout=file, check=True)
            with open(pc_token_file_path, 'r') as file:
                line = file.read()
            IAM_TOKEN = json.loads(line)["iamToken"]
            token_starts = str(start_date_time)
            with open(token_starts_file_path, 'w') as file:
                file.write(token_starts)
            print("Новый токен был получен, так как предыдущий уже устарел.")
            t.sleep(2)
    elif platform_type == "aarch64":
        print(Fore.RESET + "Проверка токена...")
        try:
            get_example_translation("A.")
            print("\nТокен в порядке.\n")
        except KeyError:
            print("\nОшибка! Введите новый токен!")
            IAM_TOKEN = input(Fore.GREEN)
            print(Fore.RESET)
            with open(token_file_path, "w") as file:
                file.write(IAM_TOKEN.strip("\n"))


def added_today():
    """Справка по количеству слов, добавленных за сутки."""
    global today_count
    current_date = str(date.today())
    with open(today_date_file_path, "r") as file:
        today_date = file.read()
    with open(today_count_file_path, "r") as file:
        today_count = file.read()
    if current_date.strip('\n') != today_date:
        today_count = 0
    with open(today_date_file_path, "w") as file:
        file.write(current_date)
    with open(today_count_file_path, "w") as file:
        file.write(str(today_count))


def begin_from_dict(this_list):
    """Формирует словарь для редактирования (удаления/перемещения слов) непосредственно перед добавлением."""
    global word, second_word
    checked_list = []
    file_to_list(checked_file_path, checked_list, True)
    ch_dict = {}
    c = 1
    for i in this_list:
        ch_dict[c] = i.strip("\n")
        c += 1
    first_list, remove_list, second_list, move_list = [], [], [], []
    while (True):
        print('Введите число показываемых слов (максимум ' + str(
            len(this_list)) + '), введите слово или "0" чтобы взять случайное:\n')
        action = input(Fore.GREEN)
        print(Fore.RESET)
        if action == "$":
            word = random.choice(queue_list)
            second_word = word
            first_menu()
            return None
        elif action.isdigit() and action != "0":
            if len(this_list) < int(action):
                colorama.init()
                print(Fore.YELLOW + "\nВведите число, меньшее или равное " + str(len(this_list)) + "!\n", Fore.RESET)
                continue
        elif (action.isalpha()) and not action in ch_dict.values() and action != "$":
            print(Fore.YELLOW, "\nТакого слова нет.", Fore.RESET)
            continue
        elif (action.isalpha()) and action in ch_dict.values():
            for value in ch_dict.values():
                if action == value:
                    word = action
                    second_word = word
                    first_menu()
                    return None
        elif action == "0":
            word = random.choice(checked_list)
            second_word = word
            first_menu()
            return None
        else:
            print(Fore.YELLOW, "\nНеверный ввод.", Fore.RESET)
            continue
        cocount = 0
        for key, value in ch_dict.items():
            print(Fore.CYAN, key, ':', value, Fore.RESET)
            cocount += 1
            if cocount == int(action):
                break
        how_many()
        local_exit_flag = False
        print("""\n• Удалить - номера через запятую без пробелов.
• Закончить и перейти к следующему шагу - 0.
• Групповое перемещение слов в известные - y.
• Сформировать очередь показываемых слов - q.\n""")
        next_step = editable_input("0")
        try:
            if next_step == '0':
                break
            elif next_step != '0' and next_step != 'y' and next_step != 'q':
                first_list = next_step.split(",")
                print()
                for f in first_list:
                    if int(f) in ch_dict:
                        k = int(f)
                        print(Fore.CYAN, ch_dict.get(k), Fore.RESET)
                    elif not int(f) in ch_dict:
                        print("\nНомер " + f + " не найден.")
                        local_exit_flag = True
                        break
                if local_exit_flag == True:
                    continue
                print(Fore.YELLOW + "\nЭти слова будут удалены. Вы уверены? (y/n)\n", Fore.RESET)
                answer = input(Fore.GREEN)
                print(Fore.RESET)
                if answer == 'y':
                    for f in first_list:
                        k = int(f)
                        remove_list = [ch_dict.get(k)]
                        del ch_dict[k]
                        this_list = list(set(this_list) - set(remove_list))
                        file_write(checked_file_path, this_list)
                    print("\nСлова успешно удалены.")
            elif next_step == 'y':
                print("""\nТеперь введите номера слов через запятую без пробела для перемещения их в известные.
• Закончить и перейти к следующему шагу - 0.\n""")
                numbers = editable_input("0")
                if numbers == '0':
                    break
                elif next_step != '0' and not numbers.isalpha():
                    second_list = numbers.split(",")
                    print()
                    for s in second_list:
                        if int(s) in ch_dict:
                            m = int(s)
                            print(Fore.CYAN, ch_dict.get(m), Fore.RESET)
                        elif not int(s) in ch_dict:
                            print(Fore.YELLOW, "\nНомер " + s + " не найден.", Fore.YELLOW)
                            local_exit_flag = True
                            break
                if local_exit_flag == True:
                    break
                print(Fore.YELLOW, "\nЭти слова будут перемещены в известные. Вы уверены? (y/n)\n", Fore.RESET)
                answer = input(Fore.GREEN)
                print(Fore.RESET)
                if answer == 'y':
                    for s in second_list:
                        if not int(s) in ch_dict:
                            print("\nНомер " + s + " не найден.")
                            break
                        elif int(s) in ch_dict:
                            m = int(s)
                            move_list = [ch_dict.get(m)]
                            known_list.append(ch_dict.get(m))
                            del ch_dict[m]
                            this_list = list(set(this_list) - set(move_list))
                            file_write(checked_file_path, this_list)
                            file_write(known_file_path, known_list)
                    print("\nСлова перемещены в известные.\n")
                    print("\nВ известных теперь", len(known_list), "слов.")
            elif next_step == 'q':
                print("""\nТеперь введите номера слов через запятую без пробела для формирования очереди.
• Закончить и перейти к следующему этапу - 0.\n""")
                queue = editable_input("0")
                if queue == '0':
                    break
                elif next_step != '0' and not queue.isalpha():
                    q_list = queue.split(",")
                    print()
                    for q in q_list:
                        if int(q) in ch_dict:
                            e = int(q)
                            print(Fore.CYAN, ch_dict.get(e), Fore.RESET)
                        elif not int(q) in ch_dict:
                            print(Fore.YELLOW, "\nНомер " + q + " не найден.", Fore.YELLOW)
                            local_exit_flag = True
                            break
                if local_exit_flag == True:
                    break
                print(Fore.YELLOW, "\nСформировать очередь из этих слов? (y/n)\n", Fore.RESET)
                answer = input(Fore.GREEN)
                print(Fore.RESET)
                if answer == 'y':
                    for q in q_list:
                        if not int(q) in ch_dict:
                            print("\nНомер " + q + " не найден.")
                            break
                        elif int(q) in ch_dict:
                            e = int(q)
                            queue_list.append(ch_dict.get(e))
                            file_write(queue_file_path, queue_list)
                    print("\nОчередь слов сформирована.\n")
        except ValueError:
            print(Fore.YELLOW, "\nНеверный ввод.", Fore.RESET)
            continue


def choose_word():
    """Меню выбора слова из списка."""
    global word, second_word, ch_dict, checked_list
    create_ch_dict()
    for w in checked_list:
        print("""\n• Чтобы взять определенное слово, введите номер или само слово.
• Взять любое слово - 0. 
• Взять слово из очереди - $.
• Отобразить список - *.\n""")
        next_word = editable_input("0")
        if next_word == "*":
            begin_from_dict(checked_list)
            continue
        elif next_word == "$":
            word = random.choice(queue_list)
            second_word = word
            return None
        elif next_word.isdigit() == True and not int(next_word) in ch_dict.keys() and next_word != '0':
            print(Fore.YELLOW, "Слова с таким номером нет.", Fore.RESET)
            continue
        elif (next_word.isdigit()) and int(next_word) in ch_dict.keys():
            for key, value in ch_dict.items():
                if int(next_word) == key:
                    word = value
                    second_word = word
                    return None
        elif (next_word.isalpha()) and not next_word in ch_dict.values():
            print(Fore.YELLOW, "Такого слова нет.", Fore.RESET)
            continue
        elif (next_word.isalpha()) and next_word in ch_dict.values():
            for value in ch_dict.values():
                if next_word == value:
                    word = next_word
                    second_word = word
                    return None
        elif next_word == "0":
            word = random.choice(checked_list)
            second_word = word
            return None
        else:
            print(Fore.YELLOW, "\nНеверный ввод.", Fore.RESET)
            continue


def continue_with_word(get_defs, find_ex, trans_ex, get_trans):
    """Формирует и отображает таблицу с англ. словом, переводом, транскрипцией, примеромом, переводом примера,
основным словом и словом примера."""
    global new_main_definition, new_examp_word, word, new_rus_ex, IAM_TOKEN
    global new_rus_ex, example_translation, main_definition, examp_word
    global transcription, example, definitions, random_mode, jelly_index, repeat
    if get_defs == True:
        try:
            definitions = get_yandex_definition(word)
        except:
            print(Fore.YELLOW, "\nТакое слово в словаре не найдено!", Fore.RESET)
            definitions = [""]
    if find_ex == True and random_mode == False:
        example = find_example(word, ex_list)
    if trans_ex == True:
        if random_mode == False:
            example = find_example(word, ex_list)
        example_translation = get_example_translation(example)
    elif new_rus_ex != "":
        example_translation = new_rus_ex
        new_rus_ex = ""
    if get_trans == True:
        transcription = get_transcription(word)
    if (definitions):
        repeat = 0
        equality_list = find_equal(example_translation, definitions)
        jelly_index = 0.85
    else:
        equality_list = ["-", "-"]
        definitions = ["-"]
        main_definition = "-"
        examp_word = "-"
    if new_main_definition != "":
        main_definition = new_main_definition
        new_main_definition = ""
    elif (definitions) and len(equality_list) > 2:
        main_definition = "-"
    elif (equality_list) and len(equality_list) <= 2 and (definitions):
        main_definition = equality_list[0]
    if new_examp_word != "":
        examp_word = new_examp_word
        new_examp_word = ""
    elif (definitions) and len(equality_list) > 2:
        examp_word = "-"
    elif (equality_list) and len(equality_list) <= 2 and (definitions):
        examp_word = equality_list[1]

        # вывод результата в табличной форме:
    defs = ", ".join(definitions)
    lines = [word + transcription, defs, example.strip('\n').strip("\r"), example_translation.strip('\n').strip("\r"),
             main_definition, examp_word]
    max_length = 49
    count = 0
    print(Fore.CYAN)
    for l in lines:
        print('+-' + '-' * (max_length) + '-+')
        if len(l) > 50:
            count += 1
            for w in wrap(l, max_length):
                print(' {0:{1}} '.format(w, max_length))
                if l == lines[-1]:
                    print('+-' + '-' * max_length + '-+')
        else:
            print(' {0:{1}} '.format(l, max_length))
            if count == 5:
                print('+-' + '-' * max_length + '-+')
            count += 1


def delete_word():
    """Удаляет слово из списка."""
    global word, old_word, checked_list, queue_list
    checked_list = []
    file_to_list(checked_file_path, checked_list, True)
    create_ch_dict()
    if old_word != "":
        deleting = old_word
    else:
        deleting = word
    k = 0
    for key, value in ch_dict.items():
        if value == deleting:
            k = key
            break
    ch_list = [ch_dict.get(k)]
    del ch_dict[int(k)]
    checked_list = list(set(checked_list) - set(ch_list))
    if ch_list[0] in queue_list:
        queue_list = list(set(queue_list) - set(ch_list))
        file_write(queue_file_path, queue_list)
    create_ch_dict()
    file_write(checked_file_path, checked_list)
    print("\nСлово удалено.")
    word = ""
    old_word = ""


def create_ch_dict():
    """Формирует словарь номер:слово."""
    global checked_list, ch_dict
    c = 1
    ch_dict = {}
    for i in checked_list:
        ch_dict[c] = i
        c += 1


def add_to_known():
    """Переносит слова в известные."""
    global word, old_word, checked_list
    known_list = []
    file_to_list(known_file_path, known_list, True)
    known_list = [line.rstrip() for line in known_list]
    added_list = []
    if word in known_list:
        print(Fore.CYAN, "\nСлово уже есть в известных!", Fore.RESET)
        start()
    else:
        checked_list = []
        file_to_list(checked_file_path, checked_list, True)
        known_list.append(word)
        if old_word == "":
            added_list = [word]
        elif old_word != "":
            added_list = [old_word]
        checked_list = list(set(checked_list) - set(added_list))
        create_ch_dict()
        file_write(checked_file_path, checked_list)
        file_write(known_file_path, known_list)
        print("\nСлово перемещено в известные.")


def edit_and_add_to_known():
    """Редактирует и переносит слова в известные."""
    global word, old_word, checked_list
    known_list = []
    file_to_list(known_file_path, known_list, True)
    known_list = [line.rstrip() for line in known_list]
    if word in known_list:
        print(Fore.YELLOW, "\nСлово уже есть в известных!", Fore.RESET)
    checked_list = []
    file_to_list(checked_file_path, checked_list, True)
    create_ch_dict()
    edited = editable_input(word)
    known_list.append(edited)
    added_list = []
    if old_word == "":
        added_list = [word]
    elif old_word != "":
        added_list = [old_word]
    checked_list = list(set(checked_list) - set(added_list))
    file_write(checked_file_path, checked_list)
    file_write(known_file_path, known_list)
    print("\nСлово перемещено в известные.")


def add_word():
    """Формирует и добавляет в файл исходную строку, удаляет добавленные слова из исходного списка, вызывает функцию
fuck_excel() для формирования строк для импорта в Anki."""
    global word, second_word, old_word
    global today_count, checked_list, queue_list, random_mode
    learning_list = []
    file_to_list(learning_file_path, learning_list, True)
    learning_list = [line.rstrip() for line in learning_list]
    if old_word == '' and random_mode == False:
        second_word = word
    elif old_word != "" and random_mode == False:
        second_word = old_word
    if word in learning_list:
        print(Fore.YELLOW, "\nСлово уже есть в изучаемых!", Fore.RESET)
        random_mode = False
        start()
    else:
        to_append = word + '*' + second_word + "*" + transcription + "*" + main_definition + "*" + examp_word + "*" + example.strip(
            '\n').strip('\r') + "*" + example_translation.strip('\n').strip('\r')
        for_anki_list.append(to_append)
        file_write(for_anki_file_path, for_anki_list)
        today_count = int(today_count) + 1
        with open(today_count_file_path, 'w') as file:
            file.write(str(today_count))
        if old_word == '':
            deleting = word
            added_list = [word]
        else:
            added_list = [old_word]
            deleting = old_word
        checked_list = []
        file_to_list(checked_file_path, checked_list, True)
        create_ch_dict()
        k = 0
        for key, value in ch_dict.items():
            if value.strip("\r") == deleting.strip("\r"):
                k = key
                break

        checked_list = list(set(checked_list) - set(added_list))
        ch_list = [ch_dict.get(k)]
        if random_mode == False:
            del ch_dict[int(k)]

        if ch_list[0] in queue_list:
            queue_list = list(set(queue_list) - set(added_list))
            file_write(queue_file_path, queue_list)

        create_ch_dict()
        file_write(checked_file_path, checked_list)

        learning_list.append(word)
        file_write(learning_file_path, learning_list)

        mp3_list.append("en_" + word + ".mp3")
        file_write(mp3_file_path, mp3_list)

        print("\nСлово добавлено.")
        print("\nИсходная запись выглядит так:\n ")
        print(Fore.CYAN, to_append, Fore.RESET)
        fuck_excel(to_append)
        how_many()
        old_word = ""
        second_word = ""


def first_menu():
    """Первое меню действий со словом."""
    global checked_list, word, old_word, second_word, definitions
    global example, example_translation, jelly_index
    print(Fore.RESET)
    print("Слово:", Fore.CYAN, word)
    print(Fore.RESET)
    if get_transcription(word) == " [null]" and len(get_yandex_definition(word)) == 0:
        colorama.init()
        print(Fore.YELLOW + '\nОтсутствуют транскрипция и значения!', Fore.RESET)
    elif len(get_yandex_definition(word)) == 0:
        colorama.init()
        print(Fore.YELLOW + '\nОтсутствуют значения!', Fore.RESET)
    else:
        print(Fore.CYAN)
        print(get_yandex_definition(word), Fore.RESET)
    print("\nЧто нужно сделать:")
    print("• пропустить/другое слово - 1")
    print("• удалить - 2")
    print("• продолжить - 3")
    print("• ред. английское слово - 4")
    print("• вывести список - 5")
    print("• добавить в известные - 6")
    print("• ред. и добавить в известные - 7\n")
    response = input(Fore.GREEN)
    print(Fore.RESET)
    if response == '1':
        second_word = ""
        old_word = ""
        word = random.choice(checked_list)
        first_menu()
    elif response == '2':
        delete_word()
        choose_word()
        first_menu()
    elif response == '3':
        token()
        continue_with_word(True, True, True, True)
        continue_menu()
    elif response == '4':
        token()
        jelly_index = 0.75
        print("\nВведите слово:\n")
        new_word = editable_input(word)
        example = find_example(word, ex_list)
        example_translation = get_example_translation(example)
        old_word = word
        second_word = old_word
        word = new_word
        continue_with_word(True, False, False, True)
        continue_menu()
    elif response == '5':
        begin_from_dict(checked_list)
        checked_list = []
        file_to_list(checked_file_path, checked_list, True)
        checked_list = [line.rstrip() for line in checked_list]
        choose_word()
        first_menu()
    elif response == '6':
        second_word = ""
        old_word = ""
        add_to_known()
        choose_word()
        first_menu()
    elif response == '7':
        second_word = ""
        old_word = ""
        edit_and_add_to_known()
        choose_word()
        first_menu()
    else:
        print(Fore.YELLOW)
        print("Неверный ввод!\n")
        first_menu()


def continue_menu():
    """Второе меню действий со словом."""
    global definitions, jelly_index, word, old_word, second_word, main_definition
    global new_main_definition, examp_word, new_examp_word, example_translation, example, random_mode
    print(Fore.RESET, "Слово: " + Fore.CYAN, word, Fore.RESET)
    print("\nИндекс совпадения равен", jelly_index)
    print("\nЧто нужно сделать:")
    print("• пропустить - 1")
    print("• удалить - 2")
    print("• добавить - 3")
    print("• ред. английское слово - 4")
    print("• ред. основное значение и слово примера - 5")
    print("• добавить в известные - 6")
    print("• ред. и добавить в известные - 7")
    print("• изменить индекс совп. и перезапустить - 8")
    print("• ред. перевод примера - 9")
    print("• взять значения у Multitran - m")
    print("• взять значения у Yandex - y\n")
    answer = input(Fore.GREEN)
    print(Fore.RESET)
    if answer == '1':
        second_word = ""
        old_word = ""
        jelly_index = 0.75
        word = random.choice(checked_list)
        first_menu()
    elif answer == '2':
        jelly_index = 0.75
        delete_word()
        choose_word()
        first_menu()
    elif answer == '3':
        token()
        jelly_index = 0.75
        add_word()
        if random_mode == True:
            print("\nПродолжить (y) или перейти к добавлению из списка (n)")
            reply = input()
            if reply == "y":
                rando()
            elif reply == "n":
                random_mode = False
        choose_word()
        first_menu()
        old_word = ""
        second_word = ""
    elif answer == '4':
        token()
        jelly_index = 0.75
        print("\nВведите слово:\n")
        new_word = editable_input(word)
        old_word = word
        second_word = old_word
        word = new_word
        continue_with_word(True, False, False, True)
        continue_menu()
        old_word = ""
        second_word = ""
    elif answer == '5':
        jelly_index = 0.75
        print("\nВведите основное значение:\n")
        new_main_definition = editable_input(main_definition)
        main_definition = new_main_definition
        print("\nВведите слово примера:\n")
        if examp_word != "":
            new_examp_word = editable_input(examp_word)
        else:
            new_examp_word = editable_input(main_definition)
            examp_word = new_examp_word
        continue_with_word(False, False, False, False)
        continue_menu()
    elif answer == '6':
        second_word = ""
        old_word = ""
        jelly_index = 0.75
        add_to_known()
        choose_word()
        first_menu()
    elif answer == '7':
        second_word = ""
        old_word = ""
        jelly_index = 0.75
        edit_and_add_to_known()
        choose_word()
        choose_word()
        first_menu()
    elif answer == '8':
        print("\nВведите новый индекс совпадения.\n")
        jelly_index = float(input(Fore.GREEN))
        print(Fore.RESET)
        continue_with_word(False, True, True, False)
        continue_menu()
    elif answer == '9':
        jelly_index = 0.75
        print("\nВведите новый пример:\n")
        new_rus_ex = editable_input(example_translation)
        example_translation = new_rus_ex
        continue_with_word(False, False, False, False)
        continue_menu()
    elif answer == "m":
        jelly_index = 0.75
        definitions = get_multitran_definition(word)
        continue_with_word(False, False, False, False)
        continue_menu()
    elif answer == "y":
        jelly_index = 0.75
        definitions = get_yandex_definition(word)
        continue_with_word(False, False, False, False)
        continue_menu()
    else:
        print(Fore.YELLOW)
        print("Неверный ввод!\n")
        continue_menu()


token()
start()
check_yandex_token()
added_today()
begin_from_dict(checked_list)
choose_word()
first_menu()

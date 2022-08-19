Данный README находится в процессе написания и не является окончательным вариантом.

***

Код скрипта находится в файле main.py.

***

Внимание! Для работы скрипта необходимы API-ключи Yandex. Dictionary и Yandex.Translator (платно). Инструкции для их получения находятся по ссылкам:

https://yandex.ru/dev/dictionary/

https://cloud.yandex.ru/docs/translate/

Строки кода, в которых необходимо ввести свои данные: 551, 593, 774, 784.

В будущем планирую написать версию с использованием бесплатного API.

***

Я очень люблю учить новые английские слова и делаю это с помощью программы Anki. Это инструмент для интервального повторения материала. В Anki слова можно добавлять медленно и кропотливо вручную, а можно по шаблону и быстро, просто импортируя текстовый файл с нужными словами.

В какой-то момент я понял, что вручную - не мой вариант, и тогда начались шаги в сторону автоматизации процесса. Я много работал в Excel, но в итоге пришел к скрипту на Python.

У моего скрипта обширный список фич, но постараюсь вкратце разъяснить основные шаги работы.

1. Взять обычный английский текст, разбить его на предложения, разбить на слова.
2. Сравнить полученные слова с базами слов и сформировать список слов, у которых не было совпадений. Под базами подразумеваются списки слов, которые я знаю и которые уже находятся на изучении. Причем, учитываются и словоформы. То есть, если мне известно слово play, то скрипт "понимает", что слова plays, played и playing также мне известны и не учитывает их в формировании списка неизвестных слов. Примечание: 1 и 2 шаги выполняются только один раз для нового текста и повторяются только тогда, когда текущий список неизвестных слов полностью обработан.
3. Из списка неизвестных слов выбирается одно слово. Подключаются парсеры значений, транскрипции, API Яндекса и еще пара-тройка написанных мной функций.
4. В итоге, карточка слова выглядит так:

![изображение](https://user-images.githubusercontent.com/71543252/185357058-b2db4d59-77aa-4c9a-ac36-81804c627319.png)

5. Далее появляется меню, и перед нами предстает свобода выбора:

![изображение](https://user-images.githubusercontent.com/71543252/185353855-41ea881f-5fb9-41da-bc08-79ea729499e0.png)

6. Если мы выбираем "добавить", происходит следующее: слово удаляется из списка неизвестных слов и добавляется в список изучаемых слов. Далее, из вышеупомянутой карточки слова формируются четыре разные строки. Эти четыре строки для каждого слова и импортируются в Anki.

Почему четыре строки? Дело в том, что за много лет изучения слов, я пришел к наиболее эффективному, на мой взгляд, способу изучения английских слов. И этот способ содержит четыре упражнения. Далее я продемонстрирую, как они выглядят уже в программе Anki после импорта.

Упражнение 1: показывается английский пример. Английское слово, которое нужно перевести, выделено. Обратите внимание, что если слово в измененной форме, в скобочках показывается то, что нужно перевести. 

![изображение](https://user-images.githubusercontent.com/71543252/185357625-a14f5fd0-2da2-4036-97f4-4a87e0cf40fb.png)

Упражнение 2: тот же английский пример, то же слово, но на этот раз - сразу на русском. 

![изображение](https://user-images.githubusercontent.com/71543252/185357844-34ffb726-73fd-4513-927f-e86423c0264a.png)

Упражнение 3: дается слово на русском и перемешанные буквы английского эквивалента, который нужно вписать вручную.

![изображение](https://user-images.githubusercontent.com/71543252/185359387-a8e8dd58-3394-4c9d-a122-6c226e32adc1.png)

Упражнение 4: на этот раз уже переведенный на русский язык пример, а вот слово в нем на английском.

![изображение](https://user-images.githubusercontent.com/71543252/185359922-3fae00f6-6c58-45d6-8e6a-d83b3576b7e0.png)

Возможно, выглядит странно, но именно эти упражнения вкупе с интервальными повторениями позволяют мне эффективно учить слова. После того как я начал использовать этот способ, количество забытых слов резко сократилось.

***

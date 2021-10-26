# Keyboa
[![Download Keyboa](https://img.shields.io/pypi/v/keyboa.svg)](https://pypi.python.org/pypi/keyboa)
![PyPI - Downloads](https://img.shields.io/pypi/dm/keyboa?color=yellow&logo=pypi&logoColor=yellow)
[![Build Status](https://travis-ci.com/torrua/keyboa.svg?branch=master)](https://travis-ci.com/torrua/keyboa)
![CodeQL](https://github.com/torrua/keyboa/workflows/CodeQL/badge.svg?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/torrua/keyboa/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/torrua/keyboa/?branch=master)
[![codecov](https://codecov.io/gh/torrua/keyboa/branch/master/graph/badge.svg?token=H4MO1Y3DDY)](https://codecov.io/gh/torrua/keyboa)
[![GitHub license](https://img.shields.io/github/license/torrua/keyboa)](https://github.com/torrua/keyboa/blob/master/LICENSE)

Это простая, но гибкая утилита для генерации клавиатуры, которая работает как дополнение к пакету PyTelegramBotAPI. С помощью **keyboa** можно:
- быстро создать клавиши со сложными колбеками,
- создавать клавиатуры из списков,
- с легкостью объединить несколько клавиатур в одну,
- и множесто других интересных вещей...

> 📖 Этот гайд актуален для версии Keyboa 3 и выше.
> Если используется Keyboa версии 2 и ниже, используйте [этот гайд](README_for_v2.md).

> 📌 **ОБРАТИТЕ ВНИМАНИЕ**: 
> 
> Версия 3 не совместима с 2й версией.
> В случае обновления со 2й до 3й версии, имейте ввиду, что придётся подстраивать Ваш код.

## Установка
Keyboa совместима с Python версии 3.7 и выше. Установить этот пакет возможно, как обычно, используя pip:
```sh
$ pip install keyboa
```
После этого остаётся только импортировать:
```python
from keyboa import Keyboa
```

## Быстрый Запуск
### Базовая клавиатура
Простейшая клавиатура в телеграм может быть создана следующим образом:
```python
menu = ["spam", "eggs", "ham"]
keyboard = Keyboa(items=menu)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard())
```
![keyboard from list of str](https://telegra.ph/file/d9280b11ed11ec13e6f56.png)

### Базовая, структурированная клавиатура
Если необходимо создать клавиатуру с предопределённой структурой:
```python
menu = [["spam", "eggs"], ["ham", "bread"], "spam"]
keyboard = Keyboa(items=menu)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard())
```
![keyboard from list of str](https://telegra.ph/file/2eb6752324fa196cae4ac.png)

Это хороший старт, но всё же, более подробно остановимся на том, как всё это работает, а заодно и отметим дополнительные особенности которые можно использовать.

## Как это работает 

Класс ```Keyboa``` предоставляет два варианта создания клавиатуры pyTelegramBotAPI совместимые с типом ```InlineKeyboardMarkup```: метод ```slice()``` и свойством ```keyboard```.
Используя [класс Keyboa](#keyboa-class) описание ниже служит лишь примером демонстрации нюансов и ограничений модуля. Обратим внимание на следующий пример.

## Создание клавиатуры
Легчайшим способом создания клавиатуры, будет инициализация (init) объекта Keyboa списком элементов и свойством ```keyboard```.
```python
menu = ["spam", "eggs", "ham"]
keyboard = Keyboa(items=menu)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard())
```
![keyboard from list of str](https://telegra.ph/file/d9280b11ed11ec13e6f56.png)

По дефолту, каждый элемент становиться отдельной строкой. Это легко изменить объединив элементы в группы.
```python
menu = [["spam", "eggs"], ["ham", "bread"], "spam"]
keyboard = Keyboa(items=menu)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard())
```
![keyboard from list of str](https://telegra.ph/file/2eb6752324fa196cae4ac.png)

Как видите, клавиши клавиатуры расположились именно таким образом, каким они были расположены в списке. 

Обратите внимание, что последний объект "spam" располагается  отдельной строкой. И это при условии, что его не разместили в отдельный список.

Разумеется есть возможность создать более сложные структуры. К примеру:
```python
menu = [["spam", "eggs", "ham"], ["ham", "eggs"], ["spam", ] ["sausages", "spam"], ["eggs", "spam", "spam"]]
keyboard = Keyboa(items=menu)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard())
```
![keyboard from list of str](https://telegra.ph/file/faff37512c626845c5524.png)

>В связи с ограничениями Telegram API, позволяется добавить **максимум 8 клавиш в строке** и **максимум 100 клавиш на всю клавиатуру**.

Заглянем глубже. Предположем, что у имеется список из 24 элементов и необдходимо расположить 6 элементов в 1 ряд. Вот, что вам требуется:
```python
numbers = list(range(1, 25))
keyboard = Keyboa(items=numbers, items_in_row=6)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard())
```
![keyboard with 6 items_in_row](https://telegra.ph/file/2122cb9f50938b39b4439.png)

💡 Можно с лёгкостью создать 3, 4 или даже 8 клавиш в ряд, изменяя лишь параметр ```items_in_row```.

Добавим больше атрибутов, чтобы продемонстрировать, как изменения отобразяться на нашем результате:
```python
keyboa = Keyboa(items=list(range(0, 48)), alignment=True)
keyboard = keyboa(slice(5, 37))
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
```
![keyboard slice with alignment](https://telegra.ph/file/cc41513058a2b3d9f83ba.png)

Как можно заметить, эта клавиатура состоит из сегмента ```[5:37]```. В дополнении, несмотря на то, что не указан показатель ```items_in_row```, функция разделила список в равные ряды,  за счёт того, что включён параметр ```alignment```.

## Создание Клавиш
💡 Обычно нет необходимости создавать отдельные кнопки, так как они создаются автоматически на основе исходных данных при создании клавиатуры.
Но если есть такая необходимость, это можно сделать следующим образом.
Импортируй класс ```Button``` ([подробное описание](#button-class)), создать объект кнопки из различных типов данных, например таких как ```str```, ```int```, ```tuple```, ```dict``` и обращайся к свойству ```button``` чтобы получить ```InlineKeyboardButton```:
```python
from keyboa import Button
spam = Button(button_data="spam").button
```

#### кнопка ```str``` или ```int```
```python
spam = Button(button_data="spam").button
```
```sh
{'text': 'spam', 'callback_data': 'spam'}
```

#### кнопка ```tuple```
```python
spam = Button(button_data=("spam", "eggs"), front_marker="ham_", back_marker="_spam").button
```
```sh
{'text': 'spam', 'callback_data': 'ham_eggs_spam'}
```
💡 Заметитьте, что в данном примере также использовался ```front_marker``` и ```back_marker```, чтобы добавить определённую данные колбека (callback_data) клавишы.

#### кнопка ```dict``` без клавиши "текста"
```python
spam = Button(button_data={"spam": "ham_eggs_spam"}).button
```
```sh
{'text': 'spam', 'callback_data': 'ham_eggs_spam'}
```

#### кнопка от ```dict``` с клавишей "текст"
```python
spam = Button(button_data={"text": "spam", "url": "https://ya.ru/", "callback_data": "eggs"}).button
```
```sh
{"text": "spam", "url": "https://ya.ru/", "callback_data": "eggs"}
```

## Комбинированная Клавиатура
Иногда необходимо объединить несколько клавиатурных блоков в один большой. Класс метода ```combine()``` в Keyboa, как раз это и делает!

Этот метод имеет лишь один параметр ввода - ```keyboards```. Это должна быть последовательность ```InlineKeyboardMarkup``` объектов. Также может быть представлена, как самостоятельный ```InlineKeyboardMarkup```.

Вот как это работает:
```python
controls = [["⏹️", "⏪️", "⏏️", "⏩️", "▶️"], ]
tracks = list(range(1, 13))

keyboard_controls = Keyboa(items=controls).keyboard
keyboard_tracks = Keyboa(items=tracks, items_in_row=4).keyboard

keyboard = Keyboa.combine(keyboards=(keyboard_tracks, keyboard_controls))
bot.send_message(chat_id=user_id, text=text_tracks, reply_markup=keyboard)
```
![keyboard combo](https://telegra.ph/file/342c06d783faeb786f242.png)

Как заметили, произошло объединение 2х клавиатур в одну.

## Сложные колбеки
Пару слов о процессе создания комплексных колбеков для клавиш. 

Часто необходимо последовательно считывать и перебирать варианты обратного вызова, которые выбрал пользователь. Например, чтобы определить адрес: города, улицы, дома, номер квартиры.

Предложем пользователю выбор из нескольких городов. Для этого создаём простую клавиатуру:
```python
kb_cities = Keyboa(
    items=["Moscow", "London", "Tokyo", ],
    front_marker="&city=",
    back_marker="$"
)
bot.send_message(chat_id=user_id, text="Select your city:", reply_markup=kb_cities())
```
![keyboard cities](https://telegra.ph/file/dcd011c72e43aefd8d00d.png)

При этом внутри клавиатуры получаем следующее:
```sh
{'inline_keyboard': [
    [{'text': 'Moscow', 'callback_data': '&city=Moscow$'}],
    [{'text': 'London', 'callback_data': '&city=London$'}],
    [{'text': 'Tokyo', 'callback_data': '&city=Tokyo$'}]
]}
```
Предположем пользователь выбрал ```London```. Хотелось бы это запомнить и предоставить ему выбор из нескольких улиц:
```python
received_callback = call.data  # "&city=London$"
streets = ["Baker Street", "Oxford Street", "Abbey Road", ]
kb_streets = Keyboa(
    items=streets, 
    front_marker="&street=",
    back_marker=received_callback  # we added existing data to the end
)
bot.send_message(chat_id=user_id, text="Select your street:", reply_markup=kb_streets())
```
![keyboard streets](https://telegra.ph/file/cf06e3bc0adece894535d.png)

```sh
{'inline_keyboard': [
    [{
        'text': 'Baker Street',
        'callback_data': '&street=Baker Street&city=London$'}],
    [{
        'text': 'Oxford Street',
        'callback_data': '&street=Oxford Street&city=London$'}],
    [{
        'text': 'Abbey Road',
        'callback_data': '&street=Abbey Road&city=London$'}]
]}
```
💡 Заметьте, что использовался ```front_marker``` чтобы указать тип выбранных элементов и ```back_marker``` для прикрепления существующей информации.

Как видите, вариант, выбранный пользователем в предыдущем окне, был также сохранен. Если пользователь выберет улицу, например, ```Baker Street```, получаем  ```call.data``` как ```'&street=Baker Street&city=London$'```. Разумеется, можно с легкостью его перехватить.

Наконец, дадим выбрать ему квартиру:
```python
received_callback = call.data  # '&street=Baker Street&city=London$'
apartments = ["221a", "221b", "221c", ]
kb_apartments = Keyboa(
    items=apartments, 
    front_marker="&apartments=", 
    back_marker=received_callback  # we added existing data to the end
)
bot.send_message(chat_id=user_id, text="Select your apartments:", reply_markup=kb_apartments())
```
![keyboard streets](https://telegra.ph/file/0eec50498f2a68955c81c.png)

```sh
{'inline_keyboard': [[
        {'text': '221a',
        'callback_data': '&apartments=221a&street=Baker Street&city=London$'}, 
        {'text': '221b', 
        'callback_data': '&apartments=221b&street=Baker Street&city=London$'},
        {'text': '221c', 
        'callback_data': '&apartments=221c&street=Baker Street&city=London$'}
    ]]
}
```
И если пользователь выберет опцию ```221b```, то можно предположить, что 🕵🏻‍♂️ Шерлок Холмс тоже использует бота!

## Детали
### Класс Keyboa
Атрибут | Тип | Описание
--------- | ---- | -----------
```items``` | BlockItems | _Обязательно_. Список элементов для клавиатуры. Из-за ограничений Telegram Bot API, общее число элементов не должно быть больше 100.
```items_in_row``` | Integer | _Опционально_. Количество клавиш в ряду клавиатуры. Из-за ограничений Telegram Bot API должно быть **от 1 до 8**<br>Значение по умолчанию - ```None``` обозначает, что структура клавиатуры зависит от группировки ```items``` элементов.
```copy_text_to_callback``` | Boolean | Если значение ```True``` и ```button_data``` является ```str``` или ```int```, функция скопирует текст кнопки в данные колбека (и добавит другие маркеры, если они имеются).<br>Значение по умолчанию - ```True```.
```front_marker``` | CallbackDataMarker | _Опционально_. Фронтальная часть данных колбека, которая является общей для всех кнопок.
```back_marker``` | CallbackDataMarker | _Опционально_. Конечная часть данных колбека, которая является общей для всех кнопок.
```alignment``` | Boolean or Iterable | Если значение ```True```, то будет проведена попытка разделить все элементы **на равные ряды в диапазоне от 3 до 5**.<br>Если ```Iterable``` (с любым ```int``` в промежутке от 1 до 8),  будет проведена попытка найти подходящий разделитель между ними.<br><br>Включённый атрибут заменяет действие ```items_in_row``` атрибута, но если подходящий разделитель не смог быть обнаружен, функция будет использовать значение ```items_in_row```.<br><br>Значение по умолчанию - ```None```.
```alignment_reverse``` | Boolean | Если значение ```True```, попытается найти делитель, начиная с конца переменной ```auto_alignment``` (если задано) или из диапазона по умолчанию.<br><br>Включённый параметр работает только в том случае, если включен атрибут ```auto_alignment```.<br><br>Значение по умолчанию - ```None```.

```python
# structureless sequence of InlineButtonData objects
FlatSequence = List[InlineButtonData]

# structured sequence of InlineButtonData objects
StructuredSequence = List[Union[FlatSequence, InlineButtonData]]

# unified type that allows you to use any available data types for the keyboard
BlockItems = Union[StructuredSequence, InlineButtonData]
```

### Класс клавиш
Атрибут | Тип | Описание
--------- | ---- | -----------
```button_data``` | InlineButtonData | Объект, из которого будет создаётся кнопка. <br>_См. подробное объяснение ниже._
```front_marker``` | CallbackDataMarker | _Опционально_. Объект, который будет добавлен к **левой** стороне колбека.
```back_marker``` | CallbackDataMarker | _Опционально_. Объект, который будет добавлен к **правой** стороне колбека.
```copy_text_to_callback``` | Boolean | Если значение ```True```, и ```button_data``` является ```str``` или ```int```, функция скопирует текст кнопки в данные колбека (и добавит другие маркеры, если они имеются).<br>Значение по умолчанию - ```False```.

Все допустимые виды объединяются в типе ```InlineButtonData```:
```python
InlineButtonData = Union[str, int, tuple, dict, InlineKeyboardButton]
```
Так же есть вид ```CallbackDataMarker``` для данных колбека:
```python
CallbackDataMarker = Optional[Union[str, int]]
```

Для объекта ```button_data``` --
* Если это ```str``` или ```int```, то они будут использованы для текста (и колбека если ```copy_text_to_callback``` не отключён).
* Если это ```tuple```, нулевой элемент [0] будет текстом и единица [1] будет колбеком. 
* Если это  ```dict```, то возникает две опции:
   * если в словаре **нет клавиши "текст"** и существует только одна клавиша, то в таком случае, клавиша будет текстом, а значение будет колбеком.<br>В таком случае проверка содержимого словаря произведена не будет!
  * Если **"текст" клавиша существует**, то функция передаёт весь словарь в ```InlineKeyboardButton```, где клавиши словаря предоставляет параметры объекта, а значение словаря соответствует значение параметров.
Во всех остальных случаях будет выдана ошибка ```ValueError```.

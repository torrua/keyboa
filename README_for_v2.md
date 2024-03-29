# Keyboa
[![Download Keyboa](https://img.shields.io/pypi/v/keyboa.svg)](https://pypi.python.org/pypi/keyboa)
![PyPI - Downloads](https://img.shields.io/pypi/dm/keyboa?color=yellow&logo=pypi&logoColor=yellow)
[![Build Status](https://travis-ci.com/torrua/keyboa.svg?branch=master)](https://travis-ci.com/torrua/keyboa)
![CodeQL](https://github.com/torrua/keyboa/workflows/CodeQL/badge.svg?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/torrua/keyboa/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/torrua/keyboa/?branch=master)
[![codecov](https://codecov.io/gh/torrua/keyboa/branch/master/graph/badge.svg?token=H4MO1Y3DDY)](https://codecov.io/gh/torrua/keyboa)
[![GitHub license](https://img.shields.io/github/license/torrua/keyboa)](https://github.com/torrua/keyboa/blob/master/LICENSE)

This is a simple but flexible inline keyboard generator that works as an add-on to PyTelegramBotAPI package. With **keyboa** you can:
- quickly create buttons with complex callback, 
- create keyboards directly from lists,
- easily combine multiple keyboards into one,
- many other cool things...

# How it works
## Installation
Keyboa is compatible with Python 3.5 and higher. You can install this package with pip as usual:
```sh
$ pip install keyboa
```
After that, just import the necessary functions:
```python
from keyboa import button_maker, keyboa_maker, keyboa_combiner
```

## Usage
There are **three main functions** which return ```InlineKeyboardButton``` or ```InlineKeyboardMarkup``` objects as a result:
- ```button_maker()``` returns ```InlineKeyboardButton```
- ```keyboa_maker()``` returns ```InlineKeyboardMarkup```
- ```keyboa_combiner()``` returns ```InlineKeyboardMarkup```

Let's take it in detail.
### How to create Button
💡 There is usually no need to create separate buttons as they will be created automatically from their source data when the keyboard is created.
But if there is such a need, it can be done as follows.

The ```button_maker()``` function creates an ```InlineKeyboardButton``` object from various data types, such as ```str```, ```int```, ```tuple```, ```dict```. You can also pass the ```InlineKeyboardButton``` object itself, which will return unchanged.

All acceptable types combined into ```InlineButtonData``` type:
```python
InlineButtonData = Union[str, int, tuple, dict, InlineKeyboardButton]
```
Also there is a ```CallbackDataMarker``` type for callback data:
```python
CallbackDataMarker = Optional[Union[str, int]]
```
The function has following input parameters:

Parameter | Type | Description
--------- | ---- | -----------
```button_data``` | InlineButtonData | An object from which the button will be created.<br>_See detailed explanation below._
```front_marker``` | CallbackDataMarker | _Optional_. An object to be added to the **left** side of callback.
```back_marker``` | CallbackDataMarker | _Optional_. An object to be added to the **right** side of callback.
```copy_text_to_callback``` | Boolean | If ```True```, and ```button_data``` is a ```str``` or an ```int```, function will copy button text to callback data (and add other markers if they exist).<br>The default value is ```False```.

For ```button_data``` object --
* If it is a ```str``` or an ```int```, it will be used for text (and callback, if ```copy_text_to_callback``` enabled).
* If it is a ```tuple```, the zero element [0] will be the text, and the first [1] will be the callback. 
* If it is a ```dict```, there are two options:
   * if there is **no "text" key** in dictionary and only one key exists, the key will be the text, and the value will be the callback.<br>In this case no verification of the dictionary's contents is performed!
  * if the **"text" key exists**, function passes the whole dictionary to ```InlineKeyboardButton```, where dictionary's keys represent object's parameters and dictionary's values represent parameters' values accordingly.
In all other cases the ```ValueError``` will be raised.

Let's look at a few examples:

#### button from ```str``` or ```int```
```python
spam = button_maker(button_data="spam", copy_text_to_callback=True)
```
```python
spam = button_maker(button_data="spam", front_marker="spam")
```
```python
spam = button_maker(button_data="spam", front_marker="sp", back_marker="am")
```
In all examples above the ```spam``` variable will contain an ```InlineKeyboardButton``` object with the following data:
```sh
{'text': 'spam', 'callback_data': 'spam'}
```
❗ You cannot use this method with ```copy_text_to_callback``` disabled and unfilled both ```front_marker``` and ```back_marker```, because callback_data cannot be empty:

```python
spam = button_maker(button_data="spam")
```
```sh
ValueError: The callback data cannot be empty.
```

#### button from ```tuple```
```python
spam = button_maker(button_data=("spam", "eggs"), front_marker="ham_", back_marker="_spam")
```
```sh
{'text': 'spam', 'callback_data': 'ham_eggs_spam'}
```
💡 Notice that in this example we also used ```front_marker``` and ```back_marker``` to add some data to button's callback_data.

#### button from ```dict``` without "text" key
```python
spam = button_maker(button_data={"spam": "ham_eggs_spam"})
```
```sh
{'text': 'spam', 'callback_data': 'ham_eggs_spam'}
```

#### button from ```dict``` with "text" key
```python
spam = button_maker(button_data={"text": "spam", "url": "https://ya.ru/", "callback_data": "eggs"})
```
```sh
{"text": "spam", "url": "https://ya.ru/", "callback_data": "eggs"}
```

### How to create Keyboard
The ```keyboa_maker()``` function creates an ```InlineKeyboardMarkup``` object from a list of ```BlockItems``` elements. A shot explanation of this type is given below:
```python
# structureless sequence of InlineButtonData objects
FlatSequence = List[InlineButtonData]

# structured sequence of InlineButtonData objects
StructuredSequence = List[Union[FlatSequence, InlineButtonData]]

# unified type that allows you to use any available data types for the keyboard
BlockItems = Union[StructuredSequence, InlineButtonData]
```
The function has following input parameters:

Parameter | Type | Description
--------- | ---- | -----------
```items``` | BlockItems | _Optional_.
```front_marker``` | CallbackDataMarker | _Optional_. Front part of callback data, which is common for all buttons.
```back_marker``` | CallbackDataMarker | _Optional_. Back part of callback data, which is common for all buttons.
```items_in_row``` | Integer | _Optional_. The number of buttons in one keyboard row. Must be **from one to eight** due to the Telegram Bot API limitation.<br>The default value is ```None```, which means that by default the keyboard structure depends on the grouping of  ```items``` elements.
```auto_alignment``` | Boolean or Iterable | If ```True```, will try to split all items into **equal rows in a range of 3 to 5**.<br>If ```Iterable``` (with any ```int``` in the range from 1 to 8), will try to use it.<br>This enabled option replaces the action of ```items_in_row``` variable, but if a suitable divisor cannot be found, function will use the ```items_in_row``` value.<br>The default value is ```False```.
```reverse_alignment_range``` | Boolean | If ```True```, will try to find the divisor starting from the end of the ```auto_alignment``` variable (if defined) or from the default range.<br>This enabled option works only if ```auto_alignment``` is enabled.<br>The default value is ```False```.
```slice_start``` | Integer | _Optional_. Refers to the index of the element which is used as a start of the slice, i.e defines **start** position in ```[start:stop:step]``` range.
```slice_stop``` | Integer | _Optional_. Refers to the index of the element we should stop just before to finish slice, i.e defines **stop** position in ```[start:stop:step]``` range.
```slice_step``` | Integer | _Optional_. It allows you to take each nth-element within range, i.e defines **step** position in ```[start:stop:step]``` range.
```copy_text_to_callback``` | Boolean | If ```True```, and ```button_data``` is a ```str``` or an ```int```, function will copy button text to callback data (and add other markers if they exist).<br>The default value is ```False```.
```add_to_keyboard``` | InlineKeyboardMarkup | _Optional_. You may pass the keyboard to which the specified items will be added.

Let's start with a simple example!
#### keyboard from ```list``` of ```str```
The easiest way to create a keyboard is to pass a list of items to a function.
```python
menu = ["spam", "eggs", "ham"]
keyboard = keyboa_maker(items=menu, copy_text_to_callback=True)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
```
![keyboard from list of str](https://telegra.ph/file/d9280b11ed11ec13e6f56.png)

By default, each item in the list becomes a separate row, but it's easy to change by combining the items into groups.
```python
menu = [["spam", "eggs"], ["ham", "bread"], "spam"]
keyboard = keyboa_maker(items=menu, copy_text_to_callback=True)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
```
![keyboard from list of str](https://telegra.ph/file/2eb6752324fa196cae4ac.png)

Now you see that the keyboard buttons are arranged according to how we grouped them in the list. 
And of course you can create more complex structures, for example:
```python
menu = [["spam", "eggs", "ham"], ["ham", "eggs"], "spam", ["sausages", "spam"], ["eggs", "spam", "spam"]]
keyboard = keyboa_maker(items=menu, copy_text_to_callback=True)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
```
![keyboard from list of str](https://telegra.ph/file/faff37512c626845c5524.png)

>Due to Telegram API limitation you can add **up to 8 buttons per row** and **up to 100 for the entire keyboard**.

Let's go deeper. Suppose you have a list of 24 items, and you would like to divide it into rows of 6 buttons each. Here is what you need to do:
```python
numbers = list(range(1, 25))
keyboard = keyboa_maker(items=numbers, items_in_row=6, copy_text_to_callback=True)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
```
![keyboard with 6 items_in_row](https://telegra.ph/file/2122cb9f50938b39b4439.png)

💡 You can easily make 3, 4 or even 8 buttons in a row, changing the ```items_in_row``` parameter only.

Now we will try to use more parameters to see how they will affect the result:
```python
keyboard = keyboa_maker(
    items=list(range(0, 48)),
    auto_alignment=True,
    slice_start=5,
    slice_stop=37,
    copy_text_to_callback=True
)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
```
![keyboard slice with auto_alignment](https://telegra.ph/file/cc41513058a2b3d9f83ba.png)

As you can see, this keyboard consists of a ```[5:37]``` slice. In addition, although we did not specify the ```items_in_row``` parameter, the function divided list into equal rows, because of enabled ```auto_alignment``` parameter.

### Combine Keyboards
Sometimes it is necessary to combine several separate keyboard blocks  into the big one. The ```keyboa_combiner()``` function does just that!

The function has only one input parameter - ```keyboards```. It should be a sequence of ```InlineKeyboardMarkup``` objects. Also could be presented as a standalone ```InlineKeyboardMarkup```.

Here is how it works:
```python
controls = [["⏹️", "⏪️", "⏏️", "⏩️", "▶️"], ]
tracks = list(range(1, 13))

keyboard_controls = keyboa_maker(items=controls, copy_text_to_callback=True)
keyboard_tracks = keyboa_maker(items=tracks, items_in_row=4, copy_text_to_callback=True)

keyboard = keyboa_combiner(keyboards=(keyboard_tracks, keyboard_controls))
bot.send_message(chat_id=user_id, text=text_tracks, reply_markup=keyboard)
```
![keyboard combo](https://telegra.ph/file/342c06d783faeb786f242.png)

As you see, we merged two keyboards into one.

### Complex callbacks
A few words about how to create complex callbacks for buttons. 

Often it is necessary to read and pass through the callback options that the user has sequentially selected. For example, determining the address: city, street, house, apartment number.

Suppose we offer the user several cities to choose from. Create a simple keyboard:
```python
kb_cities = keyboa_maker(
    items=["Moscow", "London", "Tokyo", ],
    copy_text_to_callback=True,
    front_marker="&city=",
    back_marker="$"
)
bot.send_message(chat_id=user_id, text="Select your city:", reply_markup=kb_cities)
```
![keyboard cities](https://telegra.ph/file/dcd011c72e43aefd8d00d.png)

By doing so, we get the following inside the keyboard:
```sh
{'inline_keyboard': [
    [{'text': 'Moscow', 'callback_data': '&city=Moscow$'}],
    [{'text': 'London', 'callback_data': '&city=London$'}],
    [{'text': 'Tokyo', 'callback_data': '&city=Tokyo$'}]
]}
```
Suppose a user selects ```London```. We would like to remember this, and let him choose from several streets:
```python
received_callback = call.data  # "&city=London$"
streets = ["Baker Street", "Oxford Street", "Abbey Road", ]
kb_streets = keyboa_maker(
    items=streets, 
    copy_text_to_callback=True, 
    front_marker="&street=", 
    back_marker=received_callback)  # we added existing data to the end
bot.send_message(chat_id=user_id, text="Select your street:", reply_markup=kb_streets)
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
💡 Notice that we used a ```front_marker``` to specify the type of current items, and a ```back_marker``` to attach existing information.

As you can see, the variant selected by the user in the previous step was also saved.
If the user selects a street, for example, ```Baker Street```, we will receive the ```call.data``` as ```'&street=Baker Street&city=London$'```. Of course we are able to parse it easily.

Finally, let him to choose an apartment:
```python
received_callback = call.data  # '&street=Baker Street&city=London$'
apartments = ["221a", "221b", "221c", ]
kb_apartments = keyboa_maker(
    items=apartments, 
    copy_text_to_callback=True, 
    front_marker="&apartments=", 
    back_marker=received_callback)  # we added existing data to the end
bot.send_message(chat_id=user_id, text="Select your apartments:", reply_markup=kb_apartments)
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
And if the user selects button ```221b```, we will assume that 🕵🏻‍♂️ Mr. Sherlock Holmes uses our bot too!

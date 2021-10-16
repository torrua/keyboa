# Keyboa
[![Download Keyboa](https://img.shields.io/pypi/v/keyboa.svg)](https://pypi.python.org/pypi/keyboa)
![PyPI - Downloads](https://img.shields.io/pypi/dm/keyboa?color=yellow&logo=pypi&logoColor=yellow)
[![Build Status](https://travis-ci.com/torrua/keyboa.svg?branch=master)](https://travis-ci.com/torrua/keyboa)
![CodeQL](https://github.com/torrua/keyboa/workflows/CodeQL/badge.svg?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/torrua/keyboa/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/torrua/keyboa/?branch=master)
[![codecov](https://codecov.io/gh/torrua/keyboa/branch/master/graph/badge.svg?token=H4MO1Y3DDY)](https://codecov.io/gh/torrua/keyboa)
[![GitHub license](https://img.shields.io/github/license/torrua/keyboa)](https://github.com/torrua/keyboa/blob/master/LICENSE)

Este es un generador de teclado en línea simple pero flexible que funciona como un complemento del paquete PyTelegramBotAPI. Con **keyboa** puedes:
- crear botones rápidamente con callbacks complejos,
- crear teclados directamente desde listas,
- combinar fácilmente varios teclados en uno,
- muchas otras cosas interesantes ...


> 📖 Esta guía se aplica a la versión 3 del teclado o superiores.
> Si está utilizando la versión 2 del teclado o una inferior, por favor utilice [The guide for version 2](README_for_v2.md).

> 📌 **NOTICIA IMPORTANTE**: 
> 
> La versión 3 no es compatible con la versión 2.
> Si decide actualizar de la versión 2 a la 3, tenga en cuenta que deberá ajustar su código.

## Instalación
Keyboa es compatible con Python 3.7 y superior. Puede instalar este paquete con pip como de costumbre:
```sh
$ pip install keyboa
```
Después de eso, importamos:
```python
from keyboa import Keyboa
```

## Inicio Rápido
### Teclado básico
El teclado para telegram más sencillo, se puede crear así:
```python
menu = ["spam", "eggs", "ham"]
keyboard = Keyboa(items=menu)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard())
```
![keyboard from list of str](https://telegra.ph/file/d9280b11ed11ec13e6f56.png)

### Teclado estructurado simple
Si necesita crear un teclado con una estructura predefinida, haga lo siguiente:
```python
menu = [["spam", "eggs"], ["ham", "bread"], "spam"]
keyboard = Keyboa(items=menu)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard())
```
![keyboard from list of str](https://telegra.ph/file/2eb6752324fa196cae4ac.png)

Este es un buen comienzo, pero echemos un vistazo con mayor detalle a cómo funciona y qué características adicionales podemos usar.

## Cómo funciona

La clase ```Keyboa``` proporciona dos opciones para crear teclados compatilbes con pyTelegramBotAPI a través del tipo ```InlineKeyboardMarkup``` : método ```slice()``` y la propiedad ```keyboard```.
Utilice a continuación,la descripción de la [Keyboa class](#keyboa-class). Como referencia para comprender los matices y las limitaciones del módulo o observe los siguientes ejemplos.

## Crear teclados
La forma más sencilla de crear un teclado es iniciar el objeto Keyboa con una lista de elementos y obtener la propiedad ```keyboard```.
```python
menu = ["spam", "eggs", "ham"]
keyboard = Keyboa(items=menu)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard())
```
![keyboard from list of str](https://telegra.ph/file/d9280b11ed11ec13e6f56.png)

Por defecto, cada elemento de la lista se convierte en una fila separada, pero es fácil de cambiar al combinar los elementos en grupos.
```python
menu = [["spam", "eggs"], ["ham", "bread"], "spam"]
keyboard = Keyboa(items=menu)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard())
```
![keyboard from list of str](https://telegra.ph/file/2eb6752324fa196cae4ac.png)

Puedes ver que, los botones del teclado están ordenados en función a cómo los agrupamos en la lista. 

Fíjese en que el último "spam" se ha convertido en una fila separada, aunque no lo hemos incluido en una lista separada.

Y, por supuesto, usted puede crear estructuras más complejas si lo desea, por ejemplo:
```python
menu = [["spam", "eggs", "ham"], ["ham", "eggs"], ["spam", ] ["sausages", "spam"], ["eggs", "spam", "spam"]]
keyboard = Keyboa(items=menu)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard())
```
![keyboard from list of str](https://telegra.ph/file/faff37512c626845c5524.png)

>Debido a las limitaciones de la API Telegram, puede agregar **hasta 8 botones por fila** y **hasta 100 para todo el teclado**.

Profundicemos. Suponga que tiene una lista de 24 elementos, y le gustaría dividirla en filas de 6 botones cada una. Debería realizar lo siguiente:
```python
numbers = list(range(1, 25))
keyboard = Keyboa(items=numbers, items_in_row=6)
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard())
```
![keyboard with 6 items_in_row](https://telegra.ph/file/2122cb9f50938b39b4439.png)

💡 Puede crear fácilmente 3, 4 o incluso 8 botones sseguidos, cambiando únicamente el parámetro ```items_in_row```.

Ahora intentaremos usar más atributos para ver cómo afectarán el resultado:
```python
keyboa = Keyboa(items=list(range(0, 48)), alignment=True)
keyboard = keyboa(slice(5, 37))
bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
```
![keyboard slice with alignment](https://telegra.ph/file/cc41513058a2b3d9f83ba.png)

Como puede ver, este teclado consta de un segmento ```[5:37]```. Además, aunque no especificamos el atributo ```items_in_row```, la función dividió la lista en filas iguales, debido al atributo ```alignment```.

## Crear Botones
💡 Por lo general, no es necesario crear botones separados, ya que estos se crearán automáticamente a partir de sus datos de origen cuando se crea el teclado.
Pero en caso de necesitarlo, se puede hacer de la siguiente manera.
Import ```Button``` class ([detailed description](#button-class)), create button object from various data types, such as ```str```, ```int```, ```tuple```, ```dict``` and call ```button``` property to get ```InlineKeyboardButton```:
```python
from keyboa import Button
spam = Button(button_data="spam").button
```

#### botón de ```str``` o ```int```
```python
spam = Button(button_data="spam").button
```
```sh
{'text': 'spam', 'callback_data': 'spam'}
```

#### botón de ```tuple```
```python
spam = Button(button_data=("spam", "eggs"), front_marker="ham_", back_marker="_spam").button
```
```sh
{'text': 'spam', 'callback_data': 'ham_eggs_spam'}
```
💡 Observe que, en este ejemplo también usamos ```front_marker``` y ```back_marker``` para añadir algunos datos al callback_data del botón.

#### botón de ```dict``` sin la tecla "text" 
```python
spam = Button(button_data={"spam": "ham_eggs_spam"}).button
```
```sh
{'text': 'spam', 'callback_data': 'ham_eggs_spam'}
```

#### botón de ```dict``` con la tecla "text" 
```python
spam = Button(button_data={"text": "spam", "url": "https://ya.ru/", "callback_data": "eggs"}).button
```
```sh
{"text": "spam", "url": "https://ya.ru/", "callback_data": "eggs"}
```

## Combinar Teclados
A veces es necesario combinar varios bloques de teclado en uno. ¡El método de la clase Keyboa ```combine()``` hace precisamente eso!

Este método tiene un solo parámetro de entrada - ```keyboards```. Debe ser una secuencia de objetos ```InlineKeyboardMarkup```. También podría presentarse como un único ```InlineKeyboardMarkup```.

Así es como funciona:
```python
controls = [["⏹️", "⏪️", "⏏️", "⏩️", "▶️"], ]
tracks = list(range(1, 13))

keyboard_controls = Keyboa(items=controls).keyboard
keyboard_tracks = Keyboa(items=tracks, items_in_row=4).keyboard

keyboard = Keyboa.combine(keyboards=(keyboard_tracks, keyboard_controls))
bot.send_message(chat_id=user_id, text=text_tracks, reply_markup=keyboard)
```
![keyboard combo](https://telegra.ph/file/342c06d783faeb786f242.png)

Como puede ver, fusionamos los dos teclados en uno.

## Callbacks complejos
Algunas nociones sobre cómo crear callbacks complejos para botones. 

A menudo es necesario leer y pasar por las opciones de callback que el usuario ha seleccionado secuencialmente. Por ejemplo, determinar la dirección: ciudad, calle, casa, número de apartamento.

Supongamos que ofrecemos al usuario varias ciudades para elegir. Crear un teclado simple:
```python
kb_cities = Keyboa(
    items=["Moscow", "London", "Tokyo", ],
    front_marker="&city=",
    back_marker="$"
)
bot.send_message(chat_id=user_id, text="Select your city:", reply_markup=kb_cities())
```
![keyboard cities](https://telegra.ph/file/dcd011c72e43aefd8d00d.png)

Al hacerlo, obtenemos lo siguiente dentro del teclado:
```sh
{'inline_keyboard': [
    [{'text': 'Moscow', 'callback_data': '&city=Moscow$'}],
    [{'text': 'London', 'callback_data': '&city=London$'}],
    [{'text': 'Tokyo', 'callback_data': '&city=Tokyo$'}]
]}
```
Suponga que un usuario selecciona ```London```. Nos gustaría recordar este dato y dejarle elegir entre varias calles:
```python
received_callback = call.data  # "&city=London$"
streets = ["Baker Street", "Oxford Street", "Abbey Road", ]
kb_streets = Keyboa(
    items=streets, 
    front_marker="&street=",
    back_marker=received_callback  # añadimos datos existentes al final
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
💡 Observe que usamos un ```front_marker``` para especificar el tipo de los elementos actuales, y un ```back_marker``` para adjuntar información existente.

Como puede ver, la variante seleccionada por el usuario en el paso anterior también ha sido guardada.
Si el usuario selecciona una calle, por ejemplo, ```Baker Street```, recibiremos el ```call.data``` como ```'&street=Baker Street&city=London$'```. Por supuesto podemos parsearlo fácilmente.

Finalmente, deje que seleccione un apartamento:
```python
received_callback = call.data  # '&street=Baker Street&city=London$'
apartments = ["221a", "221b", "221c", ]
kb_apartments = Keyboa(
    items=apartments, 
    front_marker="&apartments=", 
    back_marker=received_callback  # añadimos datos existentes al final
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
Y si el usuario selecciona el botón ```221b```, asumiremos que ¡🕵🏻‍♂️ Mr. Sherlock Holmes también usa nuestro bot!

## Detalles
### Clase Keyboa
Atributo | Tipo | Descripcción
--------- | ---- | -----------
```items``` | BlockItems | _Obligatorio_. Lista de elementos para el teclado. El número total no debe ser superior a 100 debido a la limitación de la API de Telegram Bot.
```items_in_row``` | Integer | _Opcional_. El número de botones en una fila de teclado. Deber ser **de 1 a 8** debido a la limitación de la API de Telegram Bot.<br>El valor por defecto es ```None```, lo que significa que de manera predeterminada la estructura del teclado depende de la agrupación de los elementos  ```items```.
```copy_text_to_callback``` | Boolean | Si es ```True```, y ```button_data``` es un ```str``` o un ```int```, la función copiará el texto del botón al callback data (y agregará otros marcadores en caso de que existan).<br>El valor por defecto es ```True```.
```front_marker``` | CallbackDataMarker | _Opcional_. Parte frontal del callback data, que es común para todos los botones.
```back_marker``` | CallbackDataMarker | _Opcional_. Parte posterior del callback data, que es común para todos los botones.
```alignment``` | Boolean or Iterable | Si es ```True```, intentará dividir todos los elementos en **filas iguales en un rango de 3 a 5**.<br>Si es ```Iterable``` (con cualquier ```int``` en un rango de 1 a 8), intentará encontrar un divisor adecuado entre ellos.<br><br>El atributo habilitado reemplaza la acción del atributo ```items_in_row```, pero si no se puede encontrar un divisor adecuado, la función usará si se proporciona el valor ```items_in_row```.<br><br>El valor por defecto es ```None```.
```alignment_reverse``` | Boolean | Si es ```True```, intentará encontrar el divisor empezando por el final de la variable ```auto_alignment``` (si está definida) o desde el rango predeterminado.<br><br>El atributo habilitado solo funciona si ```auto_alignment``` está habilitado.<br><br>El valor por defecto es ```None```.

```python
# secuencia sin estructura de objetos InlineButtonData
FlatSequence = List[InlineButtonData]

# secuencia estructurada de objetos InlineButtonData
StructuredSequence = List[Union[FlatSequence, InlineButtonData]]

# tipo unificado que le permite utilizar cualquier tipo de dato disponible para el teclado
BlockItems = Union[StructuredSequence, InlineButtonData]
```

### Clase button
Atributo | Tipo | Descripcción
--------- | ---- | -----------
```button_data``` | InlineButtonData | Un objeto a partir del cual se creará el botón.<br>_Consulte la explicación detallada a continuación._
```front_marker``` | CallbackDataMarker | _Opcional_. Un objeto que se agregará al lado **izquierdo** del callback.
```back_marker``` | CallbackDataMarker | _Opcional_. Un objeto que se agregará al lado **derecho** del callback.
```copy_text_to_callback``` | Boolean | Si es ```True```, y ```button_data``` es un ```str``` o un ```int```, la función copiará el texto del botón al callback data (y agregará otros marcadores en caso de que existan).<br>El valor por defecto es ```False```.

Todos los tipos aceptables se combinan en el tipo ```InlineButtonData```:
```python
InlineButtonData = Union[str, int, tuple, dict, InlineKeyboardButton]
```
También hay un tipo ```CallbackDataMarker``` para los callback data:
```python
CallbackDataMarker = Optional[Union[str, int]]
```

Para el objeto ```button_data```  --
* Si es un ```str``` o un ```int```, se usará para texto (y callback, si ```copy_text_to_callback``` no está deshabilitado).
* Si es un ```tuple```, el elemento cero [0] será el texto, y el primero [1] será el callback. 
* Si es un ```dict```, hay dos opciones:
   * Si **no hay clave "text"** en el diccionario y solo existe una clave, la clave será el texto, y el valor será el callback.<br>En este caso, ¡no se realiza ninguna verificación del contenido del diccionario!
  * Si **hay clave "text"**, la función pasa todo el diccionario a ```InlineKeyboardButton```, donde las claves del diccionario representan los parámetros del objeto y los valores del diccionario en consencuencia representan los valores de los parámetros.
En todos los demás casos se generará un ```ValueError```.

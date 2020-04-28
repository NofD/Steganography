"""Реализация метода стеганографии LSB.
   Применимо для файлов в формате .bmp с глубиной цвета 24.
"""
import os
import sys

def mode_choice():
    """Выбор режима.
    """
    mode = input("\nВыберите режим: \n\t1 - Поместить сообщение в стегоконтейнер\n\t2 - Извлечь сообщение\n\t3 - Выход\n")
    if mode.isdigit():
        if int(mode) == 1:
            put_mess()
        elif int(mode) == 2:
            extract_mess()
        elif int(mode) == 3:
            quit()
        else:
            print("\nНеправильная команда")
            mode_choice()
    else:
        print("\nНеправильная команда")
        mode_choice()

def str_to_bit(text, encoding='utf-8', errors='surrogatepass'):
    """Переводит символьую строку в битовую.
    """
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bit_to_str(bits, encoding='utf-8', errors='surrogatepass'):
    """Переводит битовую строку в символьную.
    """
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def code_message():
    """Принимает сообщение, которое нужно поместить в контейнер
       и переводит его в двоичную последовательность. 
    """
    mess = input("\nВведите сообщение: ")
    if mess:
        return str_to_bit(mess)
    else:
        return code_message()

def input_file():
    """Запрашивает имя файла, который является исходным контейнером.
       Проверяет, существует ли файл.
    """
    file_name = input("\nВведите имя файла-контейнера (в формате name.bmp, по умолчанию: grey.bmp): ")
    if file_name:
        try:
            open(file_name)
        except IOError:
            print("\nНе удалось открыть файл")
            return input_file()
        else:
            return file_name
    else:
        try:
            open("grey.bmp")
        except IOError:
            print("\nНе удалось открыть файл")
            return input_file()
        else:
            return "grey.bmp"       

def container_file():
    """Запрашивает имя файла, который нужно проанализировать.
       Проверяет, существует ли файл.
    """
    file_name = input("\nВведите имя файла для анализа (в формате name.bmp, по умолчанию: result.bmp): ")
    if file_name:
        try:
            open(file_name)
        except IOError:
            print("\nНе удалось открыть файл")
            return container_file()
        else:
            return file_name
    else:
        try:
            open("result.bmp")
        except IOError:
            print("\nНе удалось открыть файл")
            return container_file()
        else:
            return "result.bmp"
        
def encode_message(text_in_bytes):
    """Принимает двоичную строку, которую получили из файла,
       переводит ее в символьную и выводит результат в message.txt. 
    """
    with open('message.txt', 'w') as ouf:
        if text_in_bytes:
            ouf.write(bit_to_str(text_in_bytes))
            print("\nУспешно")
        else:
            print("\nСообщения нет")

def put_mess():
    """Сокрытие сообщения.

       Помещает сообщение в контейнер одним из трех методов.
       Результат записывает в файл result.bmp.
    """
    file_name = input_file()
    bit_mess = code_message() # сообщение в двоичном виде
    
    file_size = os.path.getsize(file_name) # размер изображения в байтах
    mess_size = (len(bit_mess)/8) # размер сообщения в байтах
    if (file_size - 54 - 8)/8 <= mess_size: # 54 байта - заголовок файла, 8 байт - отступ для правильного извлечения сообщения.
        print("\nСлишком большое сообщение.")
        return

    start = open(file_name, 'rb')
    res = open('result.bmp', 'wb') # открываем файлы

    bmp_info = start.read(54) # копируем в новый файл заголовки файла и изображения
    res.write(bmp_info)

    counter = len(bit_mess)

    while counter:
        bits = bin(int.from_bytes(start.read(1), sys.byteorder))[2:] # переводим байт в двоичный вид 
        new = (int((bits[:-1] + bit_mess[len(bit_mess) - counter]), 2)).to_bytes(1, sys.byteorder)
        res.write(new)
        counter -= 1
    
    for j in range(8):
        bits = bin(int.from_bytes(start.read(1), sys.byteorder))[2:] # переводим байт в двоичный вид 
        new = (int((bits[:-1] + "0"), 2)).to_bytes(1, sys.byteorder)
        res.write(new)

    res.write(start.read()) # записываем оставшиеся байты

    start.close()
    res.close()   # закрываем файлы

    print("\nФайл 'result.bmp' создан")

def extract_mess():
    """Извлечение сообщения.

       Анализирует текст на наличие скрытых сообщений.
       Сообщение записывает в файл message.txt.
       Если сообщение не найдено, выводит "Сообщение не найдено".
    """
    # принимает имя файла, если сообщения не найдено, то выводит "сообщения нет"
    container_name = container_file()

    
    new_substr = ""
    mess_string = ""
    container = open(container_name, 'rb') # открываем файл 
    container.seek(54) # пропускаем заголовок файла

    while True:
        for i in range(8):
            byte = bin(int.from_bytes(container.read(1), sys.byteorder))[2:] # читаем переводим байт в двоичный вид
            new_substr += byte[-1]
        if new_substr != ("00000000" or "11111111"):
            mess_string += new_substr
            new_substr = ""
        else:
            break
    else:
        print("\nКонец файла")
    
    container.close()
    message = open('message.txt', 'w')

    if mess_string:
        try:
            bit_to_str(mess_string)
        except:
            message.write("Сообщение не найдено.")
            print("\nСообщение не найдено")
        else:
            mess_string = bit_to_str(mess_string)
            message.write("Сообщение: ")
            message.write(mess_string)
            print("\nФайл 'message.txt' создан")
    else:
        message.write("Сообщение не найдено.")
        print("\nСообщение не найдено")
    
    message.close()   

#Основное исполнение
mode_choice()
input("\nНажмите Enter для выхода...")
"""Реализация трех методов текстовой стеганографии.
"""

def mode_choice():
    """Выбор режима.
    """
    mode = input("\nВыберите режим: \n\t1 - Поместить сообщение в стегоконтейнер\n\t2 - Извлечь сообщение\n\t3 - Выход\n")
    if mode.isdigit():
        if int(mode) == 1:
            encrypt()
        elif int(mode) == 2:
            decrypt()
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
    file_name = input("\nВведите имя файла-контейнера (в формате name.txt, по умолчанию: Fahrenheit.txt): ")
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
            open("Fahrenheit.txt")
        except IOError:
            print("\nНе удалось открыть файл")
            return input_file()
        else:
            return "Fahrenheit.txt"       

def container_file():
    """Запрашивает имя файла, который нужно проанализировать.
       Проверяет, существует ли файл.
    """
    file_name = input("\nВведите имя файла для анализа (в формате name.txt, по умолчанию: result.txt): ")
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
            open("result.txt")
        except IOError:
            print("\nНе удалось открыть файл")
            return container_file()
        else:
            return "result.txt"
        
def encode_message(text_in_bytes):
    """Принимает двоичную строку, которую получили из файла,
       переводит ее в символьную и выводит результат в message.txt. 
    """
    with open('message.txt', 'w') as ouf:
        if text_in_bytes:
            ouf.write(bit_to_str(text_in_bytes))
            print("Успешно")
        else:
            print("\nСообщения нет")

def symbol_replacement():
    """Реализация метода замены символа.

       'e' - en = 1
       'е' - ru = 0
    """
    bit_mess = code_message()
    file_name = input_file()
    new_string = ""
    counter = len(bit_mess)
    with open(file_name, 'r', encoding='utf-8') as container:
        with open('result.txt', 'w',  encoding='utf-8') as result:
            for line in container:
                for sym in line:
                    if counter:
                        if sym == "e"  or sym == "е": #нужная для замены буква
                            if bit_mess[0] == '0':
                                new_string += 'е'
                                bit_mess = bit_mess[1:]
                                counter -= 1
                            else:
                                new_string += 'e'
                                bit_mess = bit_mess[1:]
                                counter -= 1
                        else:                       #другая буква
                            new_string += sym   
                    else: #что делаем если бит уже кодировать не надо
                        if sym == "—":
                            new_string += "-"                
                        else:
                            new_string += sym

                result.write(new_string)
                new_string = ""
    print("\nУспешно\n")
   
def additional_spaces():
    """Реализация метода добавления дополнительных пробелов.

       '1_' = 0
       '2_' = 1
    """
    bit_mess = code_message()
    file_name = input_file()
    new_string = ""
    counter = len(bit_mess)
    with open(file_name, 'r', encoding='utf-8') as container:
        with open('result.txt', 'w',  encoding='utf-8') as result:
            for line in container:
                for sym in line:
                    if counter:
                        if sym == " ": # если нашелся пробел
                            if bit_mess[0] == '0':
                                new_string += ' '
                                bit_mess = bit_mess[1:]
                                counter -= 1
                            else:
                                new_string += '  '
                                bit_mess = bit_mess[1:]
                                counter -= 1
                        else:                       #не пробел
                            new_string += sym   
                    else: #что делаем если бит уже кодировать не надо
                        if sym == "—":
                            new_string += "-"                
                        else:
                            new_string += sym
                result.write(new_string)
                new_string = ""
    print("\nУспешно\n")

def special_symbols():
    """Реализация метода добавления специальных символов.

       '—' = 1
       '-' = 0
    """
    bit_mess = code_message()
    file_name = input_file()
    new_string = ""
    counter = len(bit_mess)
    with open(file_name, 'r', encoding='utf-8') as container:
        with open('result.txt', 'w',  encoding='utf-8') as result:
            for line in container:
                for sym in line:
                    if counter:
                        if sym == "-" or sym == "—": # если нашелся нужный знак
                            if bit_mess[0] == '0':
                                new_string += '-'
                                bit_mess = bit_mess[1:]
                                counter -= 1
                            else:
                                new_string += '—'
                                bit_mess = bit_mess[1:]
                                counter -= 1
                        else:                       #все остальные знаки
                            new_string += sym   
                    else: #что делаем если бит уже кодировать не надо
                        if sym == "—":
                            new_string += "-"                
                        else:
                            new_string += sym
                result.write(new_string)
                new_string = ""
    print("\nУспешно\n")

def de_sym_rep(container_name):
    """Ищет сообщения, скрытые методом замены символа.

       Возвращает строку, содержащюю сообщение или пустую,
       если сообщение не найдено.
    """
    mess_string = ""
    new_substr = ""
    with open(container_name, 'r', encoding='utf-8') as container:
        for line in container:
            for sym in line:
                if sym == "e":   # английская
                    new_substr += "1"
                elif sym == "е": # русская
                    new_substr += "0"
                if len(new_substr) == 8:
                    if new_substr != ("00000000" or "11111111"):
                        mess_string += new_substr
                        new_substr = ""
    if mess_string:
        try:
            bit_to_str(mess_string)
        except:
            return ""
        else:
            return bit_to_str(mess_string)
    else:
        return ""

def de_add_sp(container_name):
    """Ищет сообщения, скрытые методом добавления дополнительных пробелов.

       Возвращает строку, содержащюю сообщение или пустую,
       если сообщение не найдено.
    """
    mess_string = ""
    new_substr = ""
    previous = ""
    with open(container_name, 'r', encoding='utf-8') as container:
        for line in container:
            for sym in line:
                if sym == " " and previous == " ":
                    new_substr += "1"
                    previous = ""
                elif sym == " " and previous == "":
                    previous = " "
                elif sym != " ":
                    if previous:
                        new_substr += "0"
                        previous = ""
                if (len(new_substr) == 8):
                    if new_substr != ("00000000" or "11111111"):
                        mess_string += new_substr
                        new_substr = ""
    if mess_string:
        try:
            bit_to_str(mess_string)
        except:
            return ""
        else:
            return bit_to_str(mess_string)
    else:
        return ""

def de_spec_sym(container_name):
    """Ищет сообщения, скрытые методом специальных символов.

       Возвращает строку, содержащюю сообщение или пустую,
       если сообщение не найдено.
    """
    mess_string = ""
    new_substr = ""
    with open(container_name, 'r', encoding='utf-8') as container:
        for line in container:
            for sym in line:
                if sym == "—":
                    new_substr += "1"
                elif sym == "-":
                    new_substr += "0"
                if len(new_substr) == 8:
                    if new_substr != ("00000000" or "11111111"):
                        mess_string += new_substr
                        new_substr = ""
    if mess_string:
        try:
            bit_to_str(mess_string)
        except:
            return ""
        else:
            return bit_to_str(mess_string)
    else:
        return ""

def encrypt():
    """Сокрытие сообщения.

       Помещает сообщение в контейнер одним из трех методов.
       Результат записывает в файл result.txt.
    """
    variant = int(input("\nВыберите метод: \n\t1 - Замена символа\n\t2 - Дополнительные пробелы\n\t3 - Специальные символы\n"))
    if variant == 1:
        symbol_replacement()
    elif variant == 2:
        additional_spaces()
    elif variant == 3:
        special_symbols()
    else:
        print("\nНеправильная команда\n")
        mode_choice()

def decrypt():
    """Извлечение сообщения.

       Анализирует текст на наличие скрытых сообщений.
       Сообщение записывает в файл message.txt.
       Если сообщение не найдено, выводит "Сообщение не найдено".
    """
    # принимает имя файла и проверяет все методы на нем, если сообщения не найдено, то выводит "сообщения нет"
    container_name = container_file()

    one = de_sym_rep(container_name)
    two = de_add_sp(container_name)
    three = de_spec_sym(container_name)

    with open('message.txt', 'w',  encoding='utf-8') as message:
        if one:
            message.write(one)
            print("\nУспешно. Метод замены символа.")
        elif two:
            message.write(two)
            print("\nУспешно. Метод добавления дополнительных пробелов.")
        elif three:
            message.write(three)
            print("\nУспешно. Метод специальных символов.")
        else:
            message.write("Сообщение не найдено.\n")
            print("\nСообщение не найдено.\n")
    
#Основное исполнение
mode_choice()
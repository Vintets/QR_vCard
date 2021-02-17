#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import quopri
import pyqrcode


# error     L, M, Q, or H  level can correct up to 7, 15, 25, or 30 percent of the data respectively
ERROR_LEVEL = 'L'
VERSION = 19                        # scale QR
SCALE = 2                           # pixels per element
COLOR_TIME = [13, 58, 103, 255]     # dark blue

# подобранные по умолчанию
# error level 'L'
# version     19
# error level ENG 'M'
# version     ENG 11

def main(file_in):
    print(f'Обрабатываем файл {file_in}')
    full_in = os.path.split(file_in)
    print(f'Файл: {full_in[-1]}\n')
    path = full_in[0]
    file = os.path.splitext(full_in[-1])
    file_out_encoder = os.path.join(path, f'{file[0]}_encoder{file[1]}')

    list_line_in = reading_file(file_in)
    vcard_plain = ''.join(list_line_in)
    if 'QUOTED-PRINTABLE' in vcard_plain:
        vcard_encode_out = encode_quoted_printable(list_line_in, file_out_encoder)
    else:
        vcard_encode_out = vcard_plain

    shot_name = file[0]
    if shot_name[:6] == 'VCard_':
        shot_name = shot_name[6:]
    file_out_image = os.path.join(path, f'QR-code_{shot_name}.png')
    generate_qr_vcard(vcard_encode_out, file_out_image)
    print('Обработка закончена')

def reading_file(file_in):
    list_field = []
    with open(file_in, 'r', encoding='utf-8') as file:
        for i in file:
            list_field.append(i)
    print(f'Оригинальная vcard\n{"".join(list_field)}\n')
    return list_field

def encode_quoted_printable(list_line_in, file_out):
    list_encode = []
    for i in list_line_in:
        str_1 = quopri.encodestring(bytes(i, 'UTF-8'), 1, 0).decode('UTF-8')
        # quopri кодирует знак "=" в hex-значение "=3D", поэтому возвращаем его обратно
        str_2 = str_1.replace('=3D','=')
        list_encode.append(str_2)
    encode_out = ''.join(list_encode)
    with open(file_out, 'w', encoding='utf-8') as file:
            file.write(encode_out)
    print(f'Перекодированная vcard\n{encode_out}\n')
    return encode_out

def generate_qr_vcard(qr_data, file_out_image):
    try:
        qr = pyqrcode.create(qr_data, error=ERROR_LEVEL, version=VERSION, mode='binary')
    except ValueError as err:
        print(err)
        time.sleep(10)
        exit()
    # qr.svg('code.svg', scale=8)
    qr.png(file_out_image, scale=SCALE, module_color=COLOR_TIME, background=[0xff, 0xff, 0xff])
    # qr.show()
    # print(qr.terminal())
    # print(qr.terminal(module_color='red', background='yellow'))
    # print(qr.terminal(module_color=5, background=123, quiet_zone=1))
    pass


if __name__ == '__main__':
    _width = 100
    _hight = 50
    if sys.platform == 'win32':
        os.system('color 71')
        os.system('mode con cols=%d lines=%d' % (_width, _hight))
    main(sys.argv[1])
    # main('D:/_Work/Визитки/Заказы/QR_vCard/Test.txt')
    # main('D:/_Work/Визитки/Заказы/QR_vCard/VCard_СантехТула.vcf')
    time.sleep(5)


# --------------------------------------------------------------------------------------------------




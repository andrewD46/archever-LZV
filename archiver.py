#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import argparse
import os
import pickle

parser = argparse.ArgumentParser(description='File compression and decompression')
parser.add_argument('options', type=str, help='required function (сompress or decompress)')
parser.add_argument('file_name', type=str, help='Required file name')
args = parser.parse_args()


def compress(string):
    dict_size = 256
    dictionary = {chr(i): chr(i) for i in range(dict_size)}
    w = ""
    result = []
    for char in string:
        new_char = w + char
        if new_char in dictionary:
            w = new_char
        else:
            result.append(dictionary[w])
            dictionary[new_char] = dict_size
            dict_size += 1
            w = char
    if w:
        result.append(dictionary[w])

    return result


def decompress(compressed):
    dict_size = 256
    dictionary = {chr(i): chr(i) for i in range(dict_size)}

    w = result = compressed.pop(0)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError()
        result += entry

        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry
    return result


if args.options == 'compress':
    with open(args.file_name, 'r') as file:
        content = file.read()
        array = compress(content)
        with open(args.file_name + '.archived', 'wb') as f:
            pickle.dump(array, f)
            f.close()
        file.close()
        print('Compression successful. ' + 'Size: ' + str(os.path.getsize(args.file_name + '.archived')) + ' bytes')

elif args.options == 'decompress':
    with open(args.file_name, 'rb') as file:
        name_file = args.file_name.split('.')
        del (name_file[-1])
        new_name = ".".join(name_file)
        content = pickle.load(file)
        text = decompress(content)
        with open(new_name, 'w') as f:
            f.write(text)
            f.close()
        file.close()
        print('Decompression successful. ' + 'Size: ' + str(os.path.getsize(new_name)) + ' bytes')

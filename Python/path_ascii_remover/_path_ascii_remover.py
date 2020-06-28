# -*- coding: utf-8 -*-
from __future__ import annotations
import os
import sys

def _replace_non_ascii(source, replace_with=' ') -> str:
    res = ''
    for _character in source:
        if _character.isascii():
            res += _character
        else:
            res += replace_with
    return res

def _rename_non_ascii_by_path(_root_path, _file, _type: str = ''):
    _nu_file = _replace_non_ascii(_file)
    if _file != _nu_file:
        print('Renaming {} from to:'.format(_type))
        print(_root_path + '\\' + _file)
        print('\t{}'.format(_root_path + '\\' + _replace_non_ascii(_file)))
        os.rename(_root_path + '\\' + _file, _root_path + '\\' + _replace_non_ascii(_file))


def remove_non_ascii_text_from(paths: List[str]) -> None:
    for path in paths:
        if not os.path.isdir(path):
            print('[E](Action: Skipping) Provided path is not a dir: "{}"'.format(path))
            continue
        for (root, dirs, files) in os.walk(path):
            for _file in files:
                _rename_non_ascii_by_path(_file, root, 'file')
        for (root, dirs, files) in os.walk(path):
            for _dir in dirs:
                _rename_non_ascii_by_path(_dir, root, 'dir')

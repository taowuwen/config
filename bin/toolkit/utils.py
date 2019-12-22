#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import time

class DecodeFailed(Exception): pass

def decode_str(s):

    if not s:
        return None

    codec = ('utf-8', 'gb2312', 'gbk')

    for c in codec:
        try:
            return s.decode(c)
        except UnicodeDecodeError:
            pass
        except Exception as e:
            raise e

    raise DecodeFailed(f"decode {s} failed")


class Color:
    red = "\033[1;31m"
    green = "\033[1;32m"
    blue = "\033[1;34m"
    yellow = "\033[1;33m"
    normal = "\033[1;00m"


def paint_substr(color, ln_str, sub_str):

    if not ln_str or not sub_str:
        return ln_str

    try:
        pos = ln_str.index(sub_str)
    except ValueError:
        return ln_str
    else:
        ln = ln_str[:pos] + color + sub_str + Color.normal

        return ln + paint_substr(color, ln_str[pos + len(sub_str): ], sub_str)


def paint_substr_ignorecase(color, ln_str, sub_str):

    if not ln_str or not sub_str:
        return ln_str

    lowercase_boundry = ln_str.lower().split(sub_str.lower())

    pos = 0
    ln  = ''
    l_sub_str = len(sub_str)

    for seg in lowercase_boundry:

        # fetch segment length
        l_seg = len(seg)
        ln += ln_str[pos: pos + l_seg]
        pos += l_seg

        # color sub_str length
        ln += color + ln_str[pos: pos + l_sub_str] + Color.normal
        pos += l_sub_str

    return ln
    

if __name__ == '__main__':

    ln = "hello, world, hello, world, aaa, no, hello, world, hellohelloworldaaworld, HELLO, WORLD, , HELLOHELLOWORLDAAWORLD,HELLOHELLO,WORLDWORLDHELLOWORLD"


    print(paint_substr(Color.green, ln, "hello"))
    print(paint_substr(Color.red, ln, "world"))

    print(paint_substr(Color.blue, ln, "hello"))
    print(paint_substr(Color.yellow, ln, "world"))

    print(paint_substr(Color.blue, ln, "no"))
    print(paint_substr(Color.yellow, ln, "lo"))

    print(paint_substr_ignorecase(Color.green, ln, "hello"))
    print(paint_substr_ignorecase(Color.red, ln, "world"))
    print(paint_substr_ignorecase(Color.blue, ln, "hello"))
    print(paint_substr_ignorecase(Color.yellow, ln, "world"))
    print(paint_substr_ignorecase(Color.blue, ln, "no"))
    print(paint_substr_ignorecase(Color.yellow, ln, "lo"))



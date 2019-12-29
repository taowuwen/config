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

    @classmethod
    def valid(cls, color):

        for c in dir(cls):
            if c.startswith('_'):
                continue

            if color is getattr(cls, c):
                return True

        return False


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


def paint_str(color, ln_str):

    if Color.valid(color):
        return color + ln_str + Color.normal

    return ln_str


print_err    = lambda x: print(paint_str(Color.red,    x))
print_info   = lambda x: print(paint_str(Color.blue,   x))
print_dbg    = lambda x: print(paint_str(Color.normal, x))
print_warn   = lambda x: print(paint_str(Color.yellow, x))
print_notice = lambda x: print(paint_str(Color.green,  x))

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

    print(paint_str(Color.green, ln))

    print_err(ln)
    print_info(ln)
    print_dbg(ln)
    print_warn(ln)
    print_notice(ln)



# Importing necessary libraries
from typing import List

# Global variables
box: List[str] = [''] * 1000
box1: List[str] = [''] * 1000
st: List[int] = [0] * 1000
stt: List[int] = [0] * 1000
spn: int = 0
n: int = 0
max: int = 0
em: int = 0
em1: int = 0
mm: int = 0
flag: bool = False

def input_data():
    global em, em1, n
    em = 0
    n = int(input('n = '))
    for i in range(1, 2 * n + 1):
        box[i] = input(f'box {i} ')
        box1[i] = box[i]
        if box[i] == 'O' and em == 0:
            em = 1
    em1 = em

def check() -> bool:
    lst = box1[1]
    f1 = True
    for i in range(2, 2 * n + 1):
        if box1[i] == 'a' and lst == 'b':
            f1 = False
        if box1[i] != 'O':
            lst = box1[i]
    return f1

def print_box():
    for i in range(1, 2 * n + 1):
        print(box1[i], end=' ')
    print()

def move(pos: int):
    global spn, em1
    spn += 1
    box1[em1], box1[em1 + 1] = box1[pos], box1[pos + 1]
    box1[pos], box1[pos + 1] = 'O', 'O'
    em1 = pos
    print_box()

def move1(pos: int):
    global spn, em1
    spn += 1
    box1[em1], box1[em1 + 1] = box1[pos], box1[pos + 1]
    box1[pos], box1[pos + 1] = 'O', 'O'
    em1 = pos
    st[spn] = pos

def findway():
    global k, flag
    spn = 0
    k = 0
    while not check() and k < n - 1:
        if box1[k + 1] == 'a':
            k += 1
        else:
            if box1[k + 1] == 'b':
                if box1[k + 2] != 'O':
                    move(k + 1)
                else:
                    move(em1 + 2)
                    move(k + 1)
            t = k + 1
            while box1[t] != 'a':
                t += 1
            if t < 2 * n:
                move(t)
            else:
                move(t - 1)
                move(k + 2)
                move(k + 4)
                move(k + 1)
                if not check():
                    move(2 * n - 1)
            k += 1

def back():
    global em1, spn, flag
    em1 = em
    for i in range(1, 2 * n + 1):
        box1[i] = box[i]
    j = spn - 1
    spn = 0
    if j == 0:
        flag = False
    else:
        for i in range(1, j + 1):
            move1(st[i])

def forward():
    global flag, spn
    if spn < mm:
        t = 1
        while box1[t] == 'O' or box1[t + 1] == 'O':
            t += 1
        move1(t)
    else:
        while True:
            t = st[spn]
            back()
            while t == 2 * n or (box1[t] == 'O' and box1[t + 1] == 'O'):
                t += 1
            if t < 2 * n:
                flag = True
            if t < 2 * n or not flag:
                break
        if t < 2 * n:
            move1(t)

def findmin():
    global max, spn, mm, em1
    if check():
        mm = spn
        em1 = em
        for i in range(1, 2 * n + 1):
            box1[i] = box[i]
        max = mm + 1
        spn = 0
        flag = True
        while flag and spn <= mm:
            if check():
                if max > spn:
                    max = spn
                    for i in range(1, max + 1):
                        stt[i] = st[i]
                    mm = max
                forward()
            else:
                forward()
        print(max)
        for i in range(1, 2 * n + 1):
            box1[i] = box[i]
        em1 = em
        print_box()
        for i in range(1, max + 1):
            move(stt[i])
    else:
        print('no way')

# Main procedure
input_data()
print_box()
findway()
findmin()


import numpy as np

def find_table(img_array):  # находит границы таблицы с оценками
    a, b, c, d = -1, -1, -1, -1

    find = False
    for i in range(int(img_array.shape[0] / 2), img_array.shape[0]):
        for j in range(img_array[i].shape[0]):
            if img_array[i][j][0] > 0.5:
                a = j
                find = True
                break
        if find:
            break

    find = False
    for i in range(int(img_array.shape[0] / 2), img_array.shape[0]):
        for j in range(img_array[i].shape[0]):
            if img_array[i][-j][0] > 0.5:
                b = img_array[i].shape[0] - j
                find = True
                break
        if find:
            break

    for i in range(int(img_array.shape[0] / 2), img_array.shape[0]):
        if img_array[-i][a][0] < 0.2 and img_array[-i][a - 5][0] < 0.2 and img_array[-i][a + 5][0] < 0.2:
            c = img_array.shape[0] - i
            break

    for i in range(int(img_array.shape[0] / 2), img_array.shape[0]):
        if img_array[i][a][0] < 0.2 and img_array[i][a - 5][0] < 0.2 and img_array[i][a + 5][0] < 0.2:
            d = i
            break

    return a, b, c, d

def find_title(img_array):#находит координаты шапки
    i = 0
    while (i < img_array.shape[0]):
        if img_array[i][10][0] > 0.5:
            title = i
            break
            i += 10
        else: i += 1
    return title

def highlight_borders(img_array):#подсвечивает границы
    for i in range(img_array.shape[0]):
        for j in range(10):
            img_array[i][j][0] = 1
            img_array[i][img_array.shape[1] - j - 1][0] = 1
    for i in range(img_array.shape[1]):
        for j in range(10):
            img_array[j][i][0] = 1
            img_array[img_array.shape[0] - j - 1][i][0] = 1
    return(img_array)

def delete_highlight_borders(img_array):#убирает подсвечивание границы
    for i in range(img_array.shape[0]):
        for j in range(10):
            img_array[i][j][0] = 0
            img_array[i][img_array.shape[1] - j - 1][0] = 0
    for i in range(img_array.shape[1]):
        for j in range(10):
            img_array[j][i][0] = 0
            img_array[img_array.shape[0] - j - 1][i][0] = 0
    return(img_array)

def find_columns_coordinates(img_array):#находит координаты столбцов
    i = 0
    coordinates = []
    while (i < img_array.shape[1]):
        if img_array[15][i][0] > 0.5:
            coordinates.append(i)
            i += 100
        else:
            i += 1
    return coordinates

def find_rows_coordinates(img_array):#находит координаты строк
    i = 0
    coordinates = []
    while (i < img_array.shape[0]):
        if img_array[i][15][0] > 0.5:
            coordinates.append(i)
            i += 50
        else:
            i += 1
    return coordinates

def prepare_marks(marks):
    for t in range(len(marks)):
        for i in range(marks[t].shape[1]):
            for j in range(marks[t].shape[0]):
                if (marks[t][j][i][0] > 0.5):
                    marks[t][j][i][0] = 1
                else:
                    marks[t][j][i][0] = 0
    return marks

def detect_numbers(marks):
    coord1 = []
    coord2 = []
    coord3 = []
    coord4 = []

    for t in range(len(marks)):
        for i in range(15, marks[t].shape[1] - 21):
            summ = 0
            for j in range(15, marks[t].shape[0] - 21):
                summ += marks[t][j][i][0]
            if summ > 7:
                coord1.append(i - 5)
                break

    for t in range(len(marks)):
        for i in range(15, marks[t].shape[1] - 21):
            summ = 0
            for j in range(15, marks[t].shape[0] - 21):
                summ += marks[t][j][-i][0]
            if summ > 7:
                coord2.append(marks[t].shape[1] - i + 5)
                break

    for t in range(len(marks)):
        for i in range(15, marks[t].shape[0] - 21):
            summ = 0
            for j in range(15, marks[t].shape[1] - 21):
                summ += marks[t][i][j][0]
            if summ > 7:
                coord3.append(i - 5)
                break

    for t in range(len(marks)):
        for i in range(15, marks[t].shape[0] - 21):
            summ = 0
            for j in range(15, marks[t].shape[1] - 21):
                summ += marks[t][-i][j][0]
            if summ > 7:
                coord4.append(marks[t].shape[0] - i + 5)
                break

    for i in range(len(marks)):
        marks[i] = marks[i][coord3[i]:coord4[i], coord1[i]:coord2[i]]

    return marks

def make_square_marks(marks):
    for i in range(len(marks)):
        x = marks[i]
        plusHeight = int(x.shape[0] / 5)
        a = np.zeros((plusHeight, x.shape[1], x.shape[2]))
        b = np.vstack((x, a))
        c = np.vstack((a, b))
        plusWidth = int((c.shape[0] - c.shape[1]) / 2)
        a = np.zeros((c.shape[0], plusWidth, x.shape[2]))
        b = np.hstack((c, a))
        d = np.hstack((a, b))
        marks[i] = d
    return marks

def find_fio_column(columns_coordinates, img_array):
    razn = 0
    for i in range(len(columns_coordinates)-1):
        tmp_razn = columns_coordinates[i+1] - columns_coordinates[i]
        if tmp_razn > razn:
            max_poz = columns_coordinates[i + 1]
            max_poz_pred = columns_coordinates[i]
            razn = tmp_razn
    return img_array[0:img_array.shape[0], max_poz_pred:max_poz]
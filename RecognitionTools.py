from PIL import Image
import pytesseract
from keras.preprocessing import image
from CroppingTools import *
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
import os
from keras.models import model_from_json


def load_NN():
    json_file = open("C:/Users/eremi/Desktop/model_digit.json", "r")
    loaded_model_json = json_file.read()
    json_file.close()
    # Создаем модель на основе загруженных данных
    loaded_model = model_from_json(loaded_model_json)
    # Загружаем веса в модель
    loaded_model.load_weights("C:/Users/eremi/Desktop/model_digit.h5")
    return loaded_model

def text_recognition(inputfilepath):
    # создание обработанного изображения
    img = Image.open(inputfilepath)
    img = img.convert("RGB")
    pixdata = img.load()
    config = ('-l rus --oem 3 --psm 3')
    # Make the letters bolder for easier recognition
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][0] < 90:
                pixdata[x, y] = (0, 0, 0, 255)
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][1] < 136:
                pixdata[x, y] = (0, 0, 0, 255)
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][2] > 0:
                pixdata[x, y] = (255, 255, 255, 255)
    img.save("tmp.jpg")
    #   Make the image bigger (needed for OCR)
    im_orig = Image.open("tmp.jpg")
    im_orig = im_orig.resize((1000, 500), Image.NEAREST)
    img.save("tmp.jpg")
    # поворот изображения и считывание текста
    im = Image.open('tmp.jpg')
    (width, height) = im.size

    extr_txt = pytesseract.image_to_string(im, config=config)
    # удаление преобразованного изображения
    os.remove('tmp.jpg')
    return extr_txt





def get_marks(img_array, columns_coordinates):
    columns = []
    for i in range(len(columns_coordinates) - 1):
            columns.append(highlight_borders(img_array[0:img_array.shape[0], columns_coordinates[i]:columns_coordinates[i+1]]))
    column_with_marks1, column_with_marks2 = columns[3], columns[4]
    rows1, rows2 = find_rows_coordinates(column_with_marks1), find_rows_coordinates(column_with_marks2)
    marks = []
    for i in range(len(rows1) - 1):
            marks.append(highlight_borders(
                column_with_marks1[rows1[i]:rows1[i+1], 0:column_with_marks1.shape[1]]))
            marks.append(highlight_borders(
                column_with_marks2[rows2[i]:rows2[i+1], 0:column_with_marks2.shape[1]]))

    marks = make_square_marks(detect_numbers(prepare_marks(marks)))
    for i in range(len(marks)):
        image.save_img(f"C:/Users/eremi/Desktop/marks/mark{i}.jpg", marks[i])
    loaded_model = load_NN()
    recogniting_marks = []
    for i in range(len(marks)):
        recogniting_marks.append(recognite(f"C:/Users/eremi/Desktop/marks/mark{i}.jpg", loaded_model))
    return recogniting_marks

def get_fios(img_array, columns_coordinates):
#распознавание фио
    fio_column = highlight_borders(find_fio_column(columns_coordinates, img_array))
    rows_fio_coordinate = find_rows_coordinates(fio_column)
    fio = []
    for i in range(len(rows_fio_coordinate) - 1):
            fio.append(
                fio_column[rows_fio_coordinate[i]:rows_fio_coordinate[i+1], 0:fio_column.shape[1]])
    for i in range(len(fio)):
        image.save_img(f"C:/Users/eremi/Desktop/fios/fio{i}.jpg", delete_highlight_borders(fio[i]))
        #image.save_img(f"C:/Users/eremi/Desktop/fios/fio{i}.jpg", fio[i])

    fios = []
    for i in range(len(fio)):
        fios.append(text_recognition(f"C:/Users/eremi/Desktop/fios/fio{i}.jpg"))
    return fios

def recognite(path, loaded_model):
    img = image.load_img(path, target_size=(28, 28), color_mode="grayscale")
    x = image.img_to_array(img)
    #x = 255 - x
    x /= 255
    x = np.expand_dims(x, axis=0)
    prediction = loaded_model.predict(x)
    return np.argmax(prediction)
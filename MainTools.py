from CroppingTools import *
from RecognitionTools import *
from DataSavingTools import *
from keras.preprocessing import image

def start_recognition(path):
    #распознавание
    img = image.load_img(path, color_mode="grayscale")
    img_array = (255 - image.img_to_array(img))/255
    a, b, c, d = find_table(img_array)
    img_array = img_array[c+80:d, a:b]
    title = find_title(img_array)
    img_array = highlight_borders(img_array[title:d])
    image.save_img('C:/Users/eremi/Desktop/im.jpg', img_array)
    columns_coordinates = find_columns_coordinates(img_array)
    marks = get_marks(img_array, columns_coordinates)
    fios = get_fios(img_array, columns_coordinates)
    data = create_data(fios, marks)
    write_in_csv(data)


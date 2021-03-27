Съдържание:

- [Кода](#Код-на-уеб-приложението) на уеб приложението
- [Кода](#Код-на-модела) на модела

# Код на уеб приложението

## Приложението ползва leaflet.js

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
  integrity="~snip~"
  crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
  integrity="~snip~`"
  crossorigin=""></script>

<!-- На местата на ~snip~ е хашът от приложението-->
```

### Инициализиране на картата

```js
var mymap = L.map('karta',{
    minZoom: 14.40
}).setView([42.50, 27.47388], 14.40);

// Тук вкарваме растеризираната Maptiler карта
L.tileLayer('https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=~KEY~', {
    attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
}).addTo(mymap);
```

След като имаме картата вкарваме всички локации в масив като правим още няколко масива за информация. Данните за всеки номер елемент от единия масив се отнасят за същия номер елемнт от другите.

```js
//Масив за координати
let coordinates_arr = [[42.49828,27.47052], [42.49627,27.47135], [42.49360,27.47254], [42.49371,27.47487], [42.48881,27.48027], [42.49855,27.48190], [42.50337,27.48204], [42.56328,27.52605], [42.55404,27.51512]];
//Масив за string формат на името на локациите
let locations_arr = ["Паметник \"Альоша\"", "Център", "Хотел България", "Богориди", "Морска Гара", "Морски театър", "Детски кът", "Сарафово", "Сарафово пристанище"];
//Масив, който се използва при вкарването на клиповете
let names_arr = ["alyosha", "centre", "hotelbg", "bogoridi", "morskagara", "theater", "detskikut", "sarafovo", "marina"];
//Масив за нивата на струпване
let levels = ['Пренатрупано', 'Малко струпване', 'Малко хора'];
//Помощен масив
let people_arr = [];
//Масив за събиране на локации. Всяка локация е във вид object.
let circle_arr = [];
```

Чрез цикъл записваме всички локации в масива *circle_arr*. При направата на кръг се вика функцията *circle()*, която взима за параметри двуелементен масив с координати (*затова използвахме coordinates_arr*) и object, в който можем да стилизираме кръга. В друг цикъл след като са се добавили всички елементи зареждаме прозорчетата с информация.

```js
//Зареждане на локациите
for (let x = 0; x < coordinates_arr.length; x++) 
{
    let coordinates = coordinates_arr[x];
    circle_arr.push(L.circle(coordinates, {
        color: "grey",
        radius: 80
    }));
}

//Наслагване на pop-up-и
for (let x in circle_arr)
{
    circle_arr[x].addTo(mymap).bindPopup(`Зарежда се...`);
}
```

Накрая на кода слагаме функция, която се изпълнява на всеки 10 секунди. В случая ползваме симулация на истинската функционалност, която за да се имплементира ще е нужно да се замени **switch-а** с резултати от модела ни.

```js
setInterval(() => {
    for (let x in circle_arr)
    {
        //simulation
        let color = '';
        let level = '';
        switch (names_arr[x])
        {
            case 'alyosha':
                if (temp === 0)
                {
                    color = "red";
                    level = levels[0];
                    temp = 1;
                } else {
                    color = "yellow";
                    level = levels[1];
                    temp = 0;
                }
                break;
            case 'morskagara':
                color = 'green';
                level = levels[2];
                break;
            case 'theater':
                color = "green";
                level = levels[2]
                break;
            case 'centre': 
                color = 'red';
                level = levels[0];
                break;
            default:
                color = 'yellow';
                level = levels[1];
        };
        people_arr[x] = [color, level];
    }
    for (let x in circle_arr)
    {
        circle_arr[x].setStyle({color:people_arr[x][0]});
        circle_arr[x]._popup.setContent(`<span>Мястото е: ${locations_arr[x]} </span><br> <span>и се намира на: ${coordinates_arr[x]} </span><br> <span>Нивото на пренатрупване е: ${people_arr[x][1]} </span><video id='canvas' src="./videos/${names_arr[x]}.mp4" type="video/webm" loop muted autoplay></video> <br> `);
    }
}, 10000)
```

# Код на модела

## Импортове

```py
import pandas as pd
import random
import numpy as np
import matplotlib
import os
import tensorflow as tf
from PIL import Image
from tensorflow import keras
from tensorflow.keras import datasets, layers, models
import matplotlib.image as mp
from  matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
import tensorflowjs as tfjs
```

## Функция за извличане на снимките от dataset-а, етикиране и форматиране на данните (снимките)

```py
img_width = 64
img_height = 64

def create_dataset(img_folder):
    
    img_data_array=[]
    img_labels=[]
    class_name=[]
    for dir1 in os.listdir(img_folder):
        for file in os.listdir(os.path.join(img_folder, dir1)):
       
            if dir1=='Large density': img_labels.append(1)
            if dir1=='Average density': img_labels.append(0)
            if dir1=='No density': img_labels.append(2)
            image_path= os.path.join(img_folder, dir1,  file)
            
            image= Image.open(image_path)#.convert('L')
            image.thumbnail((img_height, img_width), Image.ANTIALIAS)
            
            image = np.array(image)
            image= np.resize(image,(img_height,img_width,3))
            image = image.astype('float32')
            image /= 255
            img_data_array.append(image)
        class_name.append(dir1)
    return img_data_array , class_name, img_labels
```

## Разделяне на снимките от dataset-а на training и test

```py
X, class_names, y = create_dataset(r'Crowds COMBINED')

train_images, test_images, train_labels, test_labels = train_test_split(X, y, test_size=0.25, random_state=1)

train_images = np.array(train_images)
train_labels = np.array(train_labels)

test_images = np.array(test_images)
test_labels = np.array(test_labels)

# Създаване на модела на невронна мрежа
```

## Оптимизиране на модела с data augmentation

```py
data_augmentation = keras.Sequential(
  [
    layers.experimental.preprocessing.RandomFlip("horizontal", 
                                                 input_shape=(img_height, 
                                                              img_width,
                                                              3)),
    layers.experimental.preprocessing.RandomRotation(0.1),
    layers.experimental.preprocessing.RandomZoom(0.1),
  ]
)
```

## Невронна мрежа

```py
model = models.Sequential([
    data_augmentation,
    layers.experimental.preprocessing.Rescaling(1./255),
    layers.Conv2D(32, (2, 2), activation='relu', input_shape=(img_height, img_width, 3)),
    layers.MaxPooling2D((2, 2)),
    #layers.Conv2D(64, (3, 3), activation='relu'),
    #layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.1),
    layers.Flatten(),
    layers.Dense(96, activation='relu'),
    layers.Dense(3)])

```

## Компилираме на модела

```py
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary()

epochs = 100

# Обучение на модела и запазване

history = model.fit(train_images, train_labels, validation_data=(test_images, test_labels), epochs=epochs)

tfjs.converters.save_keras_model(model, 'crowd_model_js')\
```

## Създаване на графика

```py
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()
```

### КОДЪТ Е ПОД MIT LICENSE

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

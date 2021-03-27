// Initialization of the map
var mymap = L.map('karta',{
    minZoom: 14.40
}).setView([42.50, 27.47388], 14.40);

L.tileLayer('https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=umeEEPwaY1ljp2yJrdAM', {
    attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
}).addTo(mymap);

// Arrays used for storing information about particular locations 
let coordinates_arr = [[42.49828,27.47052], [42.49627,27.47135], [42.49360,27.47254], [42.49371,27.47487], [42.48881,27.48027], [42.49855,27.48190], [42.50337,27.48204], [42.56328,27.52605], [42.55404,27.51512]];
let locations_arr = ["Паметник \"Альоша\"", "Център", "Хотел България", "Богориди", "Морска Гара", "Морски театър", "Детски кът", "Сарафово", "Сарафово пристанище"];
let names_arr = ["alyosha", "centre", "hotelbg", "bogoridi", "morskagara", "theater", "detskikut", "sarafovo", "marina"];
let levels = ['Пренатрупано', 'Малко струпване', 'Малко хора'];
let people_arr = [];
let circle_arr = [];

//Loading locations into an array which will be later used.
for (let x = 0; x < coordinates_arr.length; x++) 
{
    let coordinates = coordinates_arr[x];
    circle_arr.push(L.circle(coordinates, {
        color: "grey",
        radius: 80
    }));
}

async function loadModel()
{
    let model = await tf.loadLayersModel("../crowd_model_js/model.json");
}
loadModel()



//Binding pop-ups to each circle
for (let x in circle_arr)
{
    circle_arr[x].addTo(mymap).bindPopup(`Зарежда се...`);
}

let temp = 0;

//Information update every 10 seconds
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

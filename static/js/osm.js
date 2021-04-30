function osmInit(upload) {
    var moscow_location = [55.753995, 37.614069]

    var mapOptions = {
       center: moscow_location,
       zoom: 10
    }
    // initialize Leaflet
    var map = new L.map('map', mapOptions);

    // add the OpenStreetMap tiles
    var layer = new L.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');

    map.addLayer(layer);
    
    map.on('click', function(e) {
        var marker = new L.marker([e.latlng.lat, e.latlng.lng]);
        var popUpContent = `<div style="position: absolute; background-color: white; z-index:2; border: 1px solid black; border-radius: 5px;">\
        <form action="${upload}" method="POST" enctype="multipart/form-data">\
        <p align="center"><h4>Название события:</h4><input type="text" name="name"></p>\
        <p align="center"><h4>Описание:</h4><input type="text" name="description"></p>\
        <p align="center"><h4>Фото</h4>(можно выбрать несколько):<input type="file" name="photo" multiple/></p>\
        <p align="center"><h4>Видео</h4>(можно выбрать несколько):<input type="file" name="video" multiple/></p>\
        <p align="center"><input type="submit", value="Отправить"/></p></form>\
        <input type="hidden" name="lat" value="${e.latlng.lat.toString()}" />\
        <input type="hidden" name="lng" value="${e.latlng.lng.toString()}" />\
        </div>`;
        marker.bindPopup(popUpContent).openPopup();
        marker.addTo(map);
    });
}

    // show a marker on the map
    //var marker = new L.marker(moscow_location).bindPopup('Hello').openPopup();

  //  <link rel = "stylesheet" href = "http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css"/>
  // <script src = "http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>


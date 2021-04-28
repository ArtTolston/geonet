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
    

    // show a marker on the map
    var marker = new L.marker(moscow_location).bindPopup('Hello').openPopup();

    marker.addTo(map)

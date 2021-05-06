var eventLocation;

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
        eventLocation = e.latlng;
        var marker = new L.marker([e.latlng.lat, e.latlng.lng]);
        document.getElementById('lat').value = eventLocation.lat;
        document.getElementById('lng').value = eventLocation.lng;
        var eventDiv = document.getElementById('addEvent');
        var popUpContentDiv = eventDiv.cloneNode(true);
        popUpContentDiv.style.display = 'block';
        marker.bindPopup(popUpContentDiv).openPopup();
        marker.addTo(map);
    });
}

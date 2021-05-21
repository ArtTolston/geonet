var eventLocation;

function osmInit(upload, events) {
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


    for(var i = 0; i < events.length; i++) {
        var lat = parseFloat(events[i]['latitude']);
        var lng = parseFloat(events[i]['longtitude']);
        var marker = new L.Marker([lat, lng]);
        document.getElementById('eventName').innerHTML = events[i]['name'];
        var elems = document.getElementsByClassName('eventId');
        for(var j = 0; j < elems.length; j++){
            elems[j].value = events[i]['id'];
        }
        var eventInfo = document.getElementById('eventInfo');
        var popUpContentInfo = eventInfo.cloneNode(true);
        popUpContentInfo.style.display = 'block';
        marker.bindPopup(popUpContentInfo).openPopup();
        marker.addTo(map);
    }
}

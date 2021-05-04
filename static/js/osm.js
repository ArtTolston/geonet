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

function send(formData) {
    //xhr.setRequestHeader('Content-Type', 'application/json');
    //xhr.send(JSON.stringify(eventLocation));
    var obj = {};
    var filesLength = document.getElementById('photo').files.length;
    alert(filesLength);
    for(var i = 0; i < filesLength; i++) {
        obj[document.getElementById('photo').files[i].name] = document.getElementById('photo').files[i];
    }

    filesLength = document.getElementById('video').files.length;
    alert(filesLength);
    for(var i = 0; i < filesLength; i++) {
        obj[document.getElementById('video').files[i].name] = document.getElementById('video').files[i];
    }
    formData.append('files', obj)

    return formData
}

function sendEvent() {
    var formData = new FormData();
    formData = send(formData);

    var e = document.getElementById('grouplist');
    var choosenGroupId = e.options[e.selectedIndex].value;
    var name = document.getElementById('name').value;
    var description = document.getElementById('description').value;
    var latitude = document.getElementById('lat').value;
    var longtitude = document.getElementById('lng').value;
    var object = {
        'name': name,
        'description': description,
        'groupId': choosenGroupId, 
        'latlng': [latitude, longtitude],
    }
    //formData.append('meta', object);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);
    xhr.send(formData);
}



    // show a marker on the map
    //var marker = new L.marker(moscow_location).bindPopup('Hello').openPopup();

  //  <link rel = "stylesheet" href = "http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css"/>
  // <script src = "http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>
/*
                ext = os.path.splitext(name)
                mediatype = None
                if ext in ['.png', '.jpg', '.jpeg']:
                    mediatype = 'photo'
                elif ext in ['.mp4', '.avi', '.mkv']:
                    mediatype = 'video'
                else:
                    print('unknown format\n')*/
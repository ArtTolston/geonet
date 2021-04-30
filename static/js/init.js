
function init(location, upload){
    var opt = {};
    opt["zoom"] = 13;
    if(location == "moscow") {
        opt["center"] = [55.753995, 37.614069];
    } else if(location == "spb") {
        opt["center"] = [59.943611, 30.330421];
    }

    var myMap = new ymaps.Map("map", opt);

    myMap.events.add('click', function(e) {
		
        var coords = e.get('coords');
        var newPlacemark = new ymaps.Placemark(coords);

        newPlacemark.events.add('click', function(event) {
        	var divmap = document.getElementById('map');
        	var check = document.getElementById('divmenu');
        	if(!check) {
	        	var divmenu = document.createElement('div');

	        	divmenu.innerHTML = `<form action="${upload}" method="POST" enctype="multipart/form-data">\
	        	<p align="center">Описание: <br/><input type="text" name="description"></p>\
	        	<p align="center">Фото: <br/><input type="file" name="file" /></p>\
	        	<p align="center"><input type="submit", value="Отправить"/></p></form>\
	        	<input type="hidden" name="shirote" value="${coords[0].toString()}" />\
	        	<input type="hidden" name="dolgota" value="${coords[1].toString()}" />`;

	        	divmenu.style.cssText = `position: absolute; background-color: white; z-index:2; border: 1px solid black; border-radius: 5px;`;
	        	divmenu.style.left = event.get('pagePixels')[0];
	        	divmenu.style.top = event.get('pagePixels')[1];
	            divmenu.id = 'divmenu';

	        	divmap.appendChild(divmenu);
        	} else {
        		divmap.removeChild(check);
        	}

        });

        myMap.geoObjects.removeAll();
        myMap.geoObjects.add(newPlacemark);
    });

    
    


}



        var popUpContent = `<div style="position: absolute; background-color: white; z-index:2; border: 1px solid black; border-radius: 5px;">\
                <form action="${upload}" method="POST" enctype="multipart/form-data">\
                <p align="center">Описание: <br/><input type="text" name="description"></p>\
                <p align="center">Фото: <br/><input type="file" name="file" /></p>\
                <p align="center"><input type="submit", value="Отправить"/></p></form>\
                <input type="hidden" name="lat" value="${e.latlng.lat.toString()}" />\
                <input type="hidden" name="lng" value="${e.latlng.lng.toString()}" />\
                </div>`;
        marker.bindPopup(popUpContent).openPopup();
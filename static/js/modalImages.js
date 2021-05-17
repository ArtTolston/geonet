// Get the modal
var photo_ids =[];

function modalImagesInit(_photo_ids) {
	for(var i = 0; i < _photo_ids.length; i++) {
		photo_ids.push(_photo_ids[i]);
	}
}

var modal = document.getElementById('myModal');

// Get the image and insert it inside the modal - use its "alt" text as a caption
for(var i = 0; i < photo_ids.length; i++) {
	var img = document.getElementById(photo_ids[i]);
	var modalImg = document.getElementById("img01");
	img.onclick = function(){
	    modal.style.display = "block";
	    modalImg.src = this.src;
	    captionText.innerHTML = this.alt;
	}
	// Get the <span> element that closes the modal
	var span = document.getElementsByClassName("close")[0];

	// When the user clicks on <span> (x), close the modal
	span.onclick = function() {
	  modal.style.display = "none";
	} 
}
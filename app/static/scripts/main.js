function openPic(obj){
	var cont = document.getElementById('fullsize');
	var lnk = obj.getAttribute('src');
	var img = cont.firstChild;
	img.setAttribute('src',lnk);
	cont.style.display="block";
}

function hidePic(){
	var cont = document.getElementById('fullsize');
	cont.style.display="none";
}
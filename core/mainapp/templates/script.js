function readMore(){
	let more = document.getElementById("more");
	let btn = document.getElementById("btn");
	
	if(more.style.display === "none"){
	  btn.innerHTML="Скрыть";
	  more.style.display="inline";
	}else {
	  btn.innerHTML="Показать";
	  more.style.display="none";
	}

}
alert(123);
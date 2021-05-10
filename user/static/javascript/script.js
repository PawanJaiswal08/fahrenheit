var el = document.querySelector('.img-btn');

function swapper() {
	document.querySelector('.cont').classList.toggle('s-signup');
}


if(el){
	el.addEventListener('click', swapper , false);
}

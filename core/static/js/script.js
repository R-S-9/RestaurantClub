$(document).ready(function(){
	$('.slider').slick({
		dots: true,
		slidesToShow: 2,
		slidesToScroll:2,
		speed: 300,
		infinite: true,
		autoplay: false,
		autoplaySpeed: 1500,
		pauseOnFocus: true,
		pauseOnHover: true,
		pauseOnDotsHover: true,
		draggable: true, //свайп мышкой
		swipe: true,
		waitForAnimate: false,
		adaptiveHeight: true,
		
		responsive: [
			{
				breakpoint: 1000,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1,
					arrows: false
				}
			}
		]
	});
});

Element.width

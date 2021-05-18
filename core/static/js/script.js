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

// Модальное окно--------------

// Открыть
$(document).on('click', '.js-form-button', function() {
	$('.wrapper').css('filter','blur(5px)');
	$('.js-overlay').fadeIn();
	$('.js-overlay').addClass('disabled');
});
// Закрыть
$(document).on('click', '.js-close', function() {
	$('.wrapper').css('filter','none');
	$('.js-overlay').fadeOut();
});
// Закрытьпо клику все окна
$(document).mouseup(function(e) {
	let popup = $('.js-popup');
	if(e.target!=popup[0]&&popup.has(e.target).length === 0){
	$('.wrapper').css('filter','none');
	$('.js-overlay').fadeOut();
	}
});

// Расширение окна ввода
$('body')
    .one('focus.textarea', '#myTextarea', function(e) {
        baseH = this.scrollHeight;
    })
    .on('input.textarea', '#myTextarea', function(e) {
        if(baseH < this.scrollHeight) {
            $(this).height(0).height(this.scrollHeight);
        }
    });



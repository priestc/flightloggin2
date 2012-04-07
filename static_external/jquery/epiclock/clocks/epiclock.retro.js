/*!
 * Retro Style Flip Clock - epiClock Rendering Engine
 *
 * Copyright (c) 2008 Eric Garside (http://eric.garside.name)
 * Dual licensed under:
 * 	MIT: http://www.opensource.org/licenses/mit-license.php
 *	GPLv3: http://www.opensource.org/licenses/gpl-3.0.html
 */
(function($){
	
	$.extend($.epiclocks, {
		retro: {
			format: 'h:i:s a',
			stylesheet: 'clocks/retro.css',
			containerClass: 'epiclock-retro',
			tpl: '<div></div>',
			innerTpl: '<div class="epiclock-img"></div>',
			onSetup: function(){
				$('.epiclock-retro .epiclock-img').live('flip-clock', function(){
					var el = $(this);
					setTimeout(function(){ 
						el.removeClass('a1').addClass('a2');
						setTimeout(function(){ el.removeClass('a2').addClass('s') }, 150);
					}, 150);
				});
			},
			onRender: function(el, val){
				var digits = val.substring(1) == 'm' ? [val] : val.split('').reverse(),
					last = el.data('last'),
					prefix = last ? 'd' : 's',
					cmp = last ? last.split('').reverse() : [],
					img = $.makeArray($('.epiclock-img', el)).reverse(),
					clock = this;
					
				$.each(digits, function(i,v){
					if (v == cmp[i]) return;
					$(img[i] || $(clock.innerTpl).prependTo(el))
						.removeClass('s d'+cmp[i])
						.addClass('d' + v + ' a1')
						.trigger('flip-clock');
				});
			}
		}
	});
	
})(jQuery);

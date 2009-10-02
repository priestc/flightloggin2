$(document).ready(function() {
	$("a[href=]").click(function(event) {			//all fake anchors are disabled
		event.preventDefault();
	});
	
	jQuery.fn.centerScreen = function(loaded) {
        var obj = this;
        if(!loaded) {
                obj.css('top', $(window).height()/2-this.height()/2);
                obj.css('left', $(window).width()/2-this.width()/2);
                $(window).resize(function() { obj.centerScreen(!loaded); });
        } else {
                obj.stop();
                obj.animate({ top: $(window).height()/2-this.height()/2,
                left: $(window).width()/2-this.width()/2}, 200, 'linear');
        }
    }
});

function trim(str){
	return str.replace(/^\s*((?:[\S\s]*\S)?)\s*$/, '$1');
}

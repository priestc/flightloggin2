function wipe_clean() {
	$("#popup input[type=text], #popup textarea, #popup select").val("");
	$("#popup input[type=checkbox]").attr("checked", "");
}

function fire_popup() {

    var scrolledX, scrolledY;
	
	if( self.pageYOffset )
	{
		scrolledX = self.pageXOffset;
		scrolledY = self.pageYOffset;
	}
	else if( document.documentElement && document.documentElement.scrollTop )
	{
		scrolledX = document.documentElement.scrollLeft;
		scrolledY = document.documentElement.scrollTop;
	}
	else if( document.body )
	{
		scrolledX = document.body.scrollLeft;
		scrolledY = document.body.scrollTop;
	}

    var p = $('#popup');
    p.centerScreen();
    p.draggable({ 
		zIndex: 20,
		cursor: 'move',
		opacity: 1.0,
		handle: '#dragbar'
	});
	
	var t = p.css("top");
	p.css("top", scrolledY + parseInt(t));
	p.show();
	
}

function fire_popup2() {

	// Determine how much the visitor had scrolled

	var scrolledX, scrolledY;
	
	if( self.pageYOffset )
	{
		scrolledX = self.pageXOffset;
		scrolledY = self.pageYOffset;
	}
	else if( document.documentElement && document.documentElement.scrollTop )
	{
		scrolledX = document.documentElement.scrollLeft;
		scrolledY = document.documentElement.scrollTop;
	}
	else if( document.body )
	{
		scrolledX = document.body.scrollLeft;
		scrolledY = document.body.scrollTop;
	}

	top = ((window.innerHeight - $('#popup').innerHeight()) / 2) + scrolledY;
	left = (window.innerWidth - $('#popup').innerWidth()) / 2;

	$('#popup').draggable({ 
		zIndex: 20,
		cursor: 'move',
		opacity: 1.0,
		handle: '#dragbar'
	}).css("top", top).css("left", left).show();
}

$(document).ready(function() {

	$("#close_x").click(function(event) {
		$("#popup").hide("slow");
	});
});







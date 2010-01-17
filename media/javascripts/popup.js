function wipe_clean() {

    // uncheck all checkboxes and clear all input boxes
	$("#popup input[type=text], #popup textarea, #popup select").val("");
	$("#popup input[type=checkbox]").attr("checked", "");
	
	// remove the error messages
	$("#popup td#new_error_cell").text("");
	$("#popup td#edit_error_cell").text("");
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
	
	// fire popup if an error is detected
	if( $("td#new_error_cell").text() != "" )  {     
	    prepare_new();
	    fire_popup();
	}
	
	if( $("td#edit_error_cell").text() != "") {
	    prepare_edit();
	    fire_popup();
	}
});









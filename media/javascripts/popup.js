function wipe_clean() {
	$("input[type=text], textarea, select").val("");
	$("input[type=checkbox]").attr("checked", "");
}

function fire_popup(popup_id) {

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

	top = ((window.innerHeight - $('#' + popup_id).innerHeight()) / 2) + scrolledY;
	left = (window.innerWidth - $('#' + popup_id).innerWidth()) / 2;

	$('#' + popup_id).draggable({ 
		zIndex: 20,
		cursor: 'move',
		opacity: 1.0,
		handle: '#dragbar'
	}).css("top", top).css("left", left).show();
}

$(document).ready(function() {

	$("#close_x").click(function(event) {
		$("#new_entry_popup").hide("slow");
		$("#plane_popup").hide("slow");
	});
});







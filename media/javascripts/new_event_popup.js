function fill_in_event(dom_id) {
	
	id = dom_id.substr(1);

	$("#id_id").val(id);
	$("#id_non_flying").val(trim($("#p" + id + "_non_flying").text()));
	$("#id_remarks").val(trim($("#p" + id + "_remarks").text()));
}


function prepare_new_event(wipe) {
	if(wipe)
		wipe_clean();
	
	$('#titlebar').text("New Event");
	$("#new_buttons").show();
	$("#edit_buttons").hide();
}

function prepare_edit_event(wipe) {
	if(wipe)
		wipe_clean();
	
	$('#titlebar').text("Edit Event");
	$("#new_buttons").hide();
	$("#edit_buttons").show();
}

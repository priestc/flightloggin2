function fill_in_event(dom_id) {
	
	id = dom_id.substr(1);
	
	//alert(id);

	$("#id_id").val(id);
	$("#id_date").val(trim($("tr#row_" + id + " span.unformatted_date").text()));
	$("#id_remarks").val(trim($("tr#row_" + id + " td.remarks").text()));
	
	$("#id_non_flying option:contains(" + trim($("tr#row_" + id + " td.non_flying").text()) + ")").attr("selected", "selected");
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

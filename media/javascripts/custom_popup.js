function fill_in_custom(dom_id) {
	
	id = dom_id.substr(1);

	$("#id_id").val(id);
	$("#id_identifier").val(trim($("#p" + id + "_identifier").text()));
	$("#id_name").val(trim($("#p" + id + "_name").text()));
	$("#id_coordinates").val(trim($("#p" + id + "_coordinates").text()));
	$("#id_type").val(trim($("#p" + id + "_type").text()));
	$("#id_country").val(trim($("#p" + id + "_country").text()));
	$("#id_municipality").val(trim($("#p" + id + "_municipality").text()));
}


function prepare_new_custom(wipe) {
	if(wipe)
		wipe_clean();
	
	$('#titlebar').text("New Place");
	$("#new_buttons").show();
	$("#edit_buttons").hide();
}

function prepare_edit_custom(wipe) {
	if(wipe)
		wipe_clean();
	
	$('#titlebar').text("Edit Place");
	$("#new_buttons").hide();
	$("#edit_buttons").show();
}

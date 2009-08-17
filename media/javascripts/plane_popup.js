function fill_in_plane(dom_id) {
	
	id = dom_id.substr(1);

	$("#id_id").val(id);
	$("#id_tailnumber").val(trim($("#p" + id + "_tailnumber").text()));
	$("#id_model").val(trim($("#p" + id + "_model").text()));
	$("#id_manufacturer").val(trim($("#p" + id + "_manufacturer").text()));
	$("#id_type").val(trim($("#p" + id + "_type").text()));
	$("#id_cat_class").val(trim($("#p" + id + "_cat_class").text()));
	$("#id_tags").val(trim($("#p" + id + "_tags").text()));
}


function prepare_new_plane(wipe) {
	if(wipe)
		wipe_clean();
	
	$('#titlebar').text("New Plane");
	$("#new_plane_buttons").show();
	$("#edit_plane_buttons").hide();
}

function prepare_edit_plane(wipe) {
	if(wipe)
		wipe_clean();
	
	$('#titlebar').text("Edit Plane");
	$("#new_plane_buttons").hide();
	$("#edit_plane_buttons").show();
}

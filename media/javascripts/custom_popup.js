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
	
	$('#titlebar').text("New Location");
	$("#new_buttons").show();
	$("#edit_buttons").hide();
}

function prepare_edit_custom(wipe) {
	if(wipe)
		wipe_clean();
	
	$('#titlebar').text("Edit Location");
	$("#new_buttons").hide();
	$("#edit_buttons").show();
}

$(document).ready(function() {
    
    $("a.custom_click").click(function() {
        prepare_edit_custom(true);
        fill_in_custom(this.id);
        fire_popup();
    });
    
    $("#new_custom").click(function() {
        prepare_new_custom(true);
        fire_popup();
    });
    
});

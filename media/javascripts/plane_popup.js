function fill_in_plane(dom_id) {
	
	id = dom_id.substr(1);

	$("#id_id").val(id);
	$("#id_tailnumber").val(trim($("#p" + id + "_tailnumber").text()));
	$("#id_model").val(trim($("#p" + id + "_model").text()));
	$("#id_manufacturer").val(trim($("#p" + id + "_manufacturer").text()));
	$("#id_type").val(trim($("#p" + id + "_type").text()));
	$("#id_cat_class").val(trim($("#p" + id + "_cat_class").text()));
	$("#id_tags").val(trim($("#p" + id + "_tags").text()));
	$("#id_description").val(trim($("#p" + id + "_description").text()));
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

$(document).ready(function() {
	$("#new_plane").click(function(){
		wipe_clean();
		prepare_new_plane(true);
		fire_popup("popup");
	})
	
	$("a.popup_link").click(function(event){
		wipe_clean();
		prepare_edit_plane(true);
		fill_in_plane(this.id);
		fire_popup("popup");
	});

	$("#tags_window a").click(function() {
		tag= $(this).text()

		if(tag.search(' ') >= 0)
		    tag = '"' + tag + '"';
		
		val = $("#id_tags").val();
		
		if(val == "")
			$("#id_tags").val(val + tag);
	    else
	        $("#id_tags").val(val + " " + tag);
	});
});

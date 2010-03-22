function remove(s, t) {
    // remove all substrings from string
    i = s.indexOf(t);
    r = "";
    if (i == -1) return s;
    r += s.substring(0,i) + remove(s.substring(i + t.length), t);
    return r;
}

function fill_in_plane(dom_id) {

    id = dom_id.substr(1);

    $("#id_id").val(id);
    $("#id_tailnumber").val(trim($("#p" + id + "_tailnumber").text()));
    $("#id_model").val(trim($("#p" + id + "_model").text()));
    $("#id_manufacturer").val(trim($("#p" + id + "_manufacturer").text()));
    $("#id_type").val(trim($("#p" + id + "_type").text()));
    $("#id_tags").val(trim($("#p" + id + "_tags").text()));

    var desc = trim($("#p" + id + "_description").text())

    if(desc.indexOf("[Hidden]") > -1 ) {
        $("#id_hidden").attr('checked', 'checked');
    }

    if(desc.indexOf("[Retired]") > -1) {
        $("#id_retired").attr('checked', 'checked');
    }

    cc = trim($("#p" + id + "_cat_class").text());
    $("#id_cat_class option:contains(" + cc + ")").attr("selected", "selected");

    desc = remove(desc, "[Hidden]")
    desc = remove(desc, "[Retired]")
    
    $("#id_description").val(desc);	
}


function prepare_new(wipe) {
	if(wipe)
		wipe_clean();
	
	$('#titlebar').text("New Plane");
	$("#new_plane_buttons").show();
	$("#edit_plane_buttons").hide();
}

function prepare_edit(wipe) {
	if(wipe)
		wipe_clean();
	
	$('#titlebar').text("Edit Plane");
	$("#new_plane_buttons").hide();
	$("#edit_plane_buttons").show();
}

$(document).ready(function() {
	$("#new_plane").click(function(){
		wipe_clean();
		prepare_new(true);
		fire_popup("popup");
	})
	
	$("a.popup_link").click(function(event){
		wipe_clean();
		prepare_edit(true);
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

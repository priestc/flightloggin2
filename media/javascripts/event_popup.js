d = new Date();
month = (d.getMonth()+1).toString().length < 2 ? "0" + (d.getMonth()+1) : (d.getMonth()+1);	//#add a leading zero if its only one digit, +1 because javascript is dum
day = (d.getDate()).toString().length < 2 ? "0" + (d.getDate()) : (d.getDate());

var todays_date = d.getFullYear() + "-" + month + "-" + day;

//////////////////////////////////////////////////////////////////

function fill_in_event(dom_id) {
	
	id = dom_id.substr(1);
	
	//alert(id);

	$("#id_id").val(id);
	$("#id_date").val(trim($("tr#row_" + id + " span.unformatted_date").text()));
	$("#id_remarks").val(trim($("tr#row_" + id + " td.remarks").text()));
	
	$("#id_non_flying option:contains(" + trim($("tr#row_" + id + " td.non_flying").text()) + ")").attr("selected", "selected");
}


function prepare_new_event(wipe) {
	if(wipe) {
		wipe_clean();
		$("#id_date").val(todays_date);
	}
	
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

$(document).ready(function() {
    $("input[id$=date]").datepicker({
	        dateFormat: "yy-mm-dd",
	        yearRange: "-80:+1", 
	        showOn: "button", 
	        buttonImage: MEDIA_URL + "/images/calendar.gif", 
	        buttonImageOnly: true ,
	        changeYear: true
    }).addClass("embed");
    
    
    $("a.nonflight_click").click(function() {
    
        prepare_edit_event(true);
        fill_in_event(this.id);
        fire_popup();

    });
    
    $("#new_event").click(function() {
    
        prepare_new_event(true);
        
        fire_popup();

    });
    
});

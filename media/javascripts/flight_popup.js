d = new Date();
month = (d.getMonth()+1).toString().length < 2 ? "0" + (d.getMonth()+1) : (d.getMonth()+1);	//#add a leading zero if its only one digit, +1 because javascript is dum
day = (d.getDate()).toString().length < 2 ? "0" + (d.getDate()) : (d.getDate());

var todays_date = month + "/" + day + "/" + d.getFullYear();

//////////////////////////////////////////////////////////////////

function prepare_new_flight(wipe) {					    //prepares the new entry popup

	if(wipe) {
    	wipe_clean();
	    $("#id_date").val(todays_date);
	}
	
	$('#titlebar').text("New Flight");
	$("#edit_buttons").hide();
	$("#new_buttons").show();
}

function prepare_edit_flight(wipe) {				//prepares the new entry popup
	if(wipe)
		wipe_clean();
	
	$('#titlebar').text("Edit Flight");
	$("#new_buttons").hide();
	$("#edit_buttons").show();
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////

$(document).ready(function() {
	
	///////////////////////////////////////////
	
	if(ERROR == 'new') {
	    prepare_new_flight(false)
	    fire_popup("popup");
	}
	else if (ERROR == 'edit') {
	    prepare_edit_flight(false)
	    fire_popup("popup");
	}
	
	$("#id_date, .date_picker").datepicker({	// add the date pickers
			dateFormat: "yy-mm-dd",
			yearRange: "1999:2009", 
			showOn: "button", 
			buttonImage: date_button, 
			buttonImageOnly: true,
			changeYear: true 
	}).addClass("embed");
	
	/////////////////////////////////////////                 confirm checkboxes for delete flight
	
	$("#edit_buttons input[type='checkbox']").click(function() {
	
	    if ( $("#edit_buttons input[type='checkbox']:not(:checked)").size() == 0 )
            $('#delete_flight').removeAttr("disabled")
        else
            $('#delete_flight').attr("disabled", "disabled")
	    
	});
	
	/////////////////////////////////////////                     shortcut buttons
	
	$('#auto_button').click(do_auto_button);
	
	$("input[type='button'].shortcut").click(function(){
	    column = $(this).attr("class").split(" ")[0];
	    
	    prev_value = $("#id_" + column).val()
	    total_value = $("#id_total").val()
	    
	    if( total_value == prev_value)
	        $("#id_" + column).val("");
    	else
    	    $("#id_" + column).val( total_value );
	    
	});
	
	/////////////////////////////////////////
	
	$("#id_date").attr("autocomplete", "off");					// disable auto complete
	$("#id_non-date").attr("autocomplete", "off");
	$("#id_total").attr("autocomplete", "off");
	$("#id_pic").attr("autocomplete", "off");
	$("#id_solo").attr("autocomplete", "off");
	$("#id_sic").attr("autocomplete", "off");
	$("#id_dual_r").attr("autocomplete", "off");
	$("#id_dual_g").attr("autocomplete", "off");
	$("#id_act_inst").attr("autocomplete", "off");
	$("#id_sim_inst").attr("autocomplete", "off");
	$("#id_app").attr("autocomplete", "off");
	$("#id_night").attr("autocomplete", "off");
	$("#id_xc").attr("autocomplete", "off");
	$("#id_day_l").attr("autocomplete", "off");
	$("#id_night_l").attr("autocomplete", "off");
	
	////////////////////////////////////////////////////////
	
	$("#new_flight_button").click(function(event) {			//make the popup when the new flight button is clicked
		prepare_new_flight(true);
		fire_popup();
	});
	
	$("#logbook_table a").click(function(){			//make the edit popup when the date is clicked
		wipe_clean();
		prepare_edit_flight(true);
		fill_in_flight(this.id);
		fire_popup();
	});
});

function do_auto_button() {
	for(b=0;b<auto_button.length; b++)
		$("#id_" + auto_button[b]).val( $("#id_total").val() );
}

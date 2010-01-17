d = new Date();
month = (d.getMonth()+1).toString().length < 2 ? "0" + (d.getMonth()+1) : (d.getMonth()+1);	//#add a leading zero if its only one digit, +1 because javascript is dum
day = (d.getDate()).toString().length < 2 ? "0" + (d.getDate()) : (d.getDate());

var todays_date = d.getFullYear() + "-" + month + "-" + day;

//////////////////////////////////////////////////////////////////

function prepare_new(wipe) {					    //prepares the new entry popup

	if(wipe) {
    	wipe_clean();
	    $("#id_new-date").val(todays_date);
	}
	
	$('#titlebar').text("New Flight");
	$("#edit_buttons").hide();
	$("#new_buttons").show();
}

function prepare_edit(wipe) {				//prepares the new entry popup
	if(wipe)
		wipe_clean();
	
	$('#titlebar').text("Edit Flight");
	$("#new_buttons").hide();
	$("#edit_buttons").show();
}

function close_all_small_popups(){

    $(".small_popup").hide();

}

$(document).click(close_all_small_popups);

////////////////////////////////////////////////////////////////////////////////////////////////////////////////

$(document).ready(function() {
	
	$("#id_new-date, .date_picker").datepicker({	// add the date pickers
			dateFormat: "yy-mm-dd",
			yearRange: "1999:2009", 
			showOn: "button", 
			buttonImage: date_button, 
			buttonImageOnly: true,
			changeYear: true 
	}).addClass("embed");
	
	///////////////////////////////////////// confirm checkboxes for delete flight
	
	$("#edit_buttons input[type='checkbox']").click(function() {
	
	    if ( $("#edit_buttons input[type='checkbox']:not(:checked)").size() == 0 )
            $('#delete_flight').removeAttr("disabled")
        else
            $('#delete_flight').attr("disabled", "disabled")
	    
	});
	
	/////////////////////////////////////////shortcut buttons
	
	$('#auto_button').click(do_auto_button);
	
	$("input[type='button'].shortcut").click(function(){
	    column = $(this).attr("class").split(" ")[0];
	    
	    prev_value = $("#id_new-" + column).val()
	    total_value = $("#id_new-total").val()
	    
	    if( total_value == prev_value)
	        $("#id_new-" + column).val("");
    	else
    	    $("#id_new-" + column).val( total_value );
	    
	});
	
	/////////////////////////////////////////disable auto complete
	
	$("#id_new-date").attr("autocomplete", "off");
	$("#id_new-total").attr("autocomplete", "off");
	$("#id_new-pic").attr("autocomplete", "off");
	$("#id_new-solo").attr("autocomplete", "off");
	$("#id_new-sic").attr("autocomplete", "off");
	$("#id_new-dual_r").attr("autocomplete", "off");
	$("#id_new-dual_g").attr("autocomplete", "off");
	$("#id_new-act_inst").attr("autocomplete", "off");
	$("#id_new-sim_inst").attr("autocomplete", "off");
	$("#id_new-app").attr("autocomplete", "off");
	$("#id_new-night").attr("autocomplete", "off");
	$("#id_new-xc").attr("autocomplete", "off");
	$("#id_new-day_l").attr("autocomplete", "off");
	$("#id_new-night_l").attr("autocomplete", "off");
	
	////////////////////////////////////////////////////////
	
	$("#new_flight_button").click(function(event) {			//make the popup when the new flight button is clicked
		prepare_new(true);
		fire_popup();
	});
	
	$("a.popup_link").click(function(){
	
    	close_all_small_popups()
    	
	    //find the position of the date link that was clicked
	    var pos = $(this).position();
	    
	    //the id of the flight
		var f_id = this.id.substr(1);
		
		//grab the small popup window and place it next to the cursor
		little_popup = $('#s' + f_id)
		little_popup.css('top', pos.top+10).css('left', pos.left)
		little_popup.show()
		
		return false
		
	});
	
	$("a.edit_popup_link").click(function(){
    	//make the edit popup when the link for it is clicked
		wipe_clean();
		close_all_small_popups();
		prepare_edit(true);
		fill_in_flight(this.id);
		fire_popup();
	});
});

function do_auto_button() {
	for(b=0;b<auto_button.length; b++)
		$("#id_new-" + auto_button[b]).val( $("#id_new-total").val() );
}

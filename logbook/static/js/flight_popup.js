d = new Date();
month = (d.getMonth()+1).toString().length < 2 ? "0" + (d.getMonth()+1) : (d.getMonth()+1);	//#add a leading zero if its only one digit, +1 because javascript is dum
day = (d.getDate()).toString().length < 2 ? "0" + (d.getDate()) : (d.getDate());

var todays_date = d.getFullYear() + "-" + month + "-" + day;

//////////////////////////////////////////////////////////////////

function prepare_new(wipe) {					    //prepares the new entry popup
	console.log('prepare_new');

	if(wipe) {
    	wipe_clean();
	    $("#id_new-date").val(todays_date);
	}
	
	$('.modal h3').text("New Flight");
	$("#submit_edit_flight").hide();
	$("#delete_flight").hide();
	$("#submit_new_flight").show();
}

function prepare_edit(wipe) {				//prepares the new entry popup
	if(wipe)
		wipe_clean();
	
	$('.modal h3').text("Edit Flight");
	$("#submit_new_flight").hide();
	$("#submit_edit_flight").show();
	$("#delete_flight").show();
}

function close_all_small_popups(){
    $(".small_popup").hide();
}

$(document).click(close_all_small_popups);

////////////////////////////////////////////////////////////////////////////////////////////////////////////////

$(document).ready(function() {
	
	$("#id_new-date, .date_picker").datepicker({	// add the date pickers
			dateFormat: "yyyy-mm-dd",
			yearRange: "-10:+1", 
			showOn: "button", 
			buttonImage: date_button, 
			buttonImageOnly: true,
			changeYear: true 
	}).addClass("embed");
	
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
	
	$("#new_flight").click(function(event) {			//make the popup when the new flight button is clicked
		prepare_new(true);
		fire_popup();
		console.log('new flight')
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
    	
    	id = "f" + this.id.substr(1);
    	
		wipe_clean();
		close_all_small_popups();
		prepare_edit(true);
		fill_in_flight(id);
		fire_popup();
	});
});

function do_auto_button() {
	for(b=0;b<auto_button.length; b++)
		$("#id_new-" + auto_button[b]).val( $("#id_new-total").val() );
}

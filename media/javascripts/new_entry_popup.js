d = new Date();
month = (d.getMonth()+1).toString().length < 2 ? "0" + (d.getMonth()+1) : (d.getMonth()+1);	//#add a leading zero if its only one digit, +1 because javascript is dum
day = (d.getDate()).toString().length < 2 ? "0" + (d.getDate()) : (d.getDate());

var todays_date = month + "/" + day + "/" + d.getFullYear();

//////////////////////////////////////////////////////////////////

function prepare_new_flight() {					//prepares the new entry popup
	wipe_clean();
	
	$('#titlebar').text("New Flight");
	$("#id_date").val(todays_date);
	$("#edit_buttons").hide();
	$("#new_buttons").show();
}

function prepare_edit_flight(wipe) {					//prepares the new entry popup
	if(wipe)
		wipe_clean();
	
	$('#titlebar').text("Edit Flight");
	$("#new_buttons").hide();
	$("#edit_buttons").show();
}

function prepare_and_fire_popup(type, id, date, remarks, flightarray, non_flying) {		//add values to the edit entry popup
	
	prepare_edit_flight();
	
	$("#id").val(id);
	$("#id_date").val(date);
	$("#id_plane").val(flightarray[0]);
	$("#id_route").val(flightarray[1]);
	$("#id_total").val(flightarray[2]);
	$("#id_pic").val(flightarray[3]);
	$("#id_solo").val(flightarray[4]);
	$("#id_sic").val(flightarray[5]);
	$("#id_dual_r").val(flightarray[6]);
	$("#id_dual_g").val(flightarray[7]);
	$("#id_act_inst").val(flightarray[8]);
	$("#id_sim_inst").val(flightarray[9]);
	$("#id_app").val(flightarray[10]);
	$("#id_night").val(flightarray[11]);
	$("#id_xc").val(flightarray[12]);
	$("#id_day_l").val(flightarray[13]);
	$("#id_night_l").val(flightarray[14]);

	$("#id_person").val(flightarray[15]);
	$("#id_remarks").val(remarks);

	$("#id_holding").attr("checked", flightarray[16]);	
	$("#id_tracking").attr("checked", flightarray[17]);
	
	$("#id_flight_review").attr("checked", flightarray[18]);
	$("#id_ipc").attr("checked", flightarray[19]);
	$("#id_pilot_checkride").attr("checked", flightarray[20]);
	$("#id_cfi_checkride").attr("checked", flightarray[21]);
		
	///////////////////////////////////
	
	$("#edit_buttons").show();
	$("#new_buttons").hide();
	
	///////////////////////////////////
	
	if($("#id_plane option[class=sim]:selected").length == 1)
		switch_to_sim();
	else
		switch_to_plane();
	
	fire_popup("popup");
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////

$(document).ready(function() {
	
	///////////////////////////////////////////
	
	$("#id_date").datepicker({							// add the date pickers
			dateFormat: "yy-mm-dd",
			yearRange: "-10:+1", 
			showOn: "button", 
			buttonImage: "/site-media/images/calendar.gif", 
			buttonImageOnly: true 
	}).addClass("embed");
	
	$("#id_non-date").datepicker({
			dateFormat: "mm/dd/yy",
			yearRange: "-10:+1", 
			showOn: "button", 
			buttonImage: "/site-media/images/calendar.gif", 
			buttonImageOnly: true 
	}).addClass("embed");
	
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
		prepare_new_flight();
		fire_popup("popup");
	});
	
	$("#logbook_table a").click(function(){			//make the popup when the date is clicked
		wipe_clean();
		prepare_edit_flight(true);
		fill_in_flight(this.id);
		fire_popup("popup");
	});
});

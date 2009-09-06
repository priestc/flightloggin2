function fill_in_flight(dom_id) {
	
	id = dom_id.substr(1);
	
	$("#id_id").val(id);
	$("#id_date").val(trim($("#tr" + id + " td.date_col span.unformatted_date").text()));
	
	
	$("#id_plane option:contains(" + trim($("#tr" + id + " td.plane_col").text()) + ")").attr("selected", "selected");
	
	$("#id_route").val(trim($("#tr" + id + " span.unformatted_route").text()));
	
	$("#id_total").val(trim($("#tr" + id + " td.total_col").text()));
	$("#id_pic").val(trim($("#tr" + id + " td.pic_col").text()));
	$("#id_sic").val(trim($("#tr" + id + " td.sic_col").text()));
	$("#id_solo").val(trim($("#tr" + id + " td.solo_col").text()));
	$("#id_dual_r").val(trim($("#tr" + id + " td.dual_r_col").text()));
	$("#id_dual_g").val(trim($("#tr" + id + " td.dual_g_col").text()));
	$("#id_xc").val(trim($("#tr" + id + " td.xc_col").text()));
	$("#id_night").val(trim($("#tr" + id + " td.night_col").text()));	
	$("#id_app").val(trim($("#tr" + id + " td.app_col").text()));
	
	if($("#tr" + id + " td.app_col:contains(T)").text())
		$("#id_tracking").attr("checked", "checked");
		
	if($("#tr" + id + " td.app_col:contains(H)").text())
		$("#id_holding").attr("checked", "checked");
	
	$("#id_night_l").val(trim($("#tr" + id + " td.night_l_col").text()));
	$("#id_day_l").val(trim($("#tr" + id + " td.day_l_col").text()));
	
	$("#id_remarks").val(trim($("#tr" + id + " td.remarks_col span.remarks").text()));
	
	$("#id_person").val(trim($("#tr" + id + " td.person_col").text()));
	
	//#############################################################################################
	
	if($("#tr" + id + " td.remarks_col span.flying_event:contains([Pilot Checkride])").text())
		$("#id_pilot_checkride").attr("checked", "checked");
		
	if($("#tr" + id + " td.remarks_col span.flying_event:contains([Instructor Checkride])").text())
		$("#id_cfi_checkride").attr("checked", "checked");
		
	if($("#tr" + id + " td.remarks_col span.flying_event:contains([IPC])").text())
		$("#id_ipc").attr("checked", "checked");
		
	if($("#tr" + id + " td.remarks_col span.flying_event:contains([Flight Review])").text())
		$("#id_flight_review").attr("checked", "checked");
		
    return
}

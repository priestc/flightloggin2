function fill_in_flight(dom_id) {
	
	id = dom_id.substr(1);
	
	$("#id_id").val(id);
	$("#id_date").val(trim($("#tr" + id + " td.date_col span.unformatted_date").text()));
	
	
	$("#id_plane option:contains(" + trim($("#tr" + id + " span.unformatted_plane").text()) + ")").attr("selected", "selected");
	
	$("#id_route").val(trim($("#tr" + id + " span.unformatted_route").text()));
	
	total_s = $("#tr" + id + " td.total_s_col").text()      //total (sim) column
	total = $("#tr" + id + " td.total_col").text()        //total column

	if (!total && total_s){
	    if(total_s[0] == "("){
	        total = total_s.substring(1,total_s.length-1);                 //remove parentheses if present
	    }
	    else
	        total = total_s                                             //no parentheses, use value as is
	}
	
	$("#id_total").val(trim(total));
	$("#id_pic").val(trim($("#tr" + id + " td.pic_col").text()));
	$("#id_sic").val(trim($("#tr" + id + " td.sic_col").text()));
	$("#id_solo").val(trim($("#tr" + id + " td.solo_col").text()));
	$("#id_dual_r").val(trim($("#tr" + id + " td.dual_r_col").text()));
	$("#id_dual_g").val(trim($("#tr" + id + " td.dual_g_col").text()));
	$("#id_xc").val(trim($("#tr" + id + " td.xc_col").text()));
	$("#id_night").val(trim($("#tr" + id + " td.night_col").text()));
		
	$("#id_app").val(trim($("#tr" + id + " td.app_col").text().replace(/[^0-9]/g, '')));
	
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


function page_totals(columns){
    COLON=false
    for(i=0;i<columns.length;i++) {
        column = columns[i]
        count = 0;
	    $("td." + column + "_col").each(function(){
            val = $(this).text();

            if(val.indexOf(":") > 0){
                COLON = true
                list=val.split(":");
                hour=list[0];
                mins=list[1];
                val = parseFloat(hour) + parseFloat(mins) / 60;
                //alert(val)
            }
            else
        	    val=parseFloat(val);
        	   
	        if(!isNaN(val))  
	          count = count + val;
        });

        if( column == 'app' || column == 'day_l' || column == 'night_l')
            result = count;
        else {
            if(COLON) {
                if(count == 0)
                    result = "00:00";
                else {
                    str=count.toString();
                    list=str.split(".");
                    hour=list[0];
                    dec="." + list[1];
                    mins = dec * 60
                    result = sprintf("%s:%02.0f", hour, mins);
                }
            }
            else
                result = count.toFixed(1);
        }

        $("tfoot #" + column + "_pt").html(result);
    }
}

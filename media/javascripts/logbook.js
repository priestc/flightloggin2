function fill_in_flight(dom_id) {
	
	var id = dom_id.substr(1);
	$("#id_new-id").val(id);
	
	var date = $("#f" + id + " span.data_date").text();
	$("#id_new-date").val(date);

	var plane = $("#f" + id + " span.data_plane").text();
	if( $('#id_new-plane select').length ){
    	$("#id_new-plane option:contains(" + plane + ")").attr("selected", "selected");
    } else {
        plane = plane.split(' ')[0]
        $("#id_new-plane").val(plane);
    }
	
	var route = $("#f" + id + " span.data_route").text();
	$("#id_new-route").val(route);
	
	var total = $("#f" + id + " span.data_total").text();
    $("#id_new-total").val(total);

    var pic = $("#f" + id + " span.data_pic").text();
	$("#id_new-pic").val(pic);
	
	var sic = $("#f" + id + " span.data_sic").text();
	$("#id_new-sic").val(sic);
	
	var xc = $("#f" + id + " span.data_xc").text();
	$("#id_new-xc").val(xc);
	
	var solo = $("#f" + id + " span.data_solo").text();
	$("#id_new-solo").val(solo);
	
	var dual_r = $("#f" + id + " span.data_dual_r").text();
	$("#id_new-dual_r").val(dual_r);
	
	var dual_g = $("#f" + id + " span.data_dual_g").text();
	$("#id_new-dual_g").val(dual_g);

	var act_inst = $("#f" + id + " span.data_act_inst").text();
	$("#id_new-act_inst").val(act_inst);
	
	var sim_inst = $("#f" + id + " span.data_sim_inst").text();
	$("#id_new-sim_inst").val(sim_inst);
	
	var night_l = $("#f" + id + " span.data_night_l").text();
	$("#id_new-night_l").val(night_l);
	
	var night = $("#f" + id + " span.data_night").text();
	$("#id_new-night").val(night);
	
	var day_l = $("#f" + id + " span.data_day_l").text();
	$("#id_new-day_l").val(day_l);

	var app = $("#f" + id + " span.data_app").text().replace(/[^0-9]/g, '');
	$("#id_new-app").val(app);
	
	var person = $("#f" + id + " span.data_person").text();
	$("#id_new-person").val(person);
	
	//####################################################
	
	if($("#f" + id + " span.data_remarks span.flying_event:contains([Pilot Checkride])").text())
		$("#id_new-pilot_checkride").attr("checked", "checked");
		
	if($("#f" + id + " span.data_remarks span.flying_event:contains([Instructor Checkride])").text())
		$("#id_new-cfi_checkride").attr("checked", "checked");
		
	if($("#f" + id + " span.data_remarks span.flying_event:contains([IPC])").text())
		$("#id_new-ipc").attr("checked", "checked");
		
	if($("#f" + id + " span.data_remarks span.flying_event:contains([Flight Review])").text())
		$("#id_new-flight_review").attr("checked", "checked");
		
	if($("#f" + id + " span.data_app:contains(T)").text())
		$("#id_new-tracking").attr("checked", "checked");
		
	if($("#f" + id + " span.data_app:contains(H)").text())
		$("#id_new-holding").attr("checked", "checked");
	
	// must be at the bottom because it removes the flying events from the dom	
	var clone = $("#f" + id + " span.data_remarks");
	$("span.flying_event", clone).remove();
	var remarks = clone.text();
	$("#id_new-remarks").val(trim(remarks));	
		
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
                    if(list[1]){
                        dec="." + list[1];
                        mins = dec * 60;
                    } else
                        mins = 0;
                        
                    result = sprintf("%s:%02.0f", hour, mins);
                }
            }
            else
                result = count.toFixed(1);
        }

        $("tfoot #" + column + "_pt").html(result);
    }
}

function cleanup_filter_get() {
    // Remove all unused form elements by setting disabled=disabled so the
    // variable isn't passed onto the URL which just clutters things up
    
    numeric_fields = ['pic', 'sic', 'dual_g', 'dual_r',
                       'xc', 'total', 'line_dist', 'p2p',
                       'max_width', 'app', 'day_l', 'night_l',
                       'sim_inst','act_inst','night','solo'];
    
    for(var a=0; a < 16; a++) {
        
        field = numeric_fields[a];
        
        if($("#filterform input[name=" + field + "]").val() == '') {
        
            $("#filterform input[name=" + field + "]").attr('disabled', 'disabled');
            $("#filterform select[name=" + field + "_op]").attr('disabled', 'disabled');
        }
    }
    
    text_fields = ['start_date', 'end_date', 'person', 'remarks',
                   'route__fancy_rendered', 'plane__tags', 'plane__tailnumber'];
    
    for(var b=0; b < 7; b++) {
    
        field = text_fields[b];
        
        if($("#filterform input[name=" + field + "]").val() == '') {
            $("#filterform input[name=" + field + "]").attr('disabled', 'disabled');
        }
    }
    
    if($("#filterform select[name=plane__type]").val() == '') {
        $("#filterform select[name=plane__type]").attr('disabled', 'disabled');
    }
    
    if($("#filterform select[name=plane__cat_class]").val() == '') {
        $("#filterform select[name=plane__cat_class]").attr('disabled', 'disabled');
    }
}

$(document).ready(function() {
    
    $(".filter_submit").click(function() {
        cleanup_filter_get();
        
        if (this.id == 'earth') {
            $("#filterform [name=maps]").remove();
        }


        if (this.id == 'maps') {
            $("#filterform [name=earth]").remove();
        }
           
        if (this.id == 'logbook') {
            $("#filterform [name=maps]").remove();
            $("#filterform [name=earth]").remove();
        }
    });
    
});









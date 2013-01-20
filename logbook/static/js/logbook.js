function fill_in_flight(dom_id) {
	
	var id = dom_id.substr(1);
	$("#id_new-id").val(id);
	
	var date = $("#f" + id + " span.data_date").text();
	$("#id_new-date").val(date);

	var plane = $("#f" + id + " span.data_plane").text();
	if( $('select#id_new-plane').length > 0 ){
	    // if theres a select with the ID of new-plane, then use this method
	    // to fill in the plane
    	$("#id_new-plane option:contains(" + plane + ")").attr("selected", "selected");
    } else {
        // otherwise, use this other method, because the plane field is
        // a textbox
        plane = plane.split(' ')[0]
        if(plane == 'UNKNOWN') {
            // unknown plane becomes blank to aviod creating a new
            // plane called 'UNKNOWN'
            plane = '';
        }
        $("#id_new-plane").val(plane);
    }
	
	var route = $("#f" + id + " span.data_route").text();
	$("#id_new-route_string").val(route);
	
	var fuel_burn = $("#f" + id + " span.data_fuel_burn").text();
	$("#id_new-fuel_burn").val(fuel_burn);
	
	var total = $("#f" + id + " span.data_raw_total").text();
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
	
	if($("#f" + id + " span.data_remarks span.remarks_tag:contains([Pilot Checkride])").text())
		$("#id_new-pilot_checkride").attr("checked", "checked");
	
	if($("#f" + id + " span.data_remarks span.remarks_tag:contains([Instructor Checkride])").text())
		$("#id_new-cfi_checkride").attr("checked", "checked");
		
	if($("#f" + id + " span.data_remarks span.remarks_tag:contains([IPC])").text())
		$("#id_new-ipc").attr("checked", "checked");
		
	if($("#f" + id + " span.data_remarks span.remarks_tag:contains([Flight Review])").text())
		$("#id_new-flight_review").attr("checked", "checked");
		
	if($("#f" + id + " span.data_app:contains(T)").text())
		$("#id_new-tracking").attr("checked", "checked");
		
	if($("#f" + id + " span.data_app:contains(H)").text())
		$("#id_new-holding").attr("checked", "checked");
		
	return
}


function page_totals(columns){
    COLON=false
    for(i=0;i<columns.length;i++) {
        // go through each column
        column = columns[i]
        count = 0;
	    $("td." + column + "_col").each(function(){
	        // go through each cell in this column
            val = $(this).text();

            if(val.indexOf(":") > 0){
                // this cell is formatted with a colon, calculate numbers accordingly
                COLON = true
                list=val.split(":");
                hour=list[0];
                mins=list[1];
                val = parseFloat(hour) + parseFloat(mins) / 60;
            }
            else
        	    val=parseFloat(val);
        	   
	        if(!isNaN(val)) {
	            // add to count only if there is a value there  
	            count = count + val;
	        }
        });
        
        // now that we have the totals, format them correctly
        
        if( column == 'app' || column == 'day_l' || column == 'night_l')
            result = count;
            
        else if (column == 'line_dist' || column == 'gallons') {
            result = sprintf("%02.1f", parseFloat(count));
        }
        
        else {
            if(COLON) {
                if(count == 0)
                    result = "0:00";
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
                       'sim_inst','act_inst','night','solo',
                       'gallons','speed'];
    
    for(var a=0; a < 18; a++) {
        
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
    
    $("#submit_edit_flight").click(function() {
    
        $("#new_entry_form").attr("action", edit_url)
    
    });
    
    $("#submit_new_flight").click(function() {
    
        $("#new_entry_form").attr("action", new_url)
    
    });
    
    $("#delete_flight").click(function() {
    
        $("#new_entry_form").attr("action", delete_url)
    
    });
    
    
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









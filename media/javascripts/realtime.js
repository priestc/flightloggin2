$(function(){

    $('#epiclock').epiclock(
        {
         gmt: false,
         offset: {seconds: SERVER_OFFSET},
         format: "M{ }d{ }Y { <br>} H:i:s { UTC}"
        }
    );

    $.epiclock();
  
});


// return a string representation of the date and time
function get_time_now() {
    raw_str = $('#epiclock').text();
    
    date = dateFormat(raw_str.substr(0,11), "yyyy-mm-dd")
    time = raw_str.substr(12,8).replace(/:/g, ".")
    
    return date + "--" + time
    
}

function switch_to_on_duty(duty_id) {
// at the dom elements to display the page for when the user is on duty

    // set the pk of the duty object in teh database to the id of
    // the DOM element
    $("#hidden_duty_box").attr("id", "duty_" + duty_id).show();
    $("#go_on_duty").hide();
}

function switch_to_off_duty(duty_id) {

    $("#duty_" + duty_id).attr("id", "hidden_duty_box");
    $("#go_on_duty").show();
}


$(document).ready(function() {

    $.ajaxSetup ({
	    cache: false
    });

    $("#go_on_duty").click(function() {
        str = get_time_now()
        $("#id_start").val(str);
        
        $.getJSON(URLS['go_on_duty'], {timestamp: str}, function(json){
        
            switch_to_on_duty(json.duty_id)
        
        });
                  
    });

    $("#go_off_duty").click(function() {
        str = get_time_now()
        $.getJSON(URLS['go_off_duty'], {timestamp: str}, function(json){
        
            switch_to_off_duty(json.duty_id);
        
        });
    });

});

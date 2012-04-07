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
    var raw_str = $('#epiclock').text();
    
    var date = dateFormat(raw_str.substr(0,11), "yyyy-mm-dd")
    var time = raw_str.substr(12,8).replace(/:/g, ".")
    
    return date + "--" + time
    
}

function add_start_block(duty_id) {

    // select the duty element
    var duty = $("#duty_" + duty_id)

    // create the new block button
    button = $('<input>').attr("type", "button")
                         .attr("id", "start_block_" + duty_id)
                         .attr("value", "Start Block")
    
    // add button to a div
    var html = $('<div class="block_div"></div>').append(button)
    
    // add the "start block" button div to the duty box
    duty.append(html);
}

function switch_to_on_duty(json) {
    // set the pk of the duty object in teh database to the id of
    // the DOM element
    $("#hidden_duty_box").attr("id", "duty_" + json.duty.id).show();
    
    // hide the "go on duty" button
    $("#go_on_duty").hide();
    
    // fill in the "went on duty" textbox
    $("#on_duty_time").val(json.duty.start);
    
    add_start_block(json.duty.id);
}

function switch_to_off_duty(json) {

    // change the id of this element so it is hidden again
    $("#duty_" + json.duty.id).attr("id", "hidden_duty_box");
    
    // show the "go on duty" button
    $("#go_on_duty").show();
    
    $(".block_div").remove();
}


$(document).ready(function() {

    $.ajaxSetup ({
	    cache: false
    });
    
    
    $.getJSON(URLS['get_master_duty'], "", function(json){
       var a=1+1
    });
    

    $("#go_on_duty").click(function() {
        var str = get_time_now()
        $("#id_start").val(str);
        
        $.getJSON(URLS['go_on_duty'], {timestamp: str}, function(json){

            if (json.result == 'ok') {
                switch_to_on_duty(json);
            }
            else {
                alert(json.result);
            }
        
        });
                  
    });

    $("#go_off_duty").click(function() {
        str = get_time_now()
        $.getJSON(URLS['go_off_duty'], {timestamp: str}, function(json){
        
            if (json.result == 'ok') {
                switch_to_off_duty(json);
            }
            
            else {
                alert(json.result);
            }
        });
    });
    
    // all "start block" buttons
    $('input').click(function() {
        duty_id = this.id.substr(12);
        alert(duty_id);
    
    });














});

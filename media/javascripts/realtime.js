$(function(){

    $('#epiclock').epiclock(
        {
         gmt: false,
         offset: {seconds: SERVER_OFFSET},
         format: "M{ }d{ }Y {<br>} H:i:s { UTC}"
        }
    );

    $.epiclock();
  
});

function get_time_now() {
    raw_str = $('#epiclock').text();
    
    date = dateFormat(raw_str.substr(0,11), "yyyy-m-d")
    time = raw_str.substr(11,8)
    
    //alert(date);
    //alert(time);
    
    return date + " " + time
    
}


$(document).ready(function() {

    $("#on_duty").click(function() {
    
        str = get_time_now()
        $("#id_start").val(str);
    });

    $("#off_duty").click(function() {
    
        str = get_time_now()
        $("#id_end").val(str);
    });

});

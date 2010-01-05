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
    client_time = new Date();
    client_ts = client_time.getTime();
    adjusted_ts = client_ts + SERVER_OFFSET;
    
    adjusted_time = new Date();
    adjusted_time.setTime(adjusted_ts);
    
    //alert("orig ts: " + client_time.format("isoDateTime"));
    //alert("after adj: " + adjusted_time.format("isoDateTime"));

    return adjusted_time.format("UTC:yyyy-mm-dd h:MM:ss");
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

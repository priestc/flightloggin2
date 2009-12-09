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

$(document).ready(function() {

    $("#on_duty").click(function() {
        d = new Date();
        current_time = d.getTime() + SERVER_OFFSET;
        //alert(d.toUTCString(current_time) + "--" + SERVER_OFFSET);
        str = d.toUTCString(current_time)
        $("#id_start").val(str);
    });

    $("#off_duty").click(function() {
    
        alert("off duty");
    
    });

});

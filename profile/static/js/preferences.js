$(document).ready(function() {
    $("#id_dob").datepicker({
	        dateFormat: "yy-mm-dd",
	        yearRange: "1900:2008", 
	        showOn: "button", 
	        buttonImage: MEDIA_URL + "/images/calendar.gif", 
	        buttonImageOnly: true,
	        changeYear: true
    }).addClass("embed");
    
    $('.verify_flights').click(function() {
        if ( $("input.verify_flights:not(:checked)").size() == 0 )
            $('#delete_all_flights').removeAttr("disabled")
        else
            $('#delete_all_flights').attr("disabled", "disabled")
    });
    
    $('.verify_nonflights').click(function() {
        if ( $("input.verify_nonflights:not(:checked)").size() == 0 )
            $('#delete_all_nonflights').removeAttr("disabled")
        else
            $('#delete_all_nonflights').attr("disabled", "disabled")
    });
    
    $('.verify_unusedplanes').click(function() {
        if ( $("input.verify_unusedplanes:not(:checked)").size() == 0 )
            $('#delete_unusedplanes').removeAttr("disabled")
        else
            $('#delete_unusedplanes').attr("disabled", "disabled")
    });
    
    $('.verify_everything').click(function() {
        if ( $("input.verify_everything:not(:checked)").size() == 0 )
            $('#delete_everything').removeAttr("disabled")
        else
            $('#delete_everything').attr("disabled", "disabled")
    });	
});

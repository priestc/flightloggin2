function wipe_clean() {

    // uncheck all checkboxes and clear all input boxes
	$("#popup input[type=text], #popup textarea, #popup select").val("");
	$("#popup input[type=checkbox]").attr("checked", "");
	
	// remove the error messages
	$("#popup td#new_error_cell").text("");
	$("#popup td#edit_error_cell").text("");
	$("#popup td#display_error_cell").text("");
	$("#popup ul.errorlist").before("<br />").remove();
}

function fire_popup() {
    // a way to figure out how much the user has scrolled
    // that works in both IE as well as the standards browsers
    
    var scrolledX, scrolledY;

    if( self.pageYOffset ) {
        scrolledX = self.pageXOffset;
        scrolledY = self.pageYOffset;
    }
    
    else if( document.documentElement && document.documentElement.scrollTop ) {
        scrolledX = document.documentElement.scrollLeft;
        scrolledY = document.documentElement.scrollTop;
    }
    
    else if( document.body ) {
        scrolledX = document.body.scrollLeft;
        scrolledY = document.body.scrollTop;
    }

    var p = $('#popup');
    p.centerScreen();
    p.draggable({ 
        zIndex: 20,
        cursor: 'move',
        opacity: 1.0,
        handle: '#dragbar'
    });

    var t = p.css("top");
    p.css("top", scrolledY + parseInt(t));
    p.show();
}

$(document).ready(function() {

    $("#close_x").click(function(event) {
        $("#popup").hide("slow");
    });

    // fire popup if an anything is in the error cell
    // and it's the new flight that caused the error
    if( $("td#new_error_cell").text() != "" ) {     
        prepare_new();
        fire_popup();
    }

    // ...it's the edit flight popup that caused the error
    if( $("td#edit_error_cell").text() != "") {
        prepare_edit();   
        fire_popup();
    }
});









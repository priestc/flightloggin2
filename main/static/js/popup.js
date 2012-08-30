function wipe_clean() {
    // uncheck all checkboxes and clear all input boxes
    $(".modal input[type=text], .modal textarea, .modal select").val("");
    $(".modal input[type=checkbox]").attr("checked", "");
	
    // remove the error messages
    $(".modal td#new_error_cell").text("");
    $(".modal td#edit_error_cell").text("");
    $(".modal td#display_error_cell").text("");
    $(".modal ul.errorlist").before("<br />").remove();
}

function fire_popup() {
    // a way to figure out how much the user has scrolled
    // that works in both IE as well as the standards browsers
    $('.modal').modal();
}

$(document).ready(function() {

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
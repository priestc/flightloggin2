function render_line_graph(ext) {

    column = $("#line_column").val();
    
    //change all dashes to dots
    start = $("#line_start").val().replace(/-/g,'.');
    end = $("#line_end").val().replace(/-/g,'.');
    
    if($("#do_rate:checked").val()){
        rate="rate";
    }
    else {
        rate="norate";        
    }
    
    if(start && end)
        url = sprintf("linegraph/%s/%s-%s/%s.%s",column, start, end, rate, ext)
        
    else
        url = sprintf("linegraph/%s/%s.%s",column, rate, ext)
        
    if(ext=="png")
  	    $("#image").attr("src", url).css("display", "block")
  	else if(ext=="svg")
  	    window.open(url) //$("#svg_link").attr("href", url)

}

$(document).ready(function() {
    
    render_line_graph('png');
    
    $(".render_button").click(function() {
    
        ext=$(this).attr('class').split(' ').slice(-1);
    
        if(this.id == "line_graph")
            render_line_graph(ext);
        
        //if(this.id == "bar_graph")
        //   render_bar_graph(ext);
    
    });
    
    $(".date").datepicker({			// add the date pickers
            dateFormat: "yy-mm-dd",
            yearRange: year_range, 
            showOn: "button", 
            buttonImage: date_button,
            buttonImageOnly: true,
            changeYear: true
    }).addClass("embed");

});

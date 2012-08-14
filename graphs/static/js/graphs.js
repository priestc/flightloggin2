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
    
    if($("#filter_spikes:checked").val()){
        spikes="nospikes";
    }
    else {
        spikes="spikes";        
    }
    
    var username = location.href.split('/')[4];

    if(start && end)
        url = sprintf("/%s/linegraph/%s/%s-%s/%s-%s.%s",username, column, start, end, rate, spikes, ext)
        
    else
        url = sprintf("/%s/linegraph/%s/%s-%s.%s",username, column, rate, spikes, ext)
        
    if(ext=="png")
  	    $("#image").attr("src", url).css("display", "block")
  	else if(ext=="svg")
  	    window.open(url)

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

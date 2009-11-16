function render_bar_graph(ext) {

    column = $("#bar_column").val();
    agg = $("#agg").val();
    
    url = sprintf("bargraph/%s/by-%s.png",column, agg);
        
    $("#image").attr("src", url).css("display", "block");

}

$(document).ready(function() {
    
    $(".render_button").click(function() {
    
        render_bar_graph();
    
    });
});

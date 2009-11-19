function render_bar_graph() {

    column = $("#bar_column").val();
    agg = $("#agg").val();
    func = $("#func").val();
    
    url = sprintf("bargraph/%s/%s/by-%s.png", column, func, agg);
        
    $("#image").attr("src", url).css("display", "block");

}

$(document).ready(function() {

    render_bar_graph();
    
    $(".render_button").click(function() {
    
        render_bar_graph();
    
    });
});

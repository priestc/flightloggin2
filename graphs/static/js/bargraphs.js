function render_bar_graph() {
    
    url = sprintf("bargraph/%s/%s/by-%s.png",
                  $("#bar_column").val(),
                  $("#func").val(),
                  $("#agg").val());
        
    $("#image").attr("src", url).css("display", "block");

}

$(document).ready(function() {

    render_bar_graph();
    
    $(".render_button").click(function() {
    
        render_bar_graph();
    
    });
});

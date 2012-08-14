function render_bar_graph() {
    var username = location.href.split('/')[4];

    url = sprintf("/%s/bargraph/%s/%s/by-%s.png",
                  username,
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

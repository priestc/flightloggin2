$(document).ready(function() {
    $('a.graph_popup').click(function() {
    
        clear_popup()
        var image_url = "/stats_graph/" + this.id + ".png";
        var pos = $(this).position();
        
        $('#popup_div').css('top', pos.top+10)
                       .css('right', pos.right+10);
        
        $('#popup_div img').attr("src", image_url);
        
        $('#popup_div').show();
        
        return false
    });
    
    
});

function clear_popup() {
    $('#popup_div').hide();
}

$(document).click(clear_popup)

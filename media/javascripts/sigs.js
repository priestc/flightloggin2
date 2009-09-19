var url = "sigs/pic.png"

$(document).ready(function() {
	$("#generate_button").click(function(event) {
	    get_url()
		generate_sig();
		copy_url();
	});
});

function generate_sig() {
    $("#sig_image").attr("src", url);
}

function copy_url() {
    $("#sig_url").text("http://flightlogg.in/" + url);
}

function get_url() {
    
    fields = []

    $(".checktable input:checked").each(function() {
        fields.push(this.id)
    });
    
    url = "sigs/" + fields.join("-") + ".png"

}

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
    $("#sig_url").text(url);
}

function get_url() {
    
    fields = []

    $("#checktable input:checked").each(function() {
        fields.push(this.id)
    });
    
    var p = location.href.split("/");
    p[p.length-1]="";
    p=p.join("/");
    
    url = p + "sigs/" + fields.join("-") + ".png"
}

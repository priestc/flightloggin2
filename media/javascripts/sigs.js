
// the domain name of the page
var p = location.href.split("/");
p[p.length-1]="";
p=p.join("/");


// the default to show
var url = p + "sigs/pic.png";

$(document).ready(function() {

    generate();

	$("#generate_button").click(generate);
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
        fields.push(this.id);
    });
    
    $("input[name='font']:checked").each(function() {
        font = $(this).val();
    });
    
    $("input[name='size']:checked").each(function() {
        size = $(this).val();
    });
    
    $("input[name='logo']:checked").each(function() {
        logo = $(this).val();
    });
    
    url = sprintf("%s%s-sigs/%s-%s/%s.png", p, logo, font, size, fields.join("-") )
}

function generate(event) {
    get_url();
	generate_sig();
	copy_url();
}

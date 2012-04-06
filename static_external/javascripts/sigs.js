
// the domain name of the page
var p = location.href.split("/");
p[p.length-1]="";
p=p.join("/");


// the default to show
var url = p + "sigs/pic.png";

$(document).ready(function() {

    generate_totals();

	$("#generate_totals").click(generate_totals);
	$("#generate_lastx").click(generate_lastx);
});

function generate_sig() {
    $("#sig_image").attr("src", url);
}

function copy_url() {
    $("#sig_url").text(url);
}

function get_url(type) {
    
    totals_fields = []
    $("#checktable input:checked").each(function() {
        totals_fields.push(this.id);
    });
    
    $("#radiotable input:checked").each(function() {
        lastx_field = this.id;
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
    
    if(type == 'totals'){
        sig_type = sprintf("%s-sigs", logo);
        items = totals_fields.join("-");
    }
    
    if(type == 'lastx') {
        sig_type = "ds-sigs";
        items = lastx_field;
    }
    url = sprintf("%s%s/%s-%s/%s.png", p, sig_type, font, size, items )
}

function generate_totals(event) {
    get_url('totals');
	generate_sig();
	copy_url();
}

function generate_lastx(event) {
    get_url('lastx');
	generate_sig();
	copy_url();
}

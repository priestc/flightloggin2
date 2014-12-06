var map;

$(document).ready(function() {
	var chicago = new google.maps.LatLng(41.875696,-87.624207);
	var mapOptions = {
		zoom: 11,
		center: chicago
	}
	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

	var ctaLayer = new google.maps.KmlLayer({url: kml_url});
	ctaLayer.setMap(map);

	if (map.getZoom() > 6) {
		map.setZoom(6)
	}

});

$(document).ready(function() {

    $('#toggle a').toggle(function() {

        $(this).text("Hide Map Key");
        $('#key').show('slow');

    },
    function() {

        $(this).text("Show Map Key");
        $('#key').hide('slow');

    });

});

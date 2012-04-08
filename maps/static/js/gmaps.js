function initialize()
{	
	if (GBrowserIsCompatible())
	{
		map = new GMap2(document.getElementById("gmap"));
		
		var polyOptions = {geodesic:true};
		
		map.addMapType(G_PHYSICAL_MAP);
		map.setMapType(G_PHYSICAL_MAP);
		
		map.setCenter(new GLatLng(10,0), 2);
		
		map.addControl(new GLargeMapControl3D());
		map.addControl(new GHierarchicalMapTypeControl());
		map.enableContinuousZoom();
	}
}

var map;

$(document).ready(function() {
	
	initialize();
	
	var kml = new GGeoXml(kml_url, function(){
	
		if (kml.loadedCorrectly())
		{
			map.addOverlay(kml);
			kml.gotoDefaultViewport(map)
		}
		
		if (map.getZoom() > 6)
			map.setZoom(6)
	});

	
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

window.onunload = GUnload;

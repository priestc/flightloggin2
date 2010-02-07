function initialize()
{	
	if (GBrowserIsCompatible())
	{
		map = new GMap2(document.getElementById("gmap"));
		
		var polyOptions = {geodesic:true};
		
		map.addMapType(G_PHYSICAL_MAP);
		map.setMapType(G_PHYSICAL_MAP);
		
		map.setCenter(new GLatLng(10,0), 2);
		
		map.addControl(new GSmallZoomControl3D());
		map.addControl(new GHierarchicalMapTypeControl());
		map.enableContinuousZoom();
	}
}

var map;

$(document).ready(function() {
	
	initialize();
	
	var kml = new GGeoXml(routes_kml_url, function(){
	
		if (kml.loadedCorrectly())
		{
			map.addOverlay(kml);
			kml.gotoDefaultViewport(map)
		}
		
		if (map.getZoom() > 6)
			map.setZoom(6)
	});

	
});

window.onunload = GUnload;

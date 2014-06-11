	var map, infowindow, routeData, chainages, sericeRef;
	function initialize() {
		getDataForService();
	}

    function getNextStops(user_lat, user_long) {
		var serviceRef = $("#serviceRef").val(); 
        direction = "A";
        no_stops = 5;
        data = {"user_lat":user_lat, "user_long":user_long, "service_ref": serviceRef, "direction":direction, "no_stops":no_stops};
		// Grab data for service
		$.ajax({
			url: "cgi-bin/getNextStops.py",
			type: "GET",
			datatype: "json",
			data: data,
			async: false,
			success: function(data) {
                stops = JSON.parse(data);
                for (i = 0; i < stops.length; i++) {
                    addNextStopMarker(stops[i]);
                }
                //addStopMarker();
			}
		});
    }

    function addNextStopMarker(stop) {
        latlng = new google.maps.LatLng(stop['x'],stop['y']);
        var marker = new google.maps.Marker({ position: latlng});
        iconFile = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'; 
        marker.setIcon(iconFile) 
		google.maps.event.addListener(marker, "click", function() {
            if (infowindow) infowindow.close();
            content = "Name: " + stop['name']
            infowindow = new google.maps.InfoWindow({ content: content });
            infowindow.open(map,marker);
        });
		marker.setMap(map);
	}

	function getClosestStopTo(order, chainage) {
		var serviceRef = $("#serviceRef").val(); 
		// Grab data for service
		$.ajax({
			url: "cgi-bin/service_stop_test.py",
			type: "GET",
			datatype: "json",
			data: {"service_ref": serviceRef, "order":order, "chainage":chainage},
			async: false,
			success: function(data) {
                addStopMarker(JSON.parse(data));
			}
		});
	}

    function addStopMarker(stop) {
        latlng = new google.maps.LatLng(stop['x'],stop['y']);
        var marker = new google.maps.Marker({ position: latlng});
        iconFile = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'; 
        marker.setIcon(iconFile) 
		google.maps.event.addListener(marker, "click", function() {
            if (infowindow) infowindow.close();
            content = "Name: " + stop['name']
            infowindow = new google.maps.InfoWindow({ content: content });
            infowindow.open(map,marker);
        });
		marker.setMap(map);
	}

	function getDataForService() {
		// Grab data for service
		var serviceRef = $("#serviceRef").val(); 
		$.ajax({
			url: "cgi-bin/drawRoute.py",
			type: "GET",
			datatype: "json",
			data: {"ref": serviceRef},
			async: false,
			success: function(data) {
                routeData = JSON.parse(data);
				drawMap();
			}
		});
	}

	function drawMap() {
		var centerlatlng = new google.maps.LatLng(55.951891,-3.194329);
        if (routeData.length>0) centerlatlng = new google.maps.LatLng(routeData[0]['x'], routeData[0]['y']);
		var myOptions = { zoom: 13, center: centerlatlng, mapTypeId: google.maps.MapTypeId.ROADMAP };
		map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
        addMarkersForPoints(routeData);
        addPathForPoints(routeData);
	}

    function addMarkersForPoints(points) {
		for (var i = 0; i < points.length; i++) {
            point = points[i];
			latlng = new google.maps.LatLng(point['x'],point['y']);
			addMarker(point);
        }
    }
	
    function addMarker(point) {
        latlng = new google.maps.LatLng(point['x'],point['y']);
        var marker = new google.maps.Marker({ position: latlng});
		google.maps.event.addListener(marker, "click", function() {
            content = "Order: " + point['order'].toString() + "<br />Chainage: " + point['chainage'].toString() + "<br /> <a onclick='getClosestStopTo("+point['order']+","+point['chainage']+");' >Show closest stop</a> <br /> <a onclick='getNextStops("+point['loc'][0]+","+point['loc'][1]+");' >Get next stops</a>";
            if (infowindow) infowindow.close();
            infowindow = new google.maps.InfoWindow({ content: content });
            infowindow.open(map,marker);
        });
		marker.setMap(map);
	}

    function addPathForPoints(points) {
        colors = ["AliceBlue","AntiqueWhite","Aqua","Aquamarine","Azure","Beige","Bisque","Black","BlanchedAlmond","Blue","BlueViolet","Brown","BurlyWood","CadetBlue","Chartreuse","Chocolate","Coral","CornflowerBlue","Cornsilk","Crimson","Cyan","DarkBlue","DarkCyan","DarkGoldenRod","DarkGray","DarkGrey","DarkGreen","DarkKhaki","DarkMagenta","DarkOliveGreen","Darkorange","DarkOrchid","DarkRed","DarkSalmon","DarkSeaGreen","DarkSlateBlue","DarkSlateGray","DarkSlateGrey","DarkTurquoise","DarkViolet","DeepPink","DeepSkyBlue","DimGray","DimGrey","DodgerBlue","FireBrick","FloralWhite","ForestGreen","Fuchsia","Gainsboro","GhostWhite","Gold","GoldenRod","Gray","Grey","Green","GreenYellow","HoneyDew","HotPink","IndianRed","Indigo","Ivory","Khaki","Lavender","LavenderBlush","LawnGreen","LemonChiffon","LightBlue","LightCoral","LightCyan","LightGoldenRodYellow","LightGray","LightGrey","LightGreen","LightPink","LightSalmon","LightSeaGreen","LightSkyBlue","LightSlateGray","LightSlateGrey","LightSteelBlue","LightYellow","Lime","LimeGreen","Linen","Magenta","Maroon","MediumAquaMarine","MediumBlue","MediumOrchid","MediumPurple","MediumSeaGreen","MediumSlateBlue","MediumSpringGreen","MediumTurquoise","MediumVioletRed","MidnightBlue","MintCream","MistyRose","Moccasin","NavajoWhite","Navy","OldLace","Olive","OliveDrab","Orange","OrangeRed","Orchid","PaleGoldenRod","PaleGreen","PaleTurquoise","PaleVioletRed","PapayaWhip","PeachPuff","Peru","Pink","Plum","PowderBlue","Purple","Red","RosyBrown","RoyalBlue","SaddleBrown","Salmon","SandyBrown","SeaGreen","SeaShell","Sienna","Silver","SkyBlue","SlateBlue","SlateGray","SlateGrey","Snow","SpringGreen","SteelBlue","Tan","Teal","Thistle","Tomato","Turquoise","Violet","Wheat","White","WhiteSmoke","Yellow","YellowGreen"];
        chainages = {}

		for (var i = 0; i < points.length; i++) {
            point = points[i];
            chainage = point['chainage'];
            if (!chainages[chainage])
                chainages[chainage] = [];
            chainages[chainage].push(point);
		}

        for (var i = 0; i < Object.keys(chainages).length; i++) {
            chainage = Object.keys(chainages)[i];
            addPath(chainages[chainage], colors[i]);
        }
    }

	function addPath(points,color) {

        latLongs = [];
        for (var i = 0; i < points.length; i++) {
            latLongs.push(new google.maps.LatLng(points[i]['x'],points[i]['y']));
        }

		var Path = new google.maps.Polyline({
			clickable: false,
			path: latLongs,
			strokeColor: color,
			strokeOpacity: 1.000000,
			strokeWeight: 2
		});
		Path.setMap(map);
	}


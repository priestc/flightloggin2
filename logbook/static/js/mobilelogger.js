function get_current_time() {
    // return the current state of the UTC clock, parsed to integers.
    var t = $("#clock").text().split(':');
    return [parseInt(t[0]), parseInt(t[1]), parseInt(t[2])]
}

function get_location(cb) {
    navigator.geolocation.getCurrentPosition(cb);
}

function add_times(t1, t2) {
    return normalize_time([t1[0] + t2[0], t1[1] + t2[1], t1[2] + t2[2]])
}

function to_julian(tup) {
    // minutes since midnight, tup = [hour, minutes, seconds]
    return (tup[0] * 60) + tup[1] + (tup[2] / 60);
}

function is_it_day_or_night(mode) {
    var t = get_current_time();
    var night, day;

    if(mode == 'land') {
        // use civil twilight because thats how the FAA defines night landings
        night = to_julian(ect);
        day = to_julian(mct);
    } else if(mode == 'flight') {
        // use sunset and sunrise because thats how the FAA defines night and day hour logging.
        night = to_julian(sunset);
        day = to_julian(sunrise);
    } else {
        throw;
    }

    if(to_julian(t) > day && to_julian(t) < night) {
        return 'day'
    } else {
        return 'night'
    }
}

function tuple_to_display(tup) {
    var dec = (tup[0] + (tup[1] + (tup[2] / 60)) / 60).toFixed(1)
    return dec
}

function get_difference(t1, t2) {
    // get the difference between two clock times.
    // t1 = ["05", "23", "13"] t2 = ["06", "50", "02"]
    if(t1[0] > t2[0]) {
        // clock has spanned 00:00, calculate differently
        var h0 = 23 - t1[0];
        var m0 = 59 - t1[1];
        var s0 = 60 - t1[2];
        var h = t2[0] + h0;
        var m = t2[1] + m0;
        var s = t2[2] + s0;

    } else {
        var h = t2[0] - t1[0];
        var m = t2[1] - t1[1];
        var s = t2[2] - t1[2];
    }

    return normalize_time([h, m, s]);
}

function normalize_time(t) {
    var h = t[0], m = t[1], s = t[2];

    if(s >= 60) {
        s = s - 60;
        m += 1;
    }

    if(m >= 60) {
        m = m - 60;
        h += 1;
    }

    if(s < 0) {
        m = m - 1;
        s = s + 60;
    }
    if(m < 0) {
        h = h - 1;
        m = m + 60;
    }
    return [h, m, s]
}

function make_route_selection(points) {
    var lookups = [];
    var responses = [];
    for(p in points) {
        var point = points[p];
        var cb = $.ajax({
            url: '/nearby_airports.json',
            data: {'type': point[0], 'lng': point[1].longitude, 'lat': point[1].latitude},
        }).success(function(res){
            responses.push(res);
        });
        lookups.push(cb);
    }

    $.when.apply($, lookups).done(function() {
        for(i in responses) {
            var ident, type, n;
            var response = responses[i];
            var old = $("#route_box").val().split('-');

            if(old.length == 1 && !old[0]) {
                old = []
            }
            type = points[i][0];

            if(type == 'land') {
                ident = response[0].ident;
            } else if(type == 'waypoint') {
                // add '@' to the front of waypoint identifiers as per the flightloggin standard.
                ident = '@' + response[0].ident;
            }

            if(old.slice(-1)[0] != ident) {
                // skip this identifier if the last identifier is the same.
                old.push(ident);
            }

            $("#route_box").val(old.join('-'));
        }
    });
}

function send_data() {
    var fields = ['act_inst', 'remarks', 'night_l', 'dual_g', 'fuel_burn', 'dual_r',
              'xc', 'plane', 'sim_inst', 'total', 'day_l', 'pic', 'solo', 'night',
              'app', 'sic', 'person', 'route_string'];
    
    var username = 'chris';
    var d = new Date();
    var date = d.getFullYear() + '-' + d.getMonth() + '-' + d.getDate();
    var data = {'submit': 'Submit New Flight', 'new-date': date};
    for(i in fields) {
        field = fields[i];
        data['new-' + field] = $('input[name=' + field + '], textarea[name=' + field + ']').val();
    }


    $.ajax({
        type: 'post',
        url: '/new_flight-1/' + username,
        data: data,
    });
}

/*
<QueryDict: {
 'new-act_inst': [u''],
 'new-remarks': [u'terds lol'],
 'new-night_l': [u''],
 'new-dual_g': [u'1.3'],
 'new-fuel_burn': [u'2.3 gph'],
 'submit': [u'Submit New Flight'],
 'new-dual_r': [u''],
 'new-xc': [u''],
 'new-plane': [u'100242'],
 'new-sim_inst': [u''],
 'new-ipc': [u'on'],
 'new-total': [u'1.3'],
 'new-day_l': [u'2'], 
 'new-pic': [u''], 
 'new-solo': [u''], 
 'new-night': [u'1.3'], 
 'new-app': [u''],
 'new-sic': [u''], 
 'new-person': [u'woop'], 
 'new-route_string': [u'mer-lga'], 
 'new-date': [u'2012-11-12']}>
*/













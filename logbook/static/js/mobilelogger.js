function get_current_time() {
    // return the current state of the UTC clock, parsed to integers.
    var t = $("#clock").text().split(':');
    return [parseInt(t[0]), parseInt(t[1]), parseInt(t[2])]
}

function get_location(cb) {
    navigator.geolocation.getCurrentPosition(cb);
}

function get_nearest_airports() {
    $.ajax({
        url: '/nearby_airports.json',
        data: {'lng': current_location.longitude, 'lat': current_location.latitude},
        success: function(res) {
            console.log(res);
        }
    });
}

function to_julian(tup) {
    // minutes since midnight, tup = [hour, minutes, seconds]
    return (tup[0] * 60) + tup[1] + (tup[2] / 60);
}

function is_it_day_or_night(mode) {
    var t = get_current_time();
    var night, day;

    if(mode == 'landing') {
        // use civil twilight because thats how the FAA defines night landings
        night = to_julian(ect);
        day = to_julian(mct);
    } else {
        // use sunset and sunrise because thats how the FAA defines night and day hour logging.
        night = to_julian(sunset);
        day = to_julian(sunrise);
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

        if(s >= 60) {
            s = s - 60;
            m += 1
        }

        if(m >= 60) {
            m = m - 60;
            h += 1;
        }
    } else {
        var h = t2[0] - t1[0];
        var m = t2[1] - t1[1];
        var s = t2[2] - t1[2];
    }
    return [h, m, s];
}
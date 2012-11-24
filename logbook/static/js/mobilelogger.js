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
        throw "error";
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
    // t1 = [5, 23, 13] t2 = [6, 50, 2]
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
        // when all location lookups are finished, add them to the page.
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

var data;
function get_data() {
    var fields = ['act_inst', 'remarks', 'night_l', 'dual_g', 'fuel_burn', 'dual_r',
              'xc', 'sim_inst', 'total', 'day_l', 'pic', 'solo', 'night',
              'app', 'sic', 'person', 'route_string'];
    var d = new Date();
    var date = d.getFullYear() + '-' + d.getMonth() + '-' + d.getDate();
    data = {'submit': 'Submit New Flight', 'new-date': date};
    for(i in fields) {
        field = fields[i];
        data['new-' + field] = $('input[name=' + field + ']').val();
    }
    data['new-remarks'] = $('textarea[name=remarks]').val();
    data['new-plane'] = $('#plane').val();
    data['route_points'] = route_points;
    return data;
}

function send_data(data) {
    // send completed flight data to the flight loggin servers
    // `data` is what comes out of the `get_data()` function.
    $.ajax({
        type: 'post',
        url: '/new_flight-1/' + username,
        data: data,
    }).error(function() {
        $('#failed_popup').popup('open');
    }).success(function() {
        reset_app();
    });
}

planes = {};
function get_planes() {
    $.ajax({
        url: '/planes/' + username + '.json',
        type: 'get',
    }).success(function(res) {
        planes = res;
        for(i in res) {
            var plane = res[i];
            var opt = $('<option>');
            opt.attr('value', plane['id']); // the plane_id
            opt.text(plane['tailnumber'] + ' (' + plane['type'] + ')');
            $('select#plane').append(opt);
        }
    });
}

var instrument_current, day_current, night_current;
function set_currency_display(currency) {
    var day = currency['landing'][0] == 'day: CURRENT';
    var night = currency['landing'][1] == 'night: CURRENT';
    var instrument = currency['instrument'] == 'CURRENT';

    if(day) {
        $('#currency_display .day').text('Current');
        $('#currency_display .day').addClass('current').removeClass('not_current');
        day_current = true;
    } else {
        $('#currency_display .day').text('Not Current');
        $('#currency_display .day').addClass('not_current').removeClass('current');
        day_current = false;
    }
    if(night) {
        $('#currency_display .night').text('Current');
        $('#currency_display .night').addClass('current').removeClass('not_current');
        night_current = true
    } else {
        $('#currency_display .night').text('Not Current');
        $('#currency_display .night').addClass('not_current').removeClass('current');
        night_current = false
    }
    if(instrument) {
        $('#currency_display .instrument').text('Current');
        $('#currency_display .instrument').addClass('current').removeClass('not_current');
        instrument_current = true;
    } else {
        $('#currency_display .instrument').text('Not Current');
        $('#currency_display .instrument').addClass('not_current').removeClass('current');
        instrument_current = false;
    }
}

function save_locally(data){
    var old = retrieve_all_saved();
    old.push(data)
    var serialized = JSON.stringify(old);
    localStorage.setItem('flights', serialized);
}

function retrieve_all_saved() {
    var s = localStorage.getItem('flights');
    if(!s) {
        return [];
    }
    return JSON.parse(s);
}

function pop_from_queue() {
    var queued = retrieve_all_saved();
    var ret = queued[0];
    for(i in queued) {

    }
    return ret;
}

function reset_app() {
    console.log('reset');
    $('#person').val('');
    $('.time_container').text('0');
    $('.time_container.dec').text('0.0');

    hood_start = actual_start = start_time = night_start = night_stop = undefined;
    actual_acc = hood_acc = [0, 0, 0];
    route_points = [];

    var fields = ['act_inst', 'remarks', 'night_l', 'dual_g', 'fuel_burn', 'dual_r',
              'xc', 'sim_inst', 'total', 'day_l', 'pic', 'solo', 'night',
              'app', 'sic', 'person', 'route_string'];
    for(i in fields) {
        field = fields[i];
        $('input[name=' + field + ']').val('');
    }

    $('textarea[name=remarks]').val('');
    
    var len = get_queue_count();
    if(len) {
        // there are saved flights in the queue, make the button that submits them.
        var existing_button = $('#submit_queue');
        var text = "Submit " + len + " saved flights";
        if(existing_button.length == 0) {
            var button = $('<a data-theme="b" data-role="button" id="submit_queue">').text(text);
            $('#queue_length').append(button);
            button.button();
        } else {
            // button already exists, update the text.
            existing_button.find(".ui-btn-text").text(text);
        }
    }
}

function get_queue_count() {
    return retrieve_all_saved().length;
}

var pretty;
function pretty_raw_route_points() {
    var out = [];
    var disp, this_accurate, last_accurate;
    for(i in route_points) {
        var rp = route_points[i];
        var lat = rp[1].latitude.toFixed(2);
        var lng = rp[1].longitude.toFixed(2);
        var point = '[' + lat + ',' + lng + ']';
        if(rp[0] == 'land') {
            disp = $('<span>').addClass('land').text(point);
        } else {
            disp = $('<span>').addClass('waypoint').text(point);
        }
        this_accurate = rp[1].latitude.toFixed(4) + rp[1].longitude.toFixed(4);
        if(last_accurate != this_accurate) {
            // skip if the last is the same as this one (using more accurate numbers)
            out.push(disp);
            last_accurate = this_accurate;
        }
    }
    if(out.length == 1) {
        // one duplicate the only element if there is only one element
        // finishing airport is the same as takeoff airport (local flight)
        // log as KMER-KMER
        out[1] = out[0];
    }
    $('#raw_route').append(out);
    $('#raw_route span').after(' '); // add spaces between elements to allow wrapping
}

function calculate_route() {
    get_location(function(res) {
        route_points.push(['land', res.coords]);
        make_route_selection(route_points);
    });
}

function zeroFill(number, width) {
    width -= number.toString().length;
    if (width > 0) {
        return new Array(width + (/\./.test(number) ? 2 : 1)).join('0') + number;
    }
    return number + ""; // always return a string
}

function fill_in_form() {
    // get data from page 1 and 2 and fill it into the page 3 form.
    
    blank = function(val) {
        if(Number(val) == 0) {
            return '';
        } else {
            return val;
        }
    }

    var total = $('#total_time').text();
    var night = blank($('#night_time').text());
    var hood = blank($('#hood_time').text());
    var actual = blank($('#actual_time').text());
    var day_l = blank($('#day_landings').text());
    var night_l = blank($('#night_landings').text());
    var approaches = blank($('#approaches').text());

    $('input[name=total]').val(total);
    $('input[name=night]').val(night);
    $('input[name=act_inst]').val(actual);
    $('input[name=sim_inst]').val(hood);
    $('input[name=app]').val(approaches);
    $('input[name=night_l]').val(night_l);
    $('input[name=day_l]').val(day_l);

    var mode = $('#purpose').val()

    if(mode == 'student') {
        $('input[name=dual_r]').val(total);
    }
    if(mode == 'fo') {
        $('input[name=sic]').val(total);
    }
    if(mode == 'captain') {
        $('input[name=pic]').val(total);
    }
    if(mode == 'instructor') {
        $('input[name=dual_g]').val(total);
        $('input[name=pic]').val(total);
    }
    if(mode == 'solo') {
        $('input[name=solo]').val(total);
        $('input[name=pic]').val(total);
    }
    if(mode == 'training') {
        $('input[name=dual_r]').val(total);
        $('input[name=pic]').val(total);
    }
}
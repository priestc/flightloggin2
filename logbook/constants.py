
# all columns, needs to be in column display order -- ORDER REALLY MATTERS
FIELDS = [
          "date", "plane", "reg", "f_route", "s_route", "r_route",
          "total_s", "total","sim", "pic", "sic", "solo", "dual_r", "dual_g",
          "xc", "act_inst", "sim_inst", "day", "night", "night_l", "day_l",
          "app", "p2p", "multi", "m_pic", "single", "single_pic", "sea",
          "sea_pic", "mes", "mes_pic",
          
          "turbine", "t_pic", "mt", "mt_pic", "complex", "hp", "tail", "jet",
          "jet_pic", "line_dist", "p61_xc", "atp_xc", 'gallons', 'gph', 'mpg',
          "speed",
          
          "max_width", "person", 'instructor', 'student', 'fo', 'captain',
          "remarks",
          ]
          
# all agg-able columns, needs to be in column display order -- ORDER REALLY MATTERS          
ALL_AGG_FIELDS = [      
          "total_s", "total", "sim", "pic", "sic", "solo", "dual_r", "dual_g",
          "xc", "act_inst", "sim_inst", "day", "night", "night_l", "day_l",
          "app", "p2p", "multi", "m_pic", "single", "single_pic", "sea",
          "sea_pic", "mes", "mes_pic",
          "turbine", "t_pic", "mt", "mt_pic", "complex", "hp", "tail", "jet",
          "jet_pic", "line_dist", "p61_xc", "atp_xc", 'gallons'
          ]

## fields that are displayed before the total row starts         
PREFIX_FIELDS = [
          "date", "plane", "reg", "f_route", "s_route", "r_route"
          ]

# db fields that are always just numbers and nothing else
NUMERIC_FIELDS = [
          "pic", "sic", "solo", "dual_r", "dual_g", "xc", "act_inst",
          "sim_inst", "night", "night_l", "day_l",
          ]

# fields included in the backup file
BACKUP_FIELDS = [
          'date', 'reg', 'type', 'route', 'total', 'pic', 'solo', 'sic',
          'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l',
          'day_l', 'sim', 'app_num_only', 'person', 'fuel_burn', 'r_remarks', 
          'flying',
          ]

# fields that have a database column all to themseves
DB_FIELDS = [
          'date', 'plane', 'route','total', 'pic', 'sic', 'solo', 'night',
          'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l','day_l',
          'app', 'person', 'fuel_burn', 'speed', 'gallons', 'gph', 'mpg',
          'remarks'
          ]
          
# for the logbook filter box, all fields that are numerical, but arent based
# on plane category
FILTER_FIELDS = [
          'total', 'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc',
          'act_inst', 'sim_inst', 'night_l','day_l', 'app', 'p2p',
          'line_dist','max_width',
          ]

# fields to be fair game for the line graphing function and the sigs
GRAPH_FIELDS = [
          'total', 'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc',
          'act_inst', 'sim_inst', 'night_l','day_l', 'app','p2p', 'day',
          'multi', 'm_pic', 'sea', 'sea_pic', 'mes', 'mes_pic', 'turbine',
          't_pic', 'mt', 'mt_pic', 'complex', 'hp', 'sim', 'tail', 'jet',
          'jet_pic', 'line_dist', 'gallons'
          ]

# flight fields that get their totals straight from the SUM(x) database command,
# must be in DB_FIELDS. The fields must make sense to sum them together.
AGG_FIELDS = [
          'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc','act_inst',
          'sim_inst', 'night_l','day_l', 'app', 'gallons'
          ]

# fields that do get totals calculated, but require some extra processing
EXTRA_AGG = [
          'total', 'total_s', 'p2p', 'complex', 'hp', 'sim', 'day', 'multi',
          "single", "single_pic", 'm_pic', 'sea', 'sea_pic', 'mes', 'mes_pic',
          'turbine', 't_pic', 'mt', 'mt_pic', 'complex', 'hp', 'sim', 'tail',
          'jet', 'jet_pic', "line_dist", "p61_xc", "atp_xc", 'inst',
          ]

# fields that are optionally turned on and off, used to create the big list
# of checkboxes in the prefs page
OPTION_FIELDS = [
          'plane', 'reg', 'f_route', 's_route', 'r_route', 'total', 'total_s',
          'sim', 'pic', 'sic', 'solo', 'day', 'night', 'dual_r','dual_g', 'xc',
          'act_inst', 'sim_inst', 'night_l','day_l', 'app', 'p2p', 'multi',
          'm_pic', "single", "single_pic", 'sea', 'sea_pic', 'mes', 'mes_pic',
          'tail', 'turbine', 't_pic', 'mt',
          'mt_pic', 'complex', 'hp', "line_dist", "p61_xc",
          'atp_xc', 'max_width','speed',
          'gallons', 'gph', 'mpg',
          'instructor', 'student','fo','captain',
          'person', 'remarks',
          ]
 
FIELD_TITLES = {
    "any": "Any",

    "s_route": "Route (Simple)",
    "f_route": "Route (Fancy)",
    "r_route": "Route (Raw)",
    "route": "Route", #for the backup file (so the header doesn't print '(Raw)'
    "route_string": "Route",
     
    "total_s": "Total (with Sim)",
    "total": "Total",
    
    "date": "Date",
    "r_date": "Date",
    
    "plane": "Plane",
    "reg": "Registration",
    'type': "Type",    # for the backup file

    "pic": "PIC",
    "sic": "SIC",
    "solo": "Solo",
    "day": "Day",
    "night": "Night",
    "dual_r": "Dual Received",
    "dual_g": "Dual Given",
    "xc": "Cross Country",
    "act_inst": "Actual Instrument",
    "sim_inst": "Simulated Instrument",
    "night_l": "Night Landings",
    "day_l": "Day Landings",
    "app": "Approaches",
    "app_num_only": "Approaches",
    
    "p2p": "Point to Point Cross Country",
    "multi": "Multi-Engine",
    "m_pic": "Multi-Engine PIC",
    "sea": "Seaplane",
    "sea_pic": "Seaplane PIC",
    "mes": "Multi-Engine Seaplane",
    "mes_pic": "Multi-Engine Seaplane PIC",
    "turbine": "Turbine",
    "t_pic": "Turbine PIC",
    "mt": "Multi-Engine Turbine",
    "mt_pic": "Multi-Engine Turbine PIC",
    "single": "Single-Engine",
    "single_pic": "Single-Engine PIC",
    "person": "Person",
    "remarks": "Remarks",
    "r_remarks": "Remarks",
    "complex": "Complex",
    "hp": "High Performance",
    "sim": "Sim",
    "jet": "Jet",
    "jet_pic": "Jet PIC",
    "tail": "Tailwheel",
    
    'instructor': "Instructor",
    'fo': "First Officer",
    'captain': "Captain",
    'student': "Student",
    
    "non_flying": "Non-flying",
    "flying": "Flying",
    
    'route__total_line_all': "Route Distance (NM)", ## bargraph
    'max_width': "Max Width",
    'line_dist': "Distance",
    'atp_xc': "ATP Cross Country",
    'p61_xc': "Part 61 Cross Country",
    'speed': 'Speed',
    
    'fuel_burn': "Fuel Burn",
    'gph': "Gallons Per Hour",
    'mpg': "Nautical Miles Per Gallon",
    "gallons": "Gallons Burned",
}

FIELD_ABBV = {
    "s_route": "Route",
    "f_route": "Route",
    "r_route": "Route",
    "route": "Route",
    "route_string": "Route",
    
    "total_s": "Total",
    "total": "Total",

    "date": "Date",
    "r_date": "Date",
    
    "tailnumber": "Plane",
    "type": "Type",
    "plane": "Plane",
    "reg": "Reg.",
    
    "pic": "PIC",
    "sic": "SIC",
    "solo": "Solo",
    "day": "Day",
    "night": "Night",
    "dual_r": "Dual R.",
    "dual_g": "Dual G.",
    "xc": "XC",
    "act_inst": "Actual",
    "sim_inst": "Hood",
    "night_l": "Night L.",
    "day_l": "Day L.",
    "app": "App's",
    "app_num_only": "App.",
    
    "p2p": "P2P",
    "multi": "Multi",
    "m_pic": "Multi PIC",
    "single": "Single",
    "single_pic": "Single PIC",
    "sea": "Sea",
    "sea_pic": "Sea PIC",
    "mes": "ME Sea",
    "mes_pic": "ME Sea PIC",
    "turbine": "Turbine",
    "t_pic": "Turbine PIC",
    "mt": "ME Turbine",
    "mt_pic": "ME Turbine PIC",
    "person": "Person",
    "remarks": "Remarks",
    "r_remarks": "Remarks",
    "complex": "Complex",
    "hp": "HP",
    "sim": "Sim",
    "jet": "Jet",
    "jet_pic": "Jet PIC",
    "tail": "Tail",
    
    'instructor': "Instructor",
    'fo': "First Officer",
    'captain': "Captain",
    'student': "Student",
    
    "non_flying": "Non-flying",
    "flying": "Flying",
    
    'max_width': "Max W. (NM)",
    'line_dist': "Dist (NM)",
    'atp_xc': "ATP XC",
    'p61_xc': "61 XC",
    'speed': "Speed (kts)",
    
    'fuel_burn': "Burn",
    'gph': "gph",
    'mpg': "mpg",
    "gallons": "Gallons",
}

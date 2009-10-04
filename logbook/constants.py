

FIELDS = [               #all columns, needs to be in column display order -- ORDER REALLY MATTERS
          "date", "plane", "reg", "f_route", "s_route", "r_route", "total_s", "total","sim",
          "pic", "sic", "solo", "dual_r", "dual_g", "xc", "act_inst", "sim_inst", "day", "night", "night_l", "day_l", "app",
          "p2p", "multi", "m_pic", "sea", "sea_pic", "mes", "mes_pic", "turbine", "t_pic", "mt", "mt_pic", "complex",
          "hp", "tail", "jet", "jet_pic", "person", 'instructor', 'student','fo','captain', "remarks"
          ]
          
ALL_AGG_FIELDS = [      #all agg-able columns, needs to be in column display order -- ORDER REALLY MATTERS
          "total_s", "total", "sim",
          "pic", "sic", "solo", "dual_r", "dual_g", "xc", "act_inst", "sim_inst", "day", "night", "night_l", "day_l", "app",
          "p2p", "multi", "m_pic", "sea", "sea_pic", "mes", "mes_pic", "turbine", "t_pic", "mt", "mt_pic", "complex",
          "hp", "tail", "jet", "jet_pic",
          ]
          
PREFIX_FIELDS = [
          "date", "plane", "reg", "f_route", "s_route", "r_route"
          ]
          
NUMERIC_FIELDS = [      # fields that are always just numbers and nothing else
          "pic", "sic", "solo", "dual_r", "dual_g", "xc", "act_inst", "sim_inst", "night", "night_l", "day_l",
          ]
          
BACKUP_FIELDS = [       #fields included in the backup file
          'date', 'reg', 'route',
          'total', 'sim', 'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l','day_l', 'app',
          'person', 'r_remarks', 'flying',
          ]
          
DB_FIELDS = [           #fields that have a database column all to themseves
          'date', 'plane', 'route',
          'total', 'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l','day_l', 'app',
          'person', 'remarks'
          ]
          
FILTER_FIELDS = [   # for the logbook filter box, all fields that are numerical, but arent based on plane category
          'total', 'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l','day_l', 'app',
          'p2p',
          ]
          
GRAPH_FIELDS = [        #fields to be fair game for the graphing functions and the sigs
          'total', 'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l','day_l', 'app',
          'p2p', 'day',
          'multi', 'm_pic',
          'sea', 'sea_pic', 'mes', 'mes_pic',
          'turbine', 't_pic', 'mt', 'mt_pic',
          'complex', 'hp', 'sim', 'tail', 'jet', 'jet_pic',
          ]

AGG_FIELDS = [          #fields that get their totals straight from the SUM(x) database command, must be in DB_FIELDS
          'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l','day_l', 'app',
            ]

EXTRA_AGG = [           #fields that do get totals calculated, but require some extra processing
          'total', 'total_s', 'p2p', 'complex', 'hp', 'sim', 'day',
          'multi', 'm_pic',
          'sea', 'sea_pic', 'mes', 'mes_pic',
          'turbine', 't_pic', 'mt', 'mt_pic',
          'complex', 'hp', 'sim', 'tail', 'jet', 'jet_pic',
          ]
          
OPTION_FIELDS = [       #fields that are optionally turned on and off, used to create the bug list of checkboxes in the prefs page
          'plane', 'reg', 'f_route', 's_route', 'r_route', 'total', 'total_s', 'sim',
          'pic', 'sic', 'solo', 'day', 'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l','day_l', 'app',
          'p2p',
          'multi', 'm_pic',
          'sea', 'sea_pic', 'mes', 'mes_pic',
          'turbine', 't_pic', 'mt', 'mt_pic',
          'complex', 'hp',
          'instructor', 'student','fo','captain',
          'person', 'remarks',
          ]
 
FIELD_TITLES = {
    "s_route": "Route (Simple)",
    "f_route": "Route (Fancy)",
    "r_route": "Route (Raw)",
    "route": "Route",            #for the backup file
     
    "total_s": "Total (with Sim)",
    "total": "Total",
    
    "date": "Date",
    "r_date": "Date",
    
    "plane": "Plane",
    "reg": "Registration",

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
}

FIELD_ABBV = {
    "s_route": "Route",
    "f_route": "Route",
    "r_route": "Route",
    "route": "Route",
    
    "total_s": "Total",
    "total": "Total",

    "date": "Date",
    "r_date": "Date",
    
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
    
    "p2p": "P2P",
    "multi": "Multi",
    "m_pic": "Multi PIC",
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
}

#########################################
from django.utils.safestring import mark_safe
from PyHtmlTable import PyHtmlTable

def all_agg_select(prefix=""):
    out = []
    for field in GRAPH_FIELDS:
        out.append("<option name=\"%s%s\">%s</option>" % (prefix, field, FIELD_TITLES[field]))
        
    return mark_safe("<select>" + "".join(out) + "</select>")

def all_agg_checkbox(prefix=""):
    out = []
    for field in GRAPH_FIELDS:
        out.append("<input type=\"checkbox\" id=\"%s\"><label for=\"%s\">%s</label>" % (field, field, FIELD_TITLES[field]))
        
    t = PyHtmlTable(0,5, {"class": "checktable"})
    
    for row in range(0,6):
        for i,item in enumerate(out[(row*5):(row*5)+5]):
            t.setCellcontents(row,i,item)
    
    return mark_safe(t.return_html())

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        

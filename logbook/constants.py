

FIELDS = [               #needs to be in column order
          "date", "plane", "reg", "f_route", "s_route", "r_route", "total_s", "total","sim",
          "pic", "sic", "solo", "dual_r", "dual_g", "xc", "act_inst", "sim_inst", "night", "night_l", "day_l", "app",
          "p2p", "multi", "m_pic", "sea", "sea_pic", "mes", "mes_pic", "turbine", "t_pic", "mt", "mt_pic", "complex",
          "hp", "tail", "jet", "jet_pic", "person", "remarks"
          ]
          
BACKUP_FIELDS = [       #fields included in the backup file
          'date_backup', 'reg', 'r_route',
          'total', 'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l','day_l', 'app',
          'person', 'remarks'
          ]
          
DB_FIELDS = [           #fields that have a database column all to themseves
          'date', 'plane', 'route',
          'total', 'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l','day_l', 'app',
          'person', 'remarks'
          ]

AGG_FIELDS = [          #fields that get their totals straight from the SUM(x) database command, must be in DB_FIELDS
          'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l','day_l', 'app',
            ]

EXTRA_AGG = [           #fields that do get totals calculated, but require some extra processing
          'total', 'total_s', 'p2p', 'complex', 'hp', 'sim',
          'multi', 'm_pic',
          'sea', 'sea_pic', 'mes', 'mes_pic',
          'turbine', 't_pic', 'mt', 'mt_pic',
          'complex', 'hp', 'sim', 'tail', 'jet', 'jet_pic',
          ]
          
OPTION_FIELDS = [       #fields that are optionally turned on and off, used to create the bug list of checkboxes in the prefs page
          'plane', 'reg', 'f_route', 's_route', 'r_route', 'total', 'total_s', 'sim',
          'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l','day_l', 'app',
          'p2p',
          'multi', 'm_pic',
          'sea', 'sea_pic', 'mes', 'mes_pic',
          'turbine', 't_pic', 'mt', 'mt_pic',
          'complex', 'hp',
          'person', 'remarks',
          ]
 
FIELD_TITLES = {
    "s_route": "Route (Simple)",
    "f_route": "Route (Fancy)",
    "r_route": "Route (Raw)",
    
    "total_s": "Total (with Sim)",
    "total": "Total",
    
    "date": "Date",
    "date_backup": "Date",
    "plane": "Plane",
    "reg": "Registration",

    "pic": "PIC",
    "sic": "SIC",
    "solo": "Solo",
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
    "complex": "Complex",
    "hp": "High Performance",
    "sim": "Sim",
    "jet": "Jet",
    "jet_pic": "Jet PIC",
    "tail": "Tailwheel",
}

FIELD_ABBV = {
    "s_route": "Route",
    "f_route": "Route",
    "r_route": "Route",
    
    "total_s": "Total",
    "total": "Total",

    "date": "Date",
    "plane": "Plane",
    "reg": "Reg.",
    
    "pic": "PIC",
    "sic": "SIC",
    "solo": "Solo",
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
    "mes": "Multi Sea",
    "mes_pic": "Multi Sea PIC",
    "turbine": "Turbine",
    "t_pic": "Turbine PIC",
    "mt": "Multi Turbine",
    "mt_pic": "Multi Turbine PIC",
    "person": "Person",
    "remarks": "Remarks",
    "complex": "Complex",
    "hp": "HP",
    "sim": "Sim",
    "jet": "Jet",
    "jet_pic": "Jet PIC",
    "tail": "Tail",
}

NON_FLYING_CHOICES = (
    (1, "1st Class Medical"),
    (2, "2nd Class Medical"),
    (3, "3rd Class Medical"),
    (4, "CFI Refresher"),
    (5, "Student Signoff"),
)

FIELDS = [
          'date', 'plane', 'route',
          'total', 'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l','day_l', 'app',
          'p2p', 
          'multi', 'm_pic',
          'sea', 'sea_pic', 'mes', 'mes_pic',
          'turbine', 't_pic', 'mt', 'mt_pic',
          'complex', 'hp',
          'person', 'remarks',
          ]
BACKUP_FIELDS = ['date_backup', 'plane_backup', 'route_backup',
          'total', 'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l','day_l', 'app',
          'person', 'remarks'
          ]
          
DB_FIELDS = [
          'date', 'plane', 'route',
          'total', 'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l','day_l', 'app',
          'person', 'remarks'
          ]

AGG_FIELDS = [
          'total', 'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l','day_l', 'app',
            ]

EXTRA_AGG = [
          'p2p', 'complex', 'hp',
          'multi', 'm_pic',
          'sea', 'sea_pic', 'mes', 'mes_pic',
          'turbine', 't_pic', 'mt', 'mt_pic',
          'complex', 'hp',
          ]
          
OPTION_FIELDS = [
          'pic', 'sic', 'solo', 'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst', 'night_l','day_l', 'app',
          'p2p',
          'multi', 'm_pic',
          'sea', 'sea_pic', 'mes', 'mes_pic',
          'turbine', 't_pic', 'mt', 'mt_pic',
          'complex', 'hp',
          'person', 'remarks',
          ]
 
FIELD_TITLES = {
    "date": "Date",
    "date_backup": "Date",
    "plane": "Plane",
    "plane_backup": "Plane",
    "route": "Route",
    "route_backup": "Route",
    "total": "Total",
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
}

FIELD_ABBV = {
    "date": "Date",
    "plane": "Plane",
    "route": "Route",
    "total": "Total",
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
}

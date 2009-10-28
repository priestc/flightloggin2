COLUMN_NAMES = {
    "DATE": "date",
    "DATE OF FLIGHT": "date",

    "TIME IN FLIGHT": 'total',
    "TOTAL": 'total',	
    "TOTALTIME": 'total',			
    "DURATION": 'total',
    "DURATION OF FLIGHT": 'total',
    "TOTAL DURATION OF FLIGHT": 'total',
				
    "AIRCRAFT TYPE": 'type',
    "AIRCRAFT MAKE & MODEL": 'type',
    "TYPE": 'type',

    "ROUTE OF FLIGHT": 'route',
    "ROUTE": 'route',
    "FROM": 'from_',
    "TO": 'to',
    "VIA": 'via',
    "STOPS": 'via',
    "ROUTE OF FLIGHT FROM":'from_',
    "ROUTE OF FLIGHT TO": 'to',
    "ROUTE OF FLIGHT VIA": 'via',

    "AIRCRAFT IDENT": 'tailnumber',
    "TAIL NUMBER": 'tailnumber',
    "TAILNUMBER": 'tailnumber',
    "N-NUMBER": 'tailnumber',
    "PLANE": 'tailnumber',
    "REGISTRATION": 'tailnumber',
    "AIRCRAFT REGISTRATION": 'tailnumber',

    "DAY LANDINGS": 'day_l',
    "LANDINGS": 'day_l',
    "LANDINGS DAY": 'day_l',
    "DAY LAND": 'day_l',

    "NIGHT LANDINGS": 'night_l',
    "LANDINGS NIGHT": 'night_l',
    "NIGHT LAND": 'night_l',
    "NIGHT L": 'night_l',

    "SIMULATOR": 'sim',
    "SIM": 'sim',
    "FLIGHT SIMULATOR": 'sim',
    "FLIGHT SIM": 'sim',
    "FTD": 'sim',
    "PCATD": 'sim',

    "APPROACHES": 'app',
    "APPROACHES & TYPE": 'app',
    "INSTAPPR": 'app',

    "PILOT IN COMMAND": 'pic',
    "PIC": 'pic',

    "SECOND IN COMMAND": 'sic',
    "SIC": 'sic',

    "SOLO": 'solo',

    "DUAL": 'dual_r',
    "DUAL RECIEVED": 'dual_r',
    "DUAL RECEIVED": 'dual_r',

    "AS INSTRUCTOR": 'dual_g',
    "AS FLIGHT INSTRUCTOR": 'dual_g',
    "DUAL GIVEN": 'dual_g',
    "CFI": 'dual_g',

    "CROSS COUNTRY": 'xc',
    "XC": 'xc',
    "XCOUNTRY": 'xc',

    "NIGHT": 'night',

    "INSTRUMENT": 'act_inst',
    "ACTUAL INSTRUMENT": 'act_inst',
    "ACTUALINSTR": 'act_inst',
				
    "SIMULATED INSTRUMENT": 'sim_inst',
    'SIMINSTR': 'sim_inst',
				
    "STUDENT": 'student',
    "INSTRUCTOR":'instructor',
    "FIRST OFFICER": 'fo',
    "CAPTAIN": 'captain',
    "FLIGHT NUMBER": 'flight_number',
    "REMARKS": 'remarks',
    
    "HOLDS": 'holding',
    "TRACKING": 'tracking',
				
    "NON-FLYING": 'non_flying',
    "FLYING": 'flying',
}

PLANE_COLUMN_NAMES = {
				
    "TAILNUMBER": 'tailnumber',
    "TAIL NUMBER": 'tailnumber',
				
    "TYPE": 'type',
    "AIRCRAFT TYPE": 'type',
    
    "MODEL": 'model',
    
    "MANUFACTURER": "manufacturer",
    
    "CATEGORY/CLASS": 'cat_class',
    
    "TAGS": 'tags',
    
    "RT": "rt",
    
    "DESCRIPTION": 'description',
    
}

# all fields that the import feature will do anything with
CSV_FIELDS = (
          'date', 'tailnumber', 'type', 'route', 'via', 'from_', 'to',
          'total', 'sim', 'pic', 'solo', 'sic', 'night', 'dual_r','dual_g',
          'xc','act_inst', 'sim_inst', 'night_l','day_l', 'app',
          'person', 'remarks', 'holding', 'tracking', 'instructor', 'student',
          'fo', 'captain', 'flying', 'non_flying','pilot_checkride', 'ipc',
          'cfi_checkride',
          )

# fields that are displayed in the import preview page
PREVIEW_FIELDS = [
        'date', 'tailnumber', 'type', 'route',
        'total', 'sim', 'pic', 'solo', 'sic', 'night', 'dual_r','dual_g',
        'xc','act_inst', 'sim_inst', 'night_l', 'day_l', 'app',
        'person', 'remarks',
        ]

PLANE_HEADERS = (
        'SKIP', 'tailnumber', 'manufacturer', 'model', 'type', 'cat_class',
        'RT', 'tags'
        )
        
PLANE_MAP = {
        'SKIP': 'date', 'tailnumber': 'tailnumber', 'manufacturer': 'type',
        'model': 'route', 'type': 'total', 'cat_class': 'pic',
        'tags': 'sic', 'RT': 'solo',
        }

###### flightlogg.in 1.0 uses these names when it makes backup files ######

NON_FLIGHT_TRANSLATE_NUM = {
        "1": 1,
        "2": 2,
        "3": 3,
        "R": 4,
        "S": 5,
        }
        
NON_FLIGHT_TRANSLATE_TEXT = {
        "1": "1st Class Medical",
        "2": "2nd Class Medical",
        "3": "3rd Class Medical",
        "R": "CFI Refresher",
        "S": "Student Signoff",
        }










    

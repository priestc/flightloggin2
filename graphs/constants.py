BAR_AGG_FIELDS = ('By Person',
                  'By Instructor',
                  'By Captain',
                  'By First Officer',
                  'By Tailnumber',
                  'By Type',
                  'By Manufacturer',
                  'By Model',
                  'By Category/Class',
                  'By Year',
                  'By Month',
                  'By Day of the Week',
                  'By Month/Year',
                 )

from logbook.constants import AGG_FIELDS               
BAR_FIELDS = ['total',
              'route__total_line_all',
              'speed',
              'mpg',
              ] + AGG_FIELDS

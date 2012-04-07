from logbook.constants import AGG_FIELDS               

BAR_AGG_FIELDS = (
    'By Person',
    'By Instructor',
    'By Student',
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

BAR_FIELDS = [
    'total',
    'route__total_line_all',
    'speed',
    'mpg',
    'gph',
] + AGG_FIELDS
              
    
PLOT_COLORS = {
    "total": "black",
    "pic": "red",
    "sic": "purple",
    "dual_r": "blue",
    "dual_g": "orange",
    "act_inst": "green",
    "sim_inst": "lime",
}
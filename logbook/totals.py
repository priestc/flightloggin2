from django.db.models import Sum
from constants import AGG_FIELDS, EXTRA_AGG
from utils import to_minutes

def column_total_by_list(queryset, columns, format='decimal'):
    """takes a list of columns, returns a list of totals for those columns, as
    well as a list of all eligable aggregatable columns"""
    
    ret = []
    agg_columns = []   
    for cn in columns:
       
        total = queryset.agg(cn)
        
        if not total == "??":
            agg_columns.append(cn)
                
            if cn in ['night_l','day_l','app']:
                ret.append(str(total))
            else:
                if format == "decimal":
                    ret.append( "%.1f" % total )
                else:
                    ret.append( to_minutes(total) )
                    
    return (ret, agg_columns)

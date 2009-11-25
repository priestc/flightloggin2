from django.db.models import Sum
from constants import AGG_FIELDS, EXTRA_AGG
from utils import to_minutes

def column_total_by_list(queryset, columns, format='decimal'):
    """takes a list of columns, returns a list of totals for those columns
    """
    
    ret = []
    for cn in columns:
       
        total = queryset.agg(cn)
        
        if not total == "??":  
            if cn in ['night_l','day_l','app']:
                ret.append(str(total))          # write as int
            else:
                if format == "decimal":
                    ret.append( "%.1f" % total )  # write as decimal
                else:
                    ret.append( to_minutes(total) )  # write as HH:MM
                    
    return ret

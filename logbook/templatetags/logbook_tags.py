from django import template
register = template.Library()

from django.utils.dateformat import format as dj_date_format

from logbook.constants import DB_FIELDS, FIELD_TITLES


################################


@register.tag
def make_date_cell(parser, token):
    tag_name, row, profile = token.split_contents()
    return DateCell(row, profile)


class DateCell(template.Node):
    """
    Creates the date column, as well as the Data cells for the popup window
    """
    
    a_title = 'title="Date (click to so see more options)"'
    td_template = '<td title="Date" class="date_col">%s</td>'
    
    def __init__(self, row, profile):
        
        ## get these variables from the template
        self.row_var = template.Variable(row)
        self.profile_var = template.Variable(profile)
        
        
    def render(self, context):
        row = self.row_var.resolve(context)
        profile = self.profile_var.resolve(context)
        formatted_date = dj_date_format(row.date, profile.date_format)
        
        a_date = '<a class="popup_link" href="" id="f%s" %s>%s' %\
                (row.id, self.a_title, formatted_date)
        
        spans = ""
        for data_column in ('date', 'plane', 'route', 'raw_total', 'pic', 'sic',
        'solo', 'night', 'dual_r','dual_g', 'xc','act_inst', 'sim_inst',
        'night_l','day_l', 'app', 'person', 'fuel_burn', 'remarks'):
            data = row.column(data_column, profile.get_num_format())
            
            if data_column == 'plane':
                # special case when plane is retired, we can't show it's
                # tailnumber because there may be another one.
                if row.plane.retired:
                    p = "pk:%s" % row.plane.pk
                else:
                    p = data
                    
                spans += '\n<span class="data_plane">%s</span>' % p
            else:
                # all other data columns
                spans += '\n<span class="data_%s">%s</span>' % (data_column, data)
        
        return self.td_template % (a_date + spans + "</a>")


################################


@register.tag
def make_display_cells(parser, token):
    tag_name, row, columns, profile = token.split_contents()    
    return OtherCells(row, columns, profile)


class OtherCells(template.Node):
    def __init__(self, row, columns, profile):
        
        self.row_var = template.Variable(row)
        self.columns_var = template.Variable(columns)
        self.profile_var = template.Variable(profile)
        
    def render(self, context):
        columns = self.columns_var.resolve(context)
        row = self.row_var.resolve(context)
        profile = self.profile_var.resolve(context)
        
        num_format = profile.get_num_format()
        
        html = ""
        for column in columns.display_list():
            if not column == 'date':
            
                title = FIELD_TITLES[column]
                data = row.column(column, num_format)
                
                html += '<td class="%s_col" title="%s" >%s</td>\n' %\
                            (column, title, data)
            
        return html


################################


@register.tag
def make_overall_agg_cells(parser, token):
    tag_name, row, columns, profile = token.split_contents()    
    return TotalCells(row, columns, profile)


class TotalCells(template.Node):
    def __init__(self, flights, columns, profile):
        
        self.flights_var = template.Variable(flights)
        self.columns_var = template.Variable(columns)
        self.profile_var = template.Variable(profile)
        
    def render(self, context):
        flights = self.flights_var.resolve(context)
        columns = self.columns_var.resolve(context)
        profile = self.profile_var.resolve(context)
        
        num_format = profile.get_num_format()
        
        html = ""
        for column in columns.agg_list():
            if not column == 'date':
                title = FIELD_TITLES[column]
                data = flights.agg(column, num_format)
                html += '<td title="%s" class="%s_agg" >%s</td>\n' %\
                            (title, column, data)
            
        return html



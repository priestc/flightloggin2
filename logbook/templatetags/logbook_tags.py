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
        for data_column in DB_FIELDS:
            data = row.column(data_column)
            spans += '\n<span class="data_%s">%s</span>' % (data_column, data)
        
        return self.td_template % (a_date + spans + "</a>")


################################


@register.tag
def make_display_cells(parser, token):
    tag_name, row, columns = token.split_contents()    
    return OtherCells(row, columns)


class OtherCells(template.Node):
    def __init__(self, row, columns):
        
        self.row_var = template.Variable(row)
        self.columns_var = template.Variable(columns)
        
    def render(self, context):
        columns = self.columns_var.resolve(context)
        row = self.row_var.resolve(context)
        
        html = ""
        for column in columns.display_list():
            if not column == 'date':
                html += '<td title="%s" class="%s_col" >%s</td>\n' %\
                            (FIELD_TITLES[column], column, row.column(column))
            
        return html


################################


@register.tag
def make_overall_agg_cells(parser, token):
    tag_name, row, columns = token.split_contents()    
    return TotalCells(row, columns)


class TotalCells(template.Node):
    def __init__(self, flights, columns):
        
        self.flights_var = template.Variable(flights)
        self.columns_var = template.Variable(columns)
        
    def render(self, context):
        flights = self.flights_var.resolve(context)
        columns = self.columns_var.resolve(context)
        print "fffffffff", flights
        
        html = ""
        for column in columns.agg_list():
            if not column == 'date':
                html += '<td title="%s" class="%s_agg" >%s</td>\n' %\
                            (FIELD_TITLES[column], column, flights.agg(column))
            
        return html



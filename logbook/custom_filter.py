from django.utils.safestring import mark_safe
from django import forms

from constants import GRAPH_FIELDS, FIELD_ABBV
   
def html_table(data, row_length):
    out = '<table id="filter_table">'
    counter = 0
    for element in data:
        if counter % row_length == 0:
            out += '<tr>'
        out += '<td>%s</td>' % element
        counter += 1
        if counter % row_length == 0:
            out += '</tr>'
    if counter % row_length != 0:
        for i in range(0, row_length - counter % row_length):
            out += '<td> </td>'
        out += '</tr>'
    out += '</table>'
    
    return mark_safe(out)
    
def render_table(self):  #will be attached to the class in the function
    out=[]
    for field in GRAPH_FIELDS:
        num_field = str(self[field])
        op = str(self[field + "_op"])
        title = getattr(self, 'fields')[field].label
        out.append( title + op + num_field )

    return html_table(out, 4)

def make_filter_kwargs(self):
    """all field ops will be in the form "pic_op"
    """
    
    kwargs = {}
    for field,val in self.cleaned_data.iteritems():

        if not field.endswith("_op") and val:
            filter_ = val
            op = self.cleaned_data.get(field + "_op", "")
            
            if op == "0":
                op = ""
                
            elif op == "1":
                op= "__gt"
                
            elif op == "2":
                op = "__lt"
                
            kwargs.update({field + op: val})
        
    
    print kwargs
    #kwargs = {"pic__gt": 2}
    
    return kwargs
    
    
    
    
    
    
    
    
def make_filter_form(user):
    from plane.models import Plane
    
    types = Plane.objects.filter(user=user).values_list('type', flat=True).distinct()
    tt = [(t,t) for i,t in enumerate(types)]
    tt.insert(0, ("", "-------"))
    
    cat_classes = Plane.objects.filter(user=user).values_list('cat_class', flat=True).order_by().distinct()
    cc = [(t,t) for i,t in enumerate(cat_classes)]
    cc.insert(0, ("", "-------"))
    
    operators = ( (0, "="), (1, ">"), (2, "<") )
    fields = {'plane__tags': forms.CharField(required=False),
              'plane__tailnumber': forms.CharField(required=False),
              'plane__type': forms.ChoiceField(choices=tt, required=False),
              'plane__cat_class': forms.ChoiceField(choices=cc, required=False),
              'start_date': forms.DateField(label="Start", required=False, widget=forms.TextInput(attrs={"class": "date_picker"})),
              'end_date': forms.DateField(label="End", required=False, widget=forms.TextInput(attrs={"class": "date_picker"})),
             }
             
    for field in GRAPH_FIELDS:
        d = {field: forms.FloatField(label=FIELD_ABBV[field], required=False, widget=forms.TextInput(attrs={"class": "small_picker"})), 
             field + "_op": forms.ChoiceField(choices=operators, required=False, widget=forms.Select(attrs={"class": "op_select"})),
             }
        fields.update(d)
        
    FilterForm = type('FilterForm', (forms.BaseForm,), { 'base_fields': fields })
    FilterForm.render_table = render_table
    FilterForm.make_filter_kwargs = make_filter_kwargs
    
    return FilterForm












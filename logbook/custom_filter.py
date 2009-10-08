from django.utils.safestring import mark_safe
from django import forms

from constants import FILTER_FIELDS, FIELD_ABBV
   
def html_table(data, row_length):
    out = '<table id="center_filter_table">'
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
    for field in FILTER_FIELDS:
        num_field = str(self[field])
        op = str(self[field + "_op"])
        title = getattr(self, 'fields')[field].label
        out.append( title + op + num_field )

    return html_table(out, 3)

def make_filter_kwargs(self, qs):
    """filter the queryset based on the form values, the name of this function
       should be renamed
    """
    
    # all filter fields not ending with "_op"
    fields = filter(lambda x: not x[0].endswith("_op"),
                    self.cleaned_data.iteritems())
    
    for field,val in fields:
        
        if val:
            if field == "start_date":        # date filters
                kwargs = {"date__gte": val}
                qs = qs.filter(**kwargs)
            
            elif field == "end_date":
                kwargs = {"date__lte": val}
                qs = qs.filter(**kwargs)
                
            elif field == 'person':
                kwargs = {"person__icontains": val}
                qs = qs.filter(**kwargs)
                
            elif field == 'remarks':
                kwargs = {"remarks__icontains": val}
                qs = qs.filter(**kwargs)
            
            elif "__" in field:       # all "__" filters
                kwargs = {"%s__icontains" % field: val}
                qs = qs.filter(**kwargs)
            
            elif val>=0:                     # all time filters
                filter_ = val
                print field,val
                op = self.cleaned_data.get(field + "_op", "")
                
                if op == "0":
                    qs = qs.filter_by_column(field, eq=val)
                    
                elif op == "1":
                    qs = qs.filter_by_column(field, gt=val)
                    
                elif op == "2":
                    qs = qs.filter_by_column(field, lt=val)

    return qs
    
    
def make_filter_form(user):
    from plane.models import Plane
    
    types = Plane.objects.filter(user=user).values_list('type',
                                            flat=True).distinct()
                                            
    tt = [(t,t) for i,t in enumerate(types)]
    tt.insert(0, ("", "-------"))
    
    from plane.constants import CATEGORY_CLASSES
    CATEGORY_CLASSES = dict(CATEGORY_CLASSES)
    
    cat_classes = Plane.objects.filter(user=user).values_list('cat_class',
                                            flat=True).order_by().distinct()
                                            
    cc = [(t,CATEGORY_CLASSES[t]) for i,t in enumerate(cat_classes)]
    cc.insert(0, ("", "-------"))
    
    operators = ( (0, "="), (1, ">"), (2, "<") )
    fields = {'plane__tags': forms.CharField(required=False),
              'plane__tailnumber': forms.CharField(required=False),
              'plane__type': forms.ChoiceField(choices=tt, required=False),
              'plane__cat_class': forms.ChoiceField(choices=cc, required=False),
              'start_date': forms.DateField(label="Start", required=False,
                    widget=forms.TextInput(attrs={"class": "date_picker"})),
              'end_date': forms.DateField(label="End", required=False,
                    widget=forms.TextInput(attrs={"class": "date_picker"})),
              'last_flights': forms.IntegerField(required=False,
                    widget=forms.TextInput(attrs={"class": "small_picker"})),
              'person': forms.CharField(required=False),
              'remarks': forms.CharField(required=False),
              'route__fancy_rendered': forms.CharField(required=False,
                    label="Route"),
             }
             
    for field in FILTER_FIELDS:
        d = {field: forms.FloatField(label=FIELD_ABBV[field], required=False,
                widget=forms.TextInput(attrs={"class": "small_picker"})), 
             "%s_op" % field: forms.ChoiceField(choices=operators, required=False,
                widget=forms.Select(attrs={"class": "op_select"})),
             }
        fields.update(d)
        
    FilterForm = type('FilterForm', (forms.BaseForm,), { 'base_fields': fields })
    FilterForm.render_table = render_table
    FilterForm.make_filter_kwargs = make_filter_kwargs
    
    return FilterForm












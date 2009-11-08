def html_table(data, row_length, html_id='center_filter_table'):
    from django.utils.safestring import mark_safe
    out = '<table id="%s">\n' % html_id
    counter = 0
    for element in data:
        if counter % row_length == 0:
            out += '  <tr>\n'
        out += '    <td>%s</td>\n' % element
        counter += 1
        if counter % row_length == 0:
            out += '  </tr>\n\n'
    if counter % row_length != 0:
        for i in range(0, row_length - counter % row_length):
            out += '    <td> </td>\n'
        out += '  </tr>\n'
    out += '</table>\n'
    
    return mark_safe(out)

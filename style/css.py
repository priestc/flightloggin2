#!/usr/bin/env python

styles = {

"style-2": {"page_bg":          "#CCE4EB",
           "navbar_bg":         "#665B1E",
           "link_color":        "#001147",
           "h1_color":          "#0000FF",
           "h2_color":          "#00FF00",
           
           "navbar_border":     "0px solid #001147",
           "navbar_text":       "white",
           "navbar_hover":      "text-decoration: underline",
           "navbar_sel":        "background: #5DC7E9; font-weight: bold",
           "canvas_color":      "white",
           "canvas_border":     "0px solid black",
           
           "widget_border":     "1px solid black",
           
           "mt_header_color":   "#C1E8E8",
           "mt_border":         "1px solid #C3C3C3",
           
           "mt_strip1":         "#E2EEEE",
           "mt_strip2":         "#DFDFDF",
           
           "current":           "#5DC7E9",
           "expired":           "gray",
           "alert":             "#AE345E",
           
           "popup_title_bg":    "#CCE4EB",
           
           "news_bg":           "#CCE4EB",
           
           "sig_bg":            "pink",
           
           "ss_strip1":         "white",
           "ss_strip2":         "#EEEEEE",
           },
           
"style-3": {"page_bg":          "white",
           "navbar_bg":         "red",
           "link_color":        "red",
           "h1_color":          "red",
           "h2_color":          "red",
           
           "navbar_border":     "1px solid purple",
           "navbar_text":       "red",
           "navbar_hover":      "text-decoration: underline",
           "navbar_sel":        "background: red; font-weight: bold",
           "canvas_color":      "white",
           "canvas_border":     "1px solid purple",
           
           "widget_border":     "1px solid black",
           
           "mt_header_color":   "#C1E8E8",
           "mt_border":         "1px solid #C3C3C3",
           
           "mt_strip1":         "#E2EEEE",
           "mt_strip2":         "#DFDFDF",
           
           "current":           "#5DC7E9",
           "expired":           "gray",
           "alert":             "#AE345E",
           
           "popup_title_bg":    "#CCE4EB",
           
           "news_bg":           "red",
           
           "sig_bg":            "red",
           
           "ss_strip1":         "white",
           "ss_strip2":         "red",
           }

}

test = """

body                    {background: %(page_bg)s;
                         margin: 15px;}


{df: %(page_bg)s; %(page_bg)s: dfdfd
dsfdsfsdf}

"""

###############################################################################
###############################################################################
###############################################################################
###############################################################################

base = """
body                    {background: %(page_bg)s;
                         margin: 15px;
                         margin-top: 0px;
                         padding: 0px;
                         font-size: small; 
                         font-family: "Bitstream Vera Sans", sans-serif;
                         min-height: 100%%;
                         height: 100%%;}
                         
#header                 {margin:5px; overflow: hidden; border: 0px solid black}
#main_content           {margin:5px; overflow: hidden; border: 0px solid black}

#logo                   {height: 44px;
                         margin-top: 11px;
                         border: 0px solid black;}

#logo_box               {float: left}

#advert_box             {float: right; height:60px}

#logged_in_as           {float: right;
                         text-align: right;
                         font-weight: normal;
                         color: #001147;
                         width: 100%%;
                         border: 0}
                         
span.logged_user,
span.display_user       {font-weight: bold}
                         
#demo                   {font-weight: bold;
                         color: #AA3333}


#nav_bar                {background: %(navbar_bg)s;
                         border: 0px;
                         width: 100%%;
                         float: left;
                         color: %(navbar_text)s;
                         padding: 0;
                         padding-top: 3px;
                         padding-bottom: 3px;
                         border: %(navbar_border)s}
                         
                         
/* navbar for users who are not logged in */

#nav_bar a              {color: white;
                         margin-left: 3px;
                         margin-right: 3px;
                         text-decoration: none}
                         
#nav_bar a:hover        {%(navbar_hover)s}

#nav_bar .big           {font-size: large}

#nav_bar .nav_selected a {%(navbar_sel)s}

.display_user           {color: black}
.logged_user            {color: black}

/* the white background beneath (almost) all pages*/
#canvas                 {%(canvas_color)s;
                         padding: 1em;
                         overflow:hidden;
                         max-width: 73em;
                         margin: 0 auto 0 auto;
                         text-align: center;
                         border: 0px solid black}

/* the little calendar icon for the date picker*/                       
.embed + img            {position: relative;
                         left: -19px;
                         top: 3px;
                         cursor: pointer;}
	 
a                       {color: %(link_color)s}

h1                      {text-align: center;
                         font-weight: bold;
                         color: %(h1_color)s;
                         font-size: x-large;}
                         
h2                      {font-weight: bold;
                         color: %(h2_color)s;
                         font-size: large}

textarea                {border: %(widget_border)s;
                         font-family: inherit;
                         font-size: inherit;
                         background: white}
                         
select                  {border: %(widget_border)s;
                         background: #EEEEEE;
                         font-size: smaller;
                         font-family: inherit}

/* instructions boxes in a few of the pages */
.instructions           {background: #DDDDDD; padding: 20px}

input[type="button"]:hover,
input[type="submit"]:hover,
button:hover            {cursor: pointer}

input[type="submit"],
input[type="button"],
button                  {border: %(widget_border)s}

input[type="password"],
input[type="text"]      {border: %(widget_border)s; background: white}

input[type=text]:disabled {background-color: #DDDDDD;
                           color: #777777;
                           border: 1px dotted #EEEEEE}

#footer                 {text-align:center;
                         font-size: x-small;
                         color: gray;
                         width: 100%%;}
                         
/***** table for events, planes, and places *********/

table.minor_table                     {width:       100%%;
                                       border-collapse: collapse}

/* the header row */
table.minor_table thead td            {border:      1px solid #C3C3C3;
                                       background:  %(mt_header_color)s;
                                       font-weight: normal;
                                       padding:     2px}

/* the footer row */
table.minor_table tfoot td            {border:      %(mt_border)s;
                                       background:  %(mt_header_color)s;
                                       font-weight: normal;
                                       padding:     2px}

/* every other cell */
table.minor_table td                  {border:      %(mt_border)s;
                                       padding:     2px}

/* striping */
table.minor_table tr:nth-child(odd)   {background:  %(mt_strip1)s}
table.minor_table tr:nth-child(even)  {background:  %(mt_strip2)s}

/* the empty message */
table.minor_table td[colspan]         {font-size:   x-large;
                                       padding:     10px}
"""

###############################################################################

currency = """
#canvas             {text-align: left}
div.currbox         {width: 100%%; overflow: hidden; margin-bottom: 10px; text-align: center}
div.currbox p       {margin-top: 3px}
h2                  {margin-left: auto; margin-right: auto}                  
h3                  {font-size: large; color: black; margin: 11px 0 5px 0}

div.inner_currbox   {border: 1px solid black; width: 49%%; height: 100px}
div.medical_third   {border: 1px solid black; width: 32%%; height: 100px; float: left; margin: 5px}
div.inst_four       {border: 1px solid black; width: 23.5%%; height: 50px;
                     float: left; margin: 5px; font-size: xx-small;
                     padding-top: 3px}
                     
.inst_bar            {width: 99%% !important; height: 30px !important}

div.day             {float: left}
div.night           {float: right}

div.bfr             {float: left}
div.cfi             {float: right}

.expired            {background-color: {expired}}
.current            {background-color: {current}}
.alert              {background-color: {alert}}

.nothing            {font-size: large; margin: 10px; text-align: center}



table.currbox                 {width: 100%%; border: 1px solid black;
                               text-align: center; font-size: xx-small;
                               height: 100px; border-collapse: collapse;}
                               
table.currbox strong          {font-size: small}
table.currbox td              {border: 1px solid black; padding: 0px}
table.currbox td h3           {margin-top: 0px}
tr.full_bar td                {text-align: center}

table.instrument td           {width: 25%%}
table.medical td              {width: 33%%}
"""

###############################################################################

events = """
/* the date field is a little longer than normal because its one column */
td.date input                         {width: 100px}

/* the text box for comments in the popup */ 
textarea                              {width: 250px; height: 100px}

/* since theres only one column, make sure it's left aligned */
#popup td:nth-child(2)                {text-align: left}

/* hidden date for the popup */
.unformatted_date                     {display: none}
"""

###############################################################################

popup = """
/* the "new" button at the top */
input[type="button"]        {margin: 10px}

#popup                      {position: absolute;
                             top: 50px;
                             left: 50px;
                             display: none;
                             width: 380px;
                             background: white;
                             font-size: small !important;
                             text-align:center;
                             overflow: hidden;
                             border: 2px solid black}
                             
#popup table                {margin-left: auto; margin-right: auto}

#dragbar                    {background: {popup_title_bg};
                             width: 100%%;
                             text-align: right;
                             margin-bottom: .5em;
                             border-bottom: 1px solid black}
                             
#dragbar td:first-child     {width:100%%; text-align:center; font-weight: bold; font-size: larger}
#dragbar td:last-child      {text-align:right}

#close_x                    {cursor: pointer; font-weight: bold}

#edit_buttons,
#new_buttons                {padding: 10px}
"""

###############################################################################

flight_popup = """
#popup                                      {width: 480px}
				 
#new_entry_popup td                         {padding: 0}

#flying_div                                 {padding: 5px}
#table_holder                               {overflow: hidden; width:100%%; border: 0px solid green}

#flight_left_table                          {width: 53\%%; border: 0px solid black; float: left; margin-right: -10px}

#flight_left_table input[type=text],
textarea, select                            {width: 145px}

#flight_left_table textarea                 {height: 5.5em}
#flight_left_table tr td:first-child        {text-align: right; padding-right: 5px}
#flight_left_table tr td:last-child	        {text-align: left}

#flight_right_table                         {width: 47%%; border: 0px solid black; float: right}
#flight_right_table input[type=text]		{width: 2.9em}
#flight_right_table input[type=button]		{margin-left: 5px}
#flight_right_table tr td:last-child		{text-align: left; padding-left: 5px}
#flight_right_table tr td:first-child		{text-align: right}

#landings_table                             {width: 100%%; margin-top: 5px; margin-bottom: 5px}
#landings_table input[type=text]            {width: 2em}

#flight_events_table                        {width: 99%%;
                                             border:1px solid black;
                                             margin-left: auto;
                                             margin-right: auto;
                                             margin-bottom: 5px;
                                             background: lightblue}

#flight_events_table td                     {text-align: left;}

ul.errorlist                                {color: red; margin: 0px; margin-right: 5px; padding: 0px; 
                                             width: 145px; list-style-type: none; text-align: center; border: 1px solid red}

#non_events_table                           {width: 100%%; border:0px solid black; margin: 0em; background: lightblue}
#non_events_table td                        {text-align: left; width: 33%%;}

#non_flying_div                             {text-align: center}
#non_flying_div table:first-child, 
#non_flying_div textarea                    {width: 85%%; height: 5.5em;}
#non_flying_div table:first-child td:first-child  {width: 30%%; text-align: right; padding-right: 5px}
#non_flying_div table:first-child td:last-child   {text-align: left}
#non_flying_div input[type=text]            {width: 120px}


#flight_buttons, #non_buttons               {width:100%%; float: left; margin-bottom: 10px}


#flight_left_table tr:first-child           {display:none}
"""

###############################################################################

help = """
#canvas     {text-align: left}
"""

###############################################################################

locations = """
input[type="submit"],
input[type="button"]                {margin-bottom: 10px}

input[type=text],
select, textarea	                {width: 200px;
                                     font-size: small !important}

input[type="button"]                {margin: 10px}

td.remarks textarea                 {height: 50px}
td.date input                       {width: 100px}

textarea                            {width: 250px; height: 100px}
#popup td:nth-child(2)              {text-align: left}

/* for the instructions for the coordinates on the popup */
.help_text                          {color: gray;
                                     font-style: italic;
                                     font-size: x-small}
"""
###############################################################################

import__ = """
.flying_event                   {color: darkred; font-weight: bold}
#canvas                         {max-width: 100%% !important}

.preview                        {border-collapse: collapse; border: 1px solid gray; margin: 10px auto auto auto}
.preview td                     {font-size: x-small; border: 1px solid gray}

tr.bad td                       {background: pink}
tr.good td                      {background: #A2E4A7}
tr.header td                    {background: #C7A16E}

div#progress                    {font-size: large; margin: 10px;
                                 background: #EEEEEE;
                                 border: 1px solid gray}
                                 
table#import_form               {margin: 10px auto 10px auto; background: #EDEDED;
                                 border: 1px solid black}
                                 
table#import_form td            {padding: 10px; border: 1px ridge gray}

table#import_form input         {border: default; background: default}
"""

###############################################################################

logbook = """
#canvas                                      {width: 98%%; max-width: none}

/* the [Pilot Checkride] tag in the remarks section*/
.flying_event                                {color: darkred; font-weight: bold}

/* hidden data for the popup window */
.date_col span                               {display: none}


#logbook_table                               {width:100%%;
                                              border: 0px solid #C3C3C3;
                                              background: white;
                                              font-size: x-small;
                                              border-collapse: collapse}

/* odd rows */
#logbook_table tbody tr:nth-child(even) td   {background: #E2EEEE}

/* even rows */
#logbook_table tbody tr:nth-child(odd) td    {background: #FFFFFF}

/* all table cells */
#logbook_table td                            {border: 1px solid #C3C3C3; padding: 1px}

/* the remarks column */
#logbook_table td:last-child:not([colspan])  {white-space: normal; text-align: left}

/* both header rows at the top and bottom */
#logbook_table tr.header td                  {background: #E0FFFF !important}

/* mass edit link */
#logbook_table tfoot td[colspan]             {border: none; text-align:right}

td.empty_logbook                             {font-size: x-large; padding: 10px !important}
"""

###############################################################################

route = """
span.land                                    {text-decoration: underline}
span.noland                                  {text-decoration: none}

span.found_airport                           {color: MediumSlateBlue}
span.found_navaid                            {color: SeaGreen}
span.found_custom                            {color: Navy}                                             
span.not_found                               {color: gray}
span.local                                   {color: gray}
"""

###############################################################################

custom_view = """
#filter_box                             {width: 100%%; background: white; border: 0px solid black; margin-top: 10px}
#filter_box select[class*='__'],
#filter_box input[class*='__']          {width: 100px}
#filter_box td                          {width: 20%%; text-align: center; border: 0px solid black; padding: 3px}
#center_filter_table                    {margin: 0 auto 0 auto}
#center_filter_table td                 {width: 33%% !important; text-align: right}

/* middle pane is a little bit wider */
#filter_box td:nth-child(2)             {width: 60%%}

/* the little boxes and dropdowns in the middle pane*/
.small_picker                           {width: 3em}
.op_select                              {width: 4em; margin: 3px}

/**/
table#text_filters                      {margin: 0 auto 0 auto}
table#text_filters td                   {text-align: right !important}
table#text_filters td:last-child        {text-align: left !important}

/* the start/end date box */
td#date_filter_pane table               {margin: 0 auto 0 auto}
td#date_filter_pane table td            {text-align: right !important}
td#date_filter_pane table td:last-child {text-align: left !important}
.date_align                             {width: 4em; border: 1px solid red; float: left}
.date_picker                            {width: 8em; margin-top: 2px}

/* the last panel (plane filters) */
td#plane_filter_pane input,
td#plane_filter_pane select                {width: 150px}
"""

###############################################################################

maps = """
h3                              {margin-bottom: 2px}

.green                          {color:#00F014}
.red                            {color:#D20014}
.blue                           {color:#0078FF}
.purple                         {color:#780078}
.orange                         {color:#FFB114}

#images_table                   {width: 100%%;
                                 margin-left: auto;
                                 margin-right: auto}
                                 
.maps_table                     {text-align: center;
                                 margin-bottom: 20px;
                                 margin-right: auto;
                                 margin-left: auto;
                                 width: 50%%}
                                 
.maps_table td                  {width: 50%%; background: lightgray}
"""

###############################################################################

mass_entry = """
#canvas                                   {max-width: 100%%}

table.mass_table                          {width: 100%%; border-collapse: collapse}
table.mass_table input                    {font-size: small}

tr.header_row td                          {font-size: x-small; background: white; padding: 0}
table.mass_table tr:nth-child(even)       {background: #DDDDDD}

input.route_line                          {width: 8em}
input.person_line                         {width: 8em}
input.vDateField                          {width: 8em;}
input.float_line                          {width: 2.4em; margin: 1px}
"""

###############################################################################

mass_planes = """
table input,
table select                  {width: 100%%}

table.mass_table              {border-collapse: collapse;
                               margin: 0 auto 10px auto}
"""

###############################################################################

milestones = """
table.milestone_table        {margin: 0 auto 0 auto; border: 2px solid gray}
table.milestone_table td     {text-align: left; padding-left: 10px}

/* not yet met */
.x                           {color: red}

/* already met */
.v                           {color: green}
"""

###############################################################################

news = """
#canvas             {text-align: left}

.news_box			{border: 1px solid black;
	                 width: 50em;
	                 margin-right: auto;
	                 margin-left: auto;
	                 margin-bottom: 15px;
	                 padding: 5px;
	                 background: {news_bg}}

.news_box p			{font-size: medium}

.news_box big       {font-size: x-large;
	                 font-weight: bold}
	     
.news_box small     {font-size: small}

#demo_link          {background: #DDDDDD;
                     width: 100%%;
                     padding: 10px 0 10px 0;
                     text-align: center;
                     margin-bottom: 20px;
                     font-size: medium}
"""

###############################################################################

planes = """
input[type="submit"],
input[type="button"]        {margin-bottom: 10px}

input[type=text],
select, textarea	        {width: 200px; font-size: small !important}

#tags_window                {background: white;
                             font-size: x-small;
                             border: 0px solid blue;
                             padding: 5px;}
                             
#tags_window a:hover        {color: lightgreen}

textarea                    {height: 50px}

/* instructions for each field on the popup*/
span.help_text              {color: gray;
                             font-size: x-small;
                             font-style: italic}

/* message for when there are no planes to diaplay*/
td.empty_row                {font-weight: bold;
                             font-size: large;
                             padding: 10px}

/* the tag cloud in the popup window */
.tag1                       {font-size: xx-small}
.tag2                       {font-size: xx-small}
.tag3                       {font-size: x-small}
.tag4                       {font-size: small}
.tag5                       {font-size: medium}

#mass_edit_link             {width: 100%%;
                             text-align: right;
                             font-size: x-small}
"""

###############################################################################

preferences = """
fieldset                              {text-align: right}
legend                                {font-size: large; font-weight: bold;
                                        color: #11566d}
input, select                         {width: 80%%}
input[type="checkbox"]                {width: auto}
input[type='submit']                  {width: auto; margin-top: 15px}

ul                                    {font-sze: inherit; margin: 0; color: red;
                                        font-weight: bold}

.prefs_table                          {width:100%%; border: 0px solid black;
                                        font-size: medium; margin-right: auto;
                                        margin-left: auto}

.prefs_table td:first-child           {border: 0px solid green; width: 50%%;
                                        text-align: right; padding-right: 10px}
.prefs_table td                       {border: 0px solid blue; text-align: left;
                                       width: 10%%}

/* The help text column */
.prefs_table td:last-child            {font-size: small; color:gray; width: 30%%}

td[colspan='4']                       {padding-bottom: 10px; text-align: center}

#columns_table                        {color: black; border: 1px solid gray;
                                        margin-right: auto; margin-left: auto}

/* the titles column */
#columns_table td                     {font-size: small; text-align: left;
                                        padding: 0 3px 0 3px !important;
                                        width: 20em}

/* the first two columns where the checkboxes are */
#columns_table td:nth-child(2),
#columns_table td:first-child         {text-align: center; width: 2em}

/* header row */
#columns_table tr:first-child > td    {width: 2em !important;
                                        background: white !important}

/* striping */
#columns_table tr:nth-child(even) td  {background: #EDEDED}
#columns_table tr:nth-child(odd) td   {background: #E0FFFF}

/* help text row */
#columns_table td:last-child          {width: 40em; font-size: xx-small;
                                        font-style: italics; color: black}

.delete_box                           {text-align: center}

#instructions                         {text-align: center; color: gray}
"""

###############################################################################

realtime = """
/* the countdown timer*/
.epiclock                       {font-size: large; color: green}
"""

###############################################################################

records = """
textarea                        {width: 800px; height: 400px}
"""

###############################################################################

sigs = """
#checktable                     {margin-left: auto; margin-right: auto}
#checktable td                  {text-align: left}

#sig_url                        {width: 50%%;
                                 padding: 20px;
                                 font-size: large;
                                 background: {sig_bg};
                                 text-align: center;
                                 margin: 0 auto 0 auto}
                             
#image_div                      {padding: 20px;
                                 background: clear;
                                 min-width: 10%%}
"""

###############################################################################

site_stats = """
#site_stats                     {font-size: large;
                                 margin: 0 auto 0 auto;
                                 text-align: right;
                                 border-collapse: collapse;
                                 width: 100%%}

#site_stats td                  {border: 1px dotted gray;
                                 padding-right: 10px;
                                 background: {ss_strip1}}
                                  
#site_stats td:last-child       {text-align: left;
                                 font-weight: bold;
                                 padding-left: 10px}

/* striping */                              
#site_stats tr:nth-child(odd)   {background: {ss_strip2}}
                                 
#openid td, #openid th          {border: 1px dotted gray; text-align: center}
#openid                         {margin: 0 auto 0 auto;}
#openid td                      {text-align: left; padding: 0 10px 0 10px}
#openid td:first-child          {text-align: right}
"""


if __name__ == "__main__":
    
    # a dict containing all css strings undexed by filename
    css = locals()
    
    import sys
    import os  
    directory = "style-%s" % sys.argv[1]
    source = styles[directory]
    
    names = ('base', 'currency', 'events', 'flight_popup', 'help',
             'import__', 'locations', 'logbook', 'maps', 'mass_entry',
             'mass_planes', 'milestones', 'news', 'planes', 'popup',
             'preferences', 'realtime', 'records', 'sigs', 'site_stats',
             'custom_view', 'route')
    
    print directory
    
    if not os.path.isdir(directory):
        os.makedirs(directory)
    else:
        pass #assert False, "You must move/delete the old folder first"
                 
    for name in names:
        f = open("%s/%s.css" % (directory, name.replace("__",'')), 'w')
        rendered = css[name] % source
        f.writelines(rendered)
















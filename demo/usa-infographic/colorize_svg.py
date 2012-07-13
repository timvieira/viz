import csv
from BeautifulSoup import BeautifulSoup
 
# Read in unemployment rates
unemployment = {}
reader = csv.reader(open('unemployment09.csv'), delimiter=",")
for row in reader:
    full_fips = row[1] + row[2]
    rate = float(row[8].strip())
    unemployment[full_fips] = rate
 
    if 'Broward' in row[3]:
        print row


# countyincome07.csv
#"State_Code","County_Code","State_Abbrv","County_Name","Return_Num","Exmpt_Num","AGI","Wages_Salaries","Dividends","Interest"


# ['PS120050', '12', '011', 'Broward County, FL', '2009', '1,007,323  ', '908,754  ', '98,569  ', '9.8   ']


# Load the SVG map
svg = open('counties.svg', 'r').read()
 
# Load into Beautiful Soup
soup = BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'])
 
# Find counties
paths = soup.findAll('path')
 
# Map colors
colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]
 
# County style
path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;\
stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;\
marker-start:none;stroke-linejoin:bevel;fill:'

missed = 0
success = 0

# Color the counties based on unemployment rate
for p in paths:

    if p['id'] not in ["State_Lines", "separator"]:

        if p['id'] not in unemployment:
            missed += 1
            continue
        success += 1

        rate = unemployment[p['id']]
        
        if rate > 10:
            color_class = 5
        elif rate > 8:
            color_class = 4
        elif rate > 6:
            color_class = 3
        elif rate > 4:
            color_class = 2
        elif rate > 2:
            color_class = 1
        else:
            color_class = 0
 
        color = colors[color_class]
        p['style'] = path_style + color
 

print 'missed', missed, 'county out of', missed + success

with file('unemployment09.svg','wb') as f:
    f.write(soup.prettify())


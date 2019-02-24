import mistune
from dateutil import parser,rrule 
import calendarClass

# Read and parse the markdown file
# ---------------------------------
f_md = open('calendar.md','r')

isPreface = True
preface = ""

calDtList = []
calDict = {}
calKey = None

##rrDict ={}
##rrKey = None

for line in f_md:
    line = line.strip()

    if line[0:4]=="### ":
        # Regular Events
        isPreface = False
        thisDt = parser.parse(line[4:])
        calKey = thisDt.strftime('%Y-%m-%d')
        if calKey not in calDict:
            calDtList.append(thisDt)
            calDict[calKey] = ''

    elif line[0:5]=="#### ":
        # Recurring Events
        isPreface = False

    else:
        if not isPreface and not (line[0:3]=="---"):
            calDict[calKey] += line + '\n'

    if isPreface and not (line[0:3]=="---"):
        preface += line + '\n'
        
f_md.close()

prefaceHtml = mistune.markdown(preface)
calDictHtml = {}
for key in calDict:
    calDictHtml[key] = mistune.markdown(calDict[key])

# Open the HTML file and write to it 
# ---------------------------------
c = calendarClass.mdCalendar()
f = open('calendarTest.html','w')
f.write('<html>\n<head>\n'
        '<link rel="stylesheet" type="text/css" href="mdStyle.css">'
        '<meta charset="utf-8">'
        '</head>\n<body>')

f.write(prefaceHtml)
for dt in rrule.rrule(rrule.MONTHLY,dtstart=c.dtToday,until=max(calDtList)):
    f.write(c.formatMonthMd(dt.year,dt.month,calDictHtml))

f.write('</body></html>')
f.close()
print('calendar written')

# Write cleaned up MD file
# ---------------------------------
f_new = open('calendar_new.txt','w')
f_new.write(preface)
f_new.write('---' + '\n\n')
calDtList = sorted(calDtList)
for dt in calDtList:
    if dt.date() >= c.dtToday:
        f_new.write('### ' + dt.strftime('%A, %B %d, %Y') + '\n')
        f_new.write(calDict[dt.strftime('%Y-%m-%d')])
f_new.close()

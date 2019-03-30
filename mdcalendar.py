import mistune
from dateutil import parser,rrule 
import calendarClass
import datetime
try:
    import mdCalendarConfig as cfg
except ModuleNotFoundError:
    f_cfg = open('mdCalendarConfig.py','w')
    f_cfg.write("mdInPath = '/path/to/calendar.md'\n")
    f_cfg.write("mdOutPath = '/path/to/calendar_cleaned.md'\n")
    f_cfg.write("calendarOutPath = '/path/to/calendar.html'\n")
    f_cfg.write("cssPath = 'mdStyle.css'")
    f_cfg.close()
    import mdCalendarConfig as cfg

# Helper Functions
# ---------------------------------
def eomDt(dt):
    nextMo = dt.replace(day=28) + datetime.timedelta(days=4)
    return nextMo - datetime.timedelta(days=nextMo.day)

# Read and parse the markdown file
# ---------------------------------
f_md = open(cfg.mdInPath,'r')

isPreface = True
preface = ""

calDtList = []
calDict = {}
calKey = None
calCustomIdDict = {}

for line in f_md:
    line = line.strip()

    if line[0:4]=="### ":
        isPreface = False
        # Custom Ids
        if ("(" in line) and (")" in line):
            customId = line[line.find("("):line.find(")")+1]
            line = line.replace(customId,"")
            customId = customId[1:-1]
        else:
            customId = ""

        # Regular Events
        thisDt = parser.parse(line[4:])
        calKey = thisDt.strftime('%Y-%m-%d')
        if calKey not in calDict:
            calDtList.append(thisDt)
            calDict[calKey] = ''
            calCustomIdDict[calKey] = customId

    elif line[0:5]=="+ ":
        # Recurring Events
        isPreface = False
        # not implemented yet

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
f = open(cfg.calendarOutPath,'w')
f.write('<html>\n<head>\n'
        '<link rel="stylesheet" type="text/css" href="' + cfg.cssPath + '">'
        '<meta charset="utf-8">'
        '</head>\n<body>')

f.write(prefaceHtml)
eDt = eomDt(max(calDtList))
for dt in rrule.rrule(rrule.MONTHLY,dtstart=c.dtToday,until=eDt):
    f.write(c.formatMonthMd(dt.year,dt.month,calDictHtml,calCustomIdDict))

f.write('</body></html>')
f.close()
print('calendar written')

# Write cleaned up MD file
# ---------------------------------
f_new = open(cfg.mdOutPath,'w')
f_new.write(preface)
f_new.write('---' + '\n\n')

calDtListOLD = []
calDtList = sorted(calDtList)
for dt in calDtList:
    if dt.date() >= c.dtToday:
        f_new.write('### ' + dt.strftime('%A, %B %d, %Y') + '\n')
        f_new.write(calDict[dt.strftime('%Y-%m-%d')])
    else:
        calDtListOLD.append(dt)
f_new.write('---' + '\n\n')
for dt in calDtListOLD:
    f_new.write('### ' + dt.strftime('%A, %B %d, %Y') + '\n')
    f_new.write(calDict[dt.strftime('%Y-%m-%d')])

f_new.close()

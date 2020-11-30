import mistune
from dateutil import parser,relativedelta
import calendarClass
import datetime
import argparse


argParser = argparse.ArgumentParser()
argParser.add_argument('--full', help='write entire calendar to HTML', action='store_true')
args = argParser.parse_args()

# Pull in config file, create one if it doesn't exits
# ---------------------------------
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

status = "pre" # pre, cal, rec

# stuff will get added to these
# as it loops through the file
preface = ""
calDtList = []
calDict = {}
calKey = None
calCustomIdDict = {}
rrDtList = []
rrDict = {}

# read through the file
for line in f_md:
    line = line.strip()

    if line[0:4]=="### ":
        # calendar section

        status = "cal"
        # look for Custom Ids e.g '(travel)'
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
        #else:
            # not implemented

    elif line[0:2]=="+ ":

        # Recurring Events
        status = "rec"
        thisDt = parser.parse(line[2:line.find('-')])
        calKey = thisDt.strftime('%Y-%m-%d')
        if calKey not in rrDict:
            rrDtList.append(thisDt)
            rrDict[calKey] = line[line.find('-'):]
        else:
            rrDict[calKey] += '\n'+ line[line.find('-'):]

    else:
        # just append to the dict for that date
        if status=="cal" and not (line[0:3]=="---"):
            calDict[calKey] += line + '\n'
        if status=="rec" and not (line[0:3]=="---"):
            rrDict[calKey] += line + '\n'

    if status=="pre" and not (line[0:3]=="---"):
        # append to the preface
        preface += line + '\n'
        
f_md.close()

# parse the markdown into HTML
prefaceHtml = mistune.markdown(preface)
calDictHtml = {}
rrDictHtml = {}
for key in calDict:
    calDictHtml[key] = mistune.markdown(calDict[key])
for key in rrDict:
    rrDictHtml[key] = "<i>" + mistune.markdown(rrDict[key]) + "</i>"

# Open the HTML file and write to it 
# ---------------------------------
c = calendarClass.mdCalendar()
f = open(cfg.calendarOutPath,'w')
f.write('<html>\n<head><title>MDcalendar</title>\n'
        '<link rel="stylesheet" type="text/css" href="' + cfg.cssPath + '">'
        '<meta charset="utf-8">'
        '</head>\n<body>')

f.write(prefaceHtml)

eDt = eomDt(max(calDtList)).date()
if args.full:
    dt = min(calDtList).date()
else:
    dt = c.dtToday
while dt <= eDt:
    f.write(c.formatMonthMd(dt.year,dt.month,calDictHtml,rrDictHtml,calCustomIdDict))
    dt = dt + relativedelta.relativedelta(months=+1)
f.write('</body></html>')
f.close()
print('calendar written')

# Write cleaned up MD file
# ---------------------------------
f_new = open(cfg.mdOutPath,'w')
f_new.write(preface)
f_new.write('---' + '\n\n')

# write the calendar portion
calDtListOLD = []
calDtList = sorted(calDtList)
for dt in calDtList:
    if dt.date() >= c.dtToday:
        thisDtStr = dt.strftime('%Y-%m-%d')
        f_new.write('### ' + dt.strftime('%A, %B %d, %Y'))
        if calCustomIdDict[thisDtStr]:
            f_new.write(' (' + calCustomIdDict[thisDtStr] + ')')
        f_new.write('\n' + calDict[dt.strftime('%Y-%m-%d')])
    else:
        calDtListOLD.append(dt)

# write the recurring events
f_new.write('---' + '\n\n')
rrDtList = sorted(rrDtList)
for dt in rrDtList:
    thisDtStr = dt.strftime('%Y-%m-%d')
    rrDict[thisDtStr] = rrDict[thisDtStr].replace('\n- ','\n+ ' + dt.strftime('%m/%d') + ' - ')
    if rrDict[thisDtStr][0:2] == '- ':
        rrDict[thisDtStr] = rrDict[thisDtStr][2:]
    f_new.write('+ ' + dt.strftime('%m/%d') + ' - ' + rrDict[thisDtStr] + '\n')

# write the old calendar
f_new.write('---' + '\n\n')
for dt in calDtListOLD:
    thisDtStr = dt.strftime('%Y-%m-%d')
    f_new.write('### ' + dt.strftime('%A, %B %d, %Y'))
    if calCustomIdDict[thisDtStr]:
        f_new.write(' (' + calCustomIdDict[thisDtStr] + ')')
    f_new.write('\n' + calDict[dt.strftime('%Y-%m-%d')])

f_new.close()

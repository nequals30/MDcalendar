"""
This extends the HTMLCalendar class from calendar.
All aesthetic adjustments should be made in the mdStyle.css function
"""
from calendar import HTMLCalendar
import datetime

# Extending HTMLCalendar class from calendar
class mdCalendar(HTMLCalendar):

    def __init__(self,firstweekday=6):
        self.firstweekday = firstweekday
        self.cssclass_today = "today"
        self.dtToday = datetime.datetime.today().date()

    def formatMonthMd(self, theyear, themonth, mdList):
        v=[]
        a = v.append
        a('<table '
          'width="100%%" '
          'cellpadding="0" '
          'cellspacing="0" '
          'class="%s">' % (self.cssclass_month))
        a('\n')
        a(self.formatmonthname(theyear,themonth))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweekMd(week,themonth,theyear,mdList))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatweekMd(self,theweek,mo,yr,mdList):
        # just passes mdList through
        s = ''.join(self.formatdayMd(d,wd,mo,yr,mdList) for (d,wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatdayMd(self,day,weekday,mo,yr,mdList):
        if day == 0:
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            thisDay = datetime.date(yr,mo,day)
            thisDayStr = thisDay.strftime('%Y-%m-%d')

            if thisDay == self.dtToday:
                dayCssClass = self.cssclass_today
            elif thisDay < self.dtToday:
                dayCssClass = self.cssclasses[weekday] + " crossed"
            else:
                dayCssClass = self.cssclasses[weekday]
            

            if thisDayStr in mdList:
                dayContents = mdList[thisDayStr]
            else:
                dayContents = ''

            return ('<td height="100px" width="14%%" class="%s">%d<br/>'+ 
                     dayContents +
                    '</td>') % (dayCssClass,day)

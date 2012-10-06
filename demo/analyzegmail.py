"""
Analyzing your Gmail with Matplotlib

Lately, I read this post about using Mathematica to analyze a Gmail account. I
found it very interesting and I worked a with imaplib and matplotlib to create
two of the graph they showed:

A diurnal plot, which shows the date and time each email was sent (or received),
with years running along the x axis and times of day on the y axis.

And a daily distribution histogram, which represents the distribution of emails
sent by time of day.

In order to plot those graphs I created three functions. The first one, retrieve
the headers of the emails we want to analyze:
"""

try:
    from debug import ip
except ImportError:
    pass

from sys import argv
from getpass import getpass
from imaplib import IMAP4_SSL
from datetime import date, timedelta, datetime
from time import mktime
from pylab import plot_date, show, xticks, date2num
from pylab import figure, hist, num2date
from matplotlib.dates import DateFormatter
import dateutil
from iterextras import iterview
from terminal import marquee

def get_headers(address, password, folder, d):
    """ Retrieve headers of the emails from d days ago until now. """
    # imap connection
    mail = IMAP4_SSL('imap.gmail.com')
    mail.login(address,password)
    mail.select(folder)
    # retrieving the uids
    interval = (date.today() - timedelta(d)).strftime("%d-%b-%Y")
    [_, data] = mail.uid('search', None,
                         '(SENTSINCE {date})'.format(date=interval))
    # retrieving the headers
    [_, data] = mail.uid('fetch', data[0].replace(' ',','),
                         '(BODY[HEADER.FIELDS (DATE)])')
    mail.close()
    mail.logout()
    return data


def plot_diurnal(headers):
    """
    Diurnal plot of the emails, with years running along the x axis and times of
    day on the y axis.
    """
    xday = []
    ytime = []
    print 'making diurnal plot...'
    for h in iterview(headers):
        if len(h) > 1:
            try:
                s = h[1][5:].strip()
                x = dateutil.parser.parse(s)
            except ValueError:
                print
                print marquee(' ERROR: skipping ')
                print h
                print marquee()
                continue
            timestamp = mktime(x.timetuple())   # convert datetime into floating point number
            mailstamp = datetime.fromtimestamp(timestamp)
            xday.append(mailstamp)
            # Time the email is arrived
            # Note that years, month and day are not important here.
            y = datetime(2010, 10, 14, mailstamp.hour, mailstamp.minute, mailstamp.second)
            ytime.append(y)
    plot_date(xday,ytime,'.',alpha=.7)
    xticks(rotation=30)
    return xday,ytime


def plot_daily_distribution(ytime):
    """ Histogram of the daily distribution. """
    # converting dates to numbers
    numtime = [date2num(t) for t in ytime]
    # plotting the histogram
    ax = figure().gca()
    [_, _, patches] = hist(numtime, bins=24,alpha=.5)
    # adding the labels for the x axis
    tks = [num2date(p.get_x()) for p in patches]
    xticks(tks, rotation=75)
    # formatting the dates on the x axis
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))


def main():
    print 'Fetching emails...'
    email = argv[1]
    pw = getpass()
    headers = get_headers(email, pw,
                          #'inbox',
                          #'[Gmail]/Sent Mail',
                          '[Gmail]/All Mail',
                          365*5)

    print 'Plotting some statistics...'
    xday, ytime = plot_diurnal(headers)
    plot_daily_distribution(ytime)
    print len(xday),'Emails analysed.'
    show()


if __name__ == '__main__':
    main()

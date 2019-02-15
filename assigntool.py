#!/home/namato/anaconda3/bin/python

# XXX needed because of
# https://github.com/Anorov/PySocks/issues/119
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

# Import the Canvas class
from canvasapi import Canvas
import argparse
import sys
from pprint import pprint
import tempfile
import pycurl
import os
import string

# Canvas API URL + KEY
API_URL = "https://mycampus.instructure.com"
API_KEY = ""

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

def dejunk(s):
    t = str.maketrans({key: None for key in string.punctuation})
    newstr = s.translate(t)
    newstr = newstr.replace(" ", "_")
    return (newstr)

def main():
    parser = \
        argparse.ArgumentParser(description='List and download assignment submissions from Canvas.')
    parser.add_argument('course_id',
            metavar='COURSE_ID', type=int,
            help='course ID for the assignment')
    parser.add_argument('-a', metavar="ID",
            help='Assignment ID')
    parser.add_argument('-d', action='store_true',
            help='Download all submissions')
    parser.add_argument('-s', metavar = "DIR",
            help='Save downloaded submissions to directory')
    args = parser.parse_args()

    if (args.d == False):
        course = canvas.get_course(args.course_id)
        am = course.get_assignments()
        for a in am:
             if (args.a == None or args.a in str(a)):
                    print(a)
        sys.exit(0)

    d = None
    if (args.a == None):
        print('Must supply -a <ASSIGNMENT> with this option')
        sys.exit(-1)

    if (args.s != None):
        d = args.s
    else:
        print('Using a temporary directory')
        d = tempfile.mkdtemp()

    print('Saving to directory %s' % d)
    
    course = canvas.get_course(args.course_id)
    a = course.get_assignment(args.a)
    slist = a.get_submissions()
    for s in slist:
        #pprint(s)
        #print(s.user_id)
        u = course.get_user(s.user_id)
        uname = u.name
        cnt = 0
        #print(uname)
        if (hasattr(s, 'attachments')):
            udir = '%s/%s' % (d, dejunk(uname))
            os.mkdir(udir)
            for att in s.attachments:
                cnt += 1
                fn = att['filename']
                #print('\tattachment %s' % fn)
                #pprint(att)
                with open('%s/%s' % (udir, fn), 'wb') as of:
                    c = pycurl.Curl()
                    c.setopt(c.URL, att['url'])
                    c.setopt(c.WRITEDATA, of)
                    c.setopt(c.FOLLOWLOCATION, True)
                    c.perform()
                    c.close()
            print('saved %d attachments for user %s' % (cnt, uname))

if __name__ == "__main__":
    main()

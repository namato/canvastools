#!/home/namato/anaconda3/bin/python

# XXX needed because of
# https://github.com/Anorov/PySocks/issues/119
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

from canvasapi import Canvas
import argparse
import sys
from pprint import pprint
from canvasgrader import CanvasGrader
import time
import datetime

# add your info here
API_URL = "https://mycampus.instructure.com"
API_KEY = ""

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

def doprompt_student(name, override):
    if (override == True):
        print('Matched student %s' % name)
        return True
    a = str(input('Matched student %s, upload score? (Y/n): ' % name)).lower().strip()
    try:
        if a[0] == 'y':
            return True
        elif a[0] == 'n':
            return False
        else:
            print('Please enter \'y\' or \'n\'')
            return doprompt_student()
    except Exception as e:
        print('Please enter \'y\' or \'n\'')
        print(e)
        return doprompt_student()

def doprompt_late(pts, sc, override):
    if (override == True):
        return True
    a = str(input("Submission was %d days late, subtract %d points (new score: %d)?" %
              (pts, pts, sc - pts)))
    try:
        if a[0] == 'y':
            return True
        elif a[0] == 'n':
            return False
        else:
            print('Please enter \'y\' or \'n\'')
            return doprompt_late()
    except Exception as e:
        print('Please enter \'y\' or \'n\'')
        print(e)
        return doprompt_late()

def dejunk(s):
    t = str.maketrans({key: None for key in string.punctuation})
    newstr = s.translate(t)
    newstr = newstr.replace(" ", "_")
    return (newstr)

def main():
    parser = argparse.ArgumentParser(
            description='Award a point score in Canvas')
    parser.add_argument('course_id',
            metavar='COURSE_ID', type=int,
            help='course ID for the assignment')
    parser.add_argument('assign_id',
            metavar='ASSIGNMENT_ID', type=int,
            help='assign. ID to which to award score')
    parser.add_argument('name',
            metavar='NAME', type=str,
            help='quoted string, "firstname, lastname"')
    parser.add_argument('points',
            metavar='POINTS', type=int,
            help='points to award to the assignment')
    parser.add_argument('-c',
            help='Add a comment to the assignment')
    parser.add_argument('-y', action='store_true',
            help='Assume \'yes\' to confirm')
    args = parser.parse_args()

    cr = canvas.get_course(args.course_id)
    ids = [ [ n.sortable_name, n.id ] for n in cr.get_users(enrollment_type=['student']) ]
    choice = None
    for i in ids:
        if (args.name in i[0].split(',')[0]):
            if (doprompt_student(i[0], args.y)):
                choice = i[1]
                break
    if (choice == None):
        print('No student chosen or no matches, exiting')
        sys.exit(0)
    print('proceeding with id %d' % choice)

    a = cr.get_assignment(args.assign_id)
    s = a.get_submission(choice)
    due = a.due_at_date
    sa = datetime.datetime.strptime(s.submitted_at, "%Y-%m-%dT%H:%M:%S%z")
    l = sa - due
    dlate = l.days
    if (l.days == 0 and l.seconds > 0):
        dlate = 1
    if (dlate > 0):
        if (doprompt_late(dlate, args.points, args.y)):
            args.points -= dlate
            print('Proceeding with late deduction of %d points (to %d)' % (dlate, args.points))

    grades_for_canvas = {}
    k1 = 'grade_data[{student_id}][posted_grade]'.format(student_id=choice)
    grades_for_canvas[k1] = args.points
    if (args.c != None):
        k2 = 'grade_data[{student_id}][text_comment]'.format(student_id=choice)
        grades_for_canvas[k2] = args.c
    assign = cr.get_assignment(args.assign_id)
    status = assign.submissions_bulk_update(**grades_for_canvas)
    pct = status.completion
    while (True):
        if (pct == None):
            pct = 0
        sys.stdout.write("\r%d%%" % pct)
        sys.stdout.flush()
        if (pct == 100):
            print('...done')
            break
        time.sleep(1)
        pct = status.query().completion

if __name__ == "__main__":
    main()

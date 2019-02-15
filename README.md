
## canvastools

A set of scripts for finding and scoring assignments in Canvas from the command line.

### Requirements

- Python 3.7 or higher
- canvasapi
- pycurl

### Usage

Add your API_URL and API_KEY credentials at the top of each file.  Get the course ID from the
URL of the course, for example, https://mycollege.instructure.com/courses/123456/settings (in this
case the ID is '123456'.)

#### Getting Assignments

```
    assigntool.py
```

can be used to locate the IDs for assignments in a course.  Examples:

```
    assigntool.py 123456
```

 will list all of the assignments and the associated IDs, for course 123456.

```
    assigntool.py 123456 -a 111222
```

will list the assignment with ID 111222.

```
    assigntool.py 123456 -a Recursion
```

will list all assignments with 'Recursion' in the title.

```
    assigntool.py 123456 -a 111222 -d
```

will download all submissions for assignment 111222 into an automatically generated tmpdir.

```
    assigntool.py 123456 -a 111222 -d -s /home/foo/course/assign1
```

will download all submissions for assignment 111222 into the directory /home/foo/course/assign1.
Each submission will be in its own directory titled with the name of the student. This will only
download the *latest* copy of each submission.

#### Scoring Assignments

Use
```
    scoreit.py
```
to assign scores and (optionally) text comments with assignment submissions.

```
    scoreit.py 123456 111222 Schwarzenegger 20
```

will assign the score of 20 to user Schwarzenegger for assignment 111222 in course 123456.
The script will always prompt to ensure that it has found the right user, override this with the
-y option. In the case of multiple matches, simply press 'n' until the correct match is found.  For example:

```
# scoreit.py 123456 111222 Schwarzenegger 20
Matched student Schwarzenegger, Arnold, upload score (y/n): n
Matched student Schwarzenegger, Katherine, upload score (y/n): y
100%...done
```
You can also use the -c option to add a comment:
```
    scoreit.py -c "You'll be back" 123456 111222 Schwarzenegger 20
```

#### Other 

The intended general workflow is:
- Use assigntool.py to determine the ID of an assignment
- Download all the submissions for that assignment into a directory
- Read/compile each student's entry
- Upload the score and comments with scoreit.py

Feedback/improvements welcome.

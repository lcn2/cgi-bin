#!/bin/sh
# @(#)html.cat	1.1 10 Oct 1995 03:23:08
#
# html.cat - cat a file containing html in raw form
#
# usage:
#	xxx.cat
#
#	Cat the file xxx so that the reader does not interpret the
#	usual html magic characters.  The basename (minus the .cat)
#	is the file to cat.


# html header goodies
#
echo "content-type: text/html

"
echo "<pre>"

# pump out the file
#
/sbin/sed -f html.sed `/sbin/basename $0 .cat`

# final html
#
echo "</pre>"

#!/bin/sh
# @(#)html	1.1 10 Oct 1995 03:23:08
#
# html - cat a file containing html in raw form
#
# usage:
#	xxx.cat
#
#	Cat the file xxx so that the reader does not interpret the
#	usual html magic characters.  The basename (minus the .cat)
#	is the file to cat.

# setup
#
argv0="`/sbin/basename $0 .cat`"
export argv0


# special code to explain how to use html.cat
#
# This section is only invoked if we are executoed as html.cat.cat
#
if [ X"$argv0" = X"html.cat" ]; then

    # we are being executed as html.cat, display info about html.cat
    #
    /sbin/cat <<HTML_INFO1 | sed -e 's/^    //'
    <HTML>
    <HEAD>
    <TITLE> How to use html.cat </TITLE>
    </HEAD>

    <BODY>
    <H1> How to use html.cat </H1>

    <HR>

    The <B>html.cat</B> cgi script allows one to view the source of
    a selected cgi-bin script.

    <P></P>

    Say you want to be able to view the file <B>test.cgi</B>.  If the
    cgi-bin file <B>test.cgi.bin</B> is a link to <B>html.cat</B>
    then execution of the URL:

    <P></P>

    <DD><A HREF="http://prime.corp.sgi.com/cgi-bin/test.cgi.bin">
    http://prime.corp.sgi.com/cgi-bin/test.cgi.bin</A><BR>
    or:<DD><A HREF="http:/cgi-bin/test.cgi.bin">http:/cgi-bin/test.cgi.bin</A>

    <P></P>

    will display the contents of <B>test.cgi</B>.

    <P></P>

    <HR>

    <P></P>

    This html document was produced by <B>html.cat</B>.  The source to
    this script is as follows:

    <P></P>

    <PRE>
HTML_INFO1

    # display the source to html.cat
    #
    /sbin/sed -f html.sed "$argv0" | sed -e 's/^/    /'

    # display the remainder of the info
    #
    /sbin/cat <<HTML_INFO2 | sed -e 's/^    //'
    </PRE>

    <P></P>

    <HR>

    <ADDRESS>
    Landon Curt Noll 
    (<A HREF="//prime.corp.sgi.com/chongo.html">chongo@corp.sgi.com</a>)<br>
    <A HREF="//prime.corp.sgi.com/cjew.html">chongo</a> &lt; was here &gt;
    <A HREF="//prime.corp.sgi.com/faq/bat.html"><strong>/\oo/\</strong></a>
    </ADDRESS>
    </BODY>
    </HTML>
HTML_INFO2

    # all done with displaying information
    #
    exit 0
fi

# html header goodies
#
echo "content-type: text/html

"
echo "<PRE>"

# pump out the file
#
/sbin/sed -f html.sed "$argv0"

# final html
#
echo "</PRE>"

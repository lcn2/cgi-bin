#!/bin/sh
# @(#)cgibin	1.1 10 Oct 1995 03:23:08
#
# cgibin - cat a cgi-bin script in html form
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


# special code to explain how to use cgibin
#
# This section is only invoked if we are executoed as cgibin.cat
#
if [ X"$argv0" = X"cgibin" ]; then

    # we are being executed as cgibin.cat, display info about cgibin.cat
    #
    /sbin/cat <<HTML_INFO1 | sed -e 's/^    //'
    content-type: text/html

    <HTML>
    <HEAD>
    <TITLE> How to use cgibin </TITLE>
    </HEAD>

    <BODY>
    <H1> How to use cgibin </H1>

    <HR>

    The <B>cgibin.cat</B> cgi script allows one to view the source of
    a selected cgi-bin script.

    <P></P>

    Say you want to be able to view the file <B>test.cgi</B>.  If the
    cgi-bin file <B>test.cgi.bin</B> is a link to <B>cgibin.cat</B>
    then execution of the URL:

    <P></P>

    <DD><A HREF="http://prime.corp.sgi.com/cgi-bin/test.cgi.cat">
    http://prime.corp.sgi.com/cgi-bin/test.cgi.cat</A><BR>
    or:<DD><A HREF="http:/cgi-bin/test.cgi.cat">http:/cgi-bin/test.cgi.cat</A>

    <P></P>

    will display the contents of <B>test.cgi</B>.

    <HR>

    This html document that you are <I>now</I>
    viewing was produced by <B>cgibin</B>.  
    The source to <B>cgibin</B> is as follows:

    <P></P>

    <CODE>
    <PRE>
HTML_INFO1

    # display the source to cgibin
    #
    /sbin/sed -f html.sed "$argv0"

    # display the remainder of the info
    #
    /sbin/cat <<HTML_INFO2 | sed -e 's/^    //'
    </PRE>
    </CODE>

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
/sbin/cat <<HTML_INFO3
content-type: text/html

<HTML>
<HEAD>
<TITLE> $argv0 source listing </TITLE>
</HEAD>

<H1> <A HREF="http://prime.corp.sgi.com/cgi-bin/$argv0">
http://prime.corp.sgi.com/cgi-bin/$argv0</A>
source listing
</H1>

<HR>

<CODE>
<PRE>
HTML_INFO3

# pump out the file
#
/sbin/sed -f html.sed "$argv0"

# final html
#
/sbin/cat <<HTML_INFO4
</PRE>
</CODE>

<HR>

<ADDRESS>
Landon Curt Noll 
(<A HREF="//prime.corp.sgi.com/chongo.html">chongo@corp.sgi.com</a>)<br>
<A HREF="//prime.corp.sgi.com/cjew.html">chongo</a> &lt; was here &gt;
<A HREF="//prime.corp.sgi.com/faq/bat.html"><strong>/\oo/\</strong></a>
</ADDRESS>
</BODY>
</HTML>
HTML_INFO4

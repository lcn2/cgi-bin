#!/bin/sh
# @(#)cgicat	1.1 10 Oct 1995 03:23:08
#
# cgicat - cat a cgi-bin script in html form
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


# special code to explain how to use cgicat
#
# This section is only invoked if we are executed as cgicat.cat
#
if [ X"$argv0" = X"cgicat" ]; then

    # we are being executed as cgicat.cat, display info about cgicat.cat
    #
    /sbin/cat <<HTML_INFO1 | sed -e 's/^    //'
    content-type: text/html

    <HTML>
    <HEAD>
    <TITLE> How to use cgicat </TITLE>
    </HEAD>

    <BODY BGCOLOR="#80A0C0">
    <H1> How to use cgicat </H1>

    <HR>

    The <B>cgicat.cgi</B> cgi script allows one to view the source of
    a selected cgi-bin script.

    <P></P>

    Say you want to be able to view the file <B>test.cgi</B>.  If the
    cgi-bin file <B>test.cgi.cat</B> is a link to <B>cgicat.cgi</B>
    then execution of the URL:

    <P></P>

    <DD><A HREF="http://prime.csd.sgi.com/cgi-bin/test.cgi.cat">
    http://prime.csd.sgi.com/cgi-bin/test.cgi.cat</A>

    <P></P>

    will display the contents of <B>test.cgi</B>.

    <HR>

    The following are some cgi-bin scripts that you can view:

    <P></P>

    <UL>
    <DD><LI><A HREF="http://prime.csd.sgi.com/cgi-bin/hitcount.cgi.cat">
    hitcount.cgi</A> (maintain and display page usage count)<BR>
    <DD><LI><A HREF="http://prime.csd.sgi.com/cgi-bin/html.cgi.cat">
    html.cgi</A> (an example of an CGI returning HTML)<BR>
    <DD><LI><A HREF="http://prime.csd.sgi.com/cgi-bin/test.cgi.cat">
    test.cgi</A> (test server for CGI/1.1 conformance)<BR>
    <DD><LI><A HREF="http://prime.csd.sgi.com/cgi-bin/versions-b.cgi.cat">
    versions-b.cgi</A> (display versions -b output)<BR>
    </UL>

    and here is where you can run them:

    <P></P>

    <UL>
    <DD><LI><A HREF="http://prime.csd.sgi.com/cgi-bin/hitcount.cgi?hitcount+o">
    hitcount.cgi</A> (maintain and display page usage count)<BR>
    <DD><LI><A HREF="http://prime.csd.sgi.com/cgi-bin/html.cgi">
    html.cgi</A> (an example of an CGI returning HTML)<BR>
    <DD><LI><A HREF="http://prime.csd.sgi.com/cgi-bin/test.cgi">
    test.cgi</A> (test server for CGI/1.1 conformance)<BR>
    <DD><LI><A HREF="http://prime.csd.sgi.com/cgi-bin/versions-b.cgi">
    versions-b.cgi</A> (display versions -b output)<BR>
    </UL>

    <HR>

    This html document that you are <I>now</I>
    viewing was produced by <B>cgicat.cgi</B>.  
    The source to <B>cgicat.cgi</B> is as follows:

    <P></P>

    <CODE>
    <PRE>
HTML_INFO1

    # display the source to cgicat
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
    (<A HREF="//prime.csd.sgi.com/chongo.html">chongo@sgi.com</a>)<br>
    <A HREF="//prime.csd.sgi.com/cjew.html">chongo</a> &lt; was here &gt;
    <A HREF="//prime.csd.sgi.com/faq/bat.html"><strong>/\oo/\</strong></a>
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

<BODY BGCOLOR="#80A0C0">
<H1> <A HREF="http://prime.csd.sgi.com/cgi-bin/$argv0">
http://prime.csd.sgi.com/cgi-bin/$argv0</A>
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
(<A HREF="//prime.csd.sgi.com/chongo.html">chongo@sgi.com</a>)<br>
<A HREF="//prime.csd.sgi.com/cjew.html">chongo</a> &lt; was here &gt;
<A HREF="//prime.csd.sgi.com/faq/bat.html"><strong>/\oo/\</strong></a>
</ADDRESS>
</BODY>
</HTML>
HTML_INFO4

#!/bin/sh
# @(#)html.cgi	1.4 10 Oct 1995 03:31:37
#
# html.cgi - an example of an CGI returning HTML

# we must first send our MIME type
#
echo Content-type: text/html

# we must next send a URL for another document, or an empty line
#
echo

# return the HTML document
#
cat <<END_OF_FILE
<HTML>
<HEAD>
<TITLE> HTML returned by html.cgi </TITLE>
</HEAD>

<BODY BGCOLOR="#80A0C0">
<H1> HTML returned by html.cgi </H1>

<HR>

This html document was produced by html.cgi. <P>

View the <A HREF="http://prime.csd.sgi.com/cgi-bin/html.cgi.cat">html.cgi</A> source.
<P>

Return to the <A HREF="//prime.csd.sgi.com/sample/cgi.html#example">CGI</A> 
example.

<HR>

<ADDRESS>
Landon Curt Noll 
(<A HREF="//prime.csd.sgi.com/chongo.html">chongo@sgi.com</a>)<br>
<A HREF="//prime.csd.sgi.com/cjew.html">chongo</a> &lt; was here &gt;
<A HREF="//prime.csd.sgi.com/faq/bat.html"><strong>/\oo/\</strong></a>
</ADDRESS>
</BODY>
</HTML>
END_OF_FILE

#!/usr/bin/perl -wT
# @(#)html.cgi	1.4 10 Oct 1995 03:31:37
#
# html.cgi - an example of an CGI returning HTML

# setup
#
use strict;
require 5.003;
select(STDOUT);
$| = 1;

# we must first send our MIME type
#
print "Content-type: text/html\n";

# we must next send a URL for another document, or an empty line
#
print "\n";

# return the HTML document
#
print <<END_OF_FILE;
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

Return to the <A HREF="//prime.csd.sgi.com/html/cgi.html#example">CGI</A> 
example.

<HR>

<ADDRESS>
Landon Curt Noll 
(<A HREF="//prime.csd.sgi.com/chongo.html">chongo\@sgi.com</a>)<br>
<A HREF="//prime.csd.sgi.com/cjew.html">chongo</a> &lt; was here &gt;
<A HREF="//prime.csd.sgi.com/html/bat.html"><strong>/\\oo/\\</strong></a>
</ADDRESS>
</BODY>
</HTML>
END_OF_FILE
exit(0);

#!/usr/bin/perl -wT
# @(#)html.cgi	1.4 10 Oct 1995 03:31:37
#
# html.cgi - an example of an CGI returning HTML

# setup
#
use strict;
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

View the <A HREF="/chongo/tech/comp/cgi/html.cgi.txt">html.cgi</A> source.
<P>

Return to the <A HREF="/chongo/tech/comp/cgi/cgidemo.html">CGI</A> 
sutff page.

<HR>

<H3>Author:</H3>
<BLOCKQUOTE>
<A HREF="/chongo/index.html">chongo</A>
&lt; Landon Curt Noll &gt;
<STRONG>/\\oo/\\</STRONG>
</BLOCKQUOTE>

</BODY>
</HTML>
END_OF_FILE
exit(0);

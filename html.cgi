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
<html>
<head>
<title> HTML returned by html.cgi </title>
</head>

<body>
<h1> HTML returned by html.cgi </h1>

<hr>

This html document was produced by html.cgi. <p>

View the <a href="http://prime.corp.sgi.com/cgi-bin/html.cgi.cat"> html.cgi</a> source.
<p>

Return to the <a href="//prime.corp.sgi.com/sample/cgi.html"> CGI</a> 
example.

<hr>

<address>
Landon Curt Noll 
(<a href="//prime.corp.sgi.com/chongo.html">chongo@corp.sgi.com</a>)<br>
<a href="//prime.corp.sgi.com/cjew.html">chongo</a> &lt; was here &gt;
<a href="//prime.corp.sgi.com/faq/bat.html"><strong>/\oo/\</strong></a>
</address>
</body>
</html>
END_OF_FILE

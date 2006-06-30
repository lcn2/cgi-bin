#!/usr/bin/perl -wT
#
# nothing.cgi - CGI to redirect user to another page
#
# @(#) $Revision: 1.17 $
# @(#) $Id: cgi-example.cgi,v 1.17 2006/06/27 15:59:21 root Exp root $
#
# usage:
#	nothing.cgi

# setup
#
use strict;

# I/O setup
#
close(STDIN);
select(STDOUT);
$| = 1;
$SIG{ALRM} = sub { print "Content-type: text/html\n\n" .
			 "HTML><HEAD><TITLE>timeout<//TITLE></HEAD><BODY> " .
			 "time limit </BODY></HTML>\n"; exit(1); };
alarm(5);

# my vars
#
my $redirect = "http://www.isthe.com/err/index.html";

# Output the redirection
#
print <<END_OF_FILE;
HTTP/1.0 302 Moved Temporarily
Connection: close
Content-Type: text/html; charset=ISO-8859-1
Location: $redirect

<HTML><HEAD><TITLE>302 Moved Temporarily</TITLE></HEAD>
<BODY>
<H1>302 Moved</H1>The document has moved
<A HREF="$redirect">here</A>.
</BODY></HTML>
END_OF_FILE

# all done
#
exit(0);

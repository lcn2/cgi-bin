#!/usr/bin/perl -wT
# @(#)cgicat	1.1 10 Oct 1995 03:23:08
#
# index.html.cgi - cat the generic index.html file
#
# usage:
#	index.html

# setup
#
use strict;

# I/O setup
#
close(STDIN);
select(STDOUT);
$| = 1;
$SIG{ALRM} = sub { print "content-type: text/html\n\n" .
			 "HTML><HEAD><TITLE>timeout<//TITLE></HEAD><BODY> " .
			 "time limit </BODY></HTML>\n"; exit(1); };
alarm(5);

# my vars
#
my $html;		# URL :-)
my $content;		# $html content

# open the html file
#
$html = "/err/index.html";
$html = "/web/isthe/chroot/index.html";    #-# real location
open(HTML, "<$html") ||
  die "content-type: text/html\n\n" .
      "<HTML><HEAD><TITLE>read error</TITLE></HEAD><BODY> " .
      "cannot open $html </BODY></HTML>\n";

# read in the entire file
#
undef $/;
$content = <HTML>;
if (! defined $content) {
  die "content-type: text/html\n\n" .
      "<HTML><HEAD><TITLE>read error</TITLE></HEAD><BODY> " .
      "cannot read $html </BODY></HTML>\n";
}

# write the entire file - ignore write errors
#
print "content-type: text/html\n\n";
print "$content";

# all done
#
exit(0);

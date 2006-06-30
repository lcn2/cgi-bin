#!/usr/bin/perl -wT
#
# cgi-example.cgi - Simple CGI Example #0
#
# @(#) $Revision: 1.17 $
# @(#) $Id: cgi-example.cgi,v 1.17 2006/06/27 15:59:21 root Exp root $
#
# NOTE: We added newlines to each CGI print statement to make the HTML output
#	a little easier for humans to read.  These \n's are not required.
#
# chongo (Landon Curt Noll, http://www.isthe.com/chongo/index.html) /\oo/\
#
# Share and enjoy! :-)

# requirements
#
use CGI qw(:standard);
use strict;

# For DOS (Denial Of Service) protection prevent file uploads and
# really big "POSTS"
#
$CGI::POST_MAX = 32768;		# max post size
$CGI::DISABLE_UPLOADS = 1;	# no uploads

# my vars
#
my $q;		# our CGI object

# setup
#
$q = new CGI;
if (cgi_error()) {
    print "Content-type: text/plain\n\n";
    print "Your browser sent bad or too much data!\n";
    print "Error: ", cgi_error(), "\n";
    exit(1);
}

# start off HTML header output
#
print $q->header, "\n";
print $q->start_html(-title => 'CGI Example #0',
		     -bgcolor => '#98B8D8'), "\n";
print $q->h1('CGI Example #0'), "\n";

# print something
#
print "Fizzbin ...", "\n";
print $q->p, "\n";
print $q->hr, "\n";

# our standard trailer
#
print "You can view the ";
print $q->a({-href => "/chongo/tech/comp/cgi/cgi-simple_cgi.txt"},
	    'source code'), "\n";
print " to this program.\n";
print $q->hr, "\n";
print $q->end_html, "\n";
exit(0);

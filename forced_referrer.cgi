#!/usr/bin/perl -wT
#
# forced_referrer.cgi - Example of forcing a referring URL to contain a string
#
# Copyright (c) 1999-2002 by Landon Curt Noll.  All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and
# its documentation for any purpose and without fee is hereby granted,
# provided that the above copyright, this permission notice and text
# this comment, and the disclaimer below appear in all of the following:
#
#       supporting documentation
#       source copies
#       source works derived from this source
#       binaries derived from this source or from derived source
#
# LANDON CURT NOLL DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO
# EVENT SHALL LANDON CURT NOLL BE LIABLE FOR ANY SPECIAL, INDIRECT OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
# USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
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
$CGI::POST_MAX = 1024;		# max post size
$CGI::DISABLE_UPLOADS = 1;	# no uploads

# my vars
#
my $q;          # our CGI object
my $myself;     # this URL
my $mysrc;	# name of this source file

# URL info
#
# The HTTP_REFERER must contain with $referrer_url or we will
# ask them to visit $bounce_url first.
#
my $referrer_url = "/chongo/tech/comp/cgi/referrer/";
my $bounce_url = "/chongo/tech/comp/cgi/referrer/index.html";
my $timeout = 6;

# setup
#
$q = new CGI;
if (cgi_error()) {
    print "Content-type: text/plain\n\n";
    print "Your browser sent bad or too much data!\n";
    print "Error: ", cgi_error(), "\n";
    exit(1);
}
($myself = $q->self_url) =~ s/\?.*$//;
$myself =~ s/.*\///;
$mysrc = "${referrer_url}${myself}.txt";
$mysrc =~ s/\.cgi/_cgi/;

# If we did not come from the right URL, bounce them back
# to where they should have come from in the first place.
#
if (!defined($ENV{'HTTP_REFERER'})) {
    $ENV{'HTTP_REFERER'} = ' << NO HTTP_REFERER FOUND >> ';
}
if ($ENV{'HTTP_REFERER'} !~ /\Q$referrer_url\E/) {
    print $q->header(-refresh => "$timeout; url=$bounce_url");
    print $q->start_html(-title => 'Forced Referer demo',
			 -bgcolor => '000000',
			 -link => '#FF0000',
			 -vlink => '#FFF000',
			 -text => '#FFFFFF');
    print $q->h2('Access Denied');
    print "\nSorry, you may only access the\n";
    print $q->b("forced referrer CGI");
    print "\nvia the URLs that contain the string:\n";
    print $q->br;
    print $q->br;
    print $q->blockquote($q->b($referrer_url));
    print $q->p;
    print "\nYour previous URL:\n";
    print $q->blockquote($q->b($q->a({'href' => $ENV{'HTTP_REFERER'}},
			 $ENV{'HTTP_REFERER'})));
    print $q->p;
    print "\ndid not contain that string.\n";
    print $q->p;
    print "\nIf your browser supports it, in $timeout seconds, you will\n";
    print "be moved to the ";
    print $q->b($q->a({-href => $bounce_url}, 'forced referrer demo'));
    print "\npage or you may click on that link to go there now.\n";
    print $q->p;
    print "\nFYI: The\n";
    print $q->a({-href => "${mysrc}"}, 'source');
    print "\nfor this CGI is available.\n";
    print $q->p;
    print $q->end_html;
    exit(1);
}

# The HTTP_REFERER is good, so tell them they are successful.
#
print $q->header;
print $q->start_html(-title => 'Forced Referer demo',
		     -bgcolor => '#98B8D8');
print $q->h2('Success');
print "\nBecause your previous URL:\n";
print $q->br;
print $q->br;
print $q->blockquote($q->a({-href => $ENV{'HTTP_REFERER'}},
		     $ENV{'HTTP_REFERER'}));
print $q->p;
print "\ncontained the string:\n";
print $q->br;
print $q->blockquote($q->b($referrer_url));
print $q->p;
print "\nand so you were allowed to access the\n";
print $q->i("forced referrer CGI");
print ".\n";
print $q->p;
print "\nFYI: The\n";
print $q->a({-href => "${mysrc}"}, 'source');
print "\nfor this CGI is available.\n";
print $q->p;
print "\nGo ";
print $q->a({-href => "${bounce_url}"}, 'back'), ".\n";
print $q->end_html;
exit(0);

#!/usr/bin/perl -wT
#
# cookie.cgi - get and set cookies
#
# NOTE: We added newlines to each CGI print statement to make the HTML output
#	a little easier for humans to read.  These \n's are not required.
#
# @(#) $Revision: 1.13 $
# @(#) $Id: cgi-example.cgi,v 1.13 2002/03/14 20:09:54 chongo Exp $
# @(#) $Source: /web/isthe/chroot/cgi-bin/RCS/cgi-example.cgi,v $
#
# Copyright (c) 2002 by Landon Curt Noll.  All Rights Reserved.
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
use Sys::Hostname;
use CGI::Cookie;
use CGI::Carp;
use strict;

# For DOS (Denial Of Service) protection prevent file uploads and
# really big "POSTS"
#
$CGI::POST_MAX = 1024;		# max post size
$CGI::DISABLE_UPLOADS = 1;	# no uploads

# my vars
#
my $q;		# our CGI object
my $myself;	# this URL
my %cookies;	# collection of cookies returned by the browser
my $cookie_set;	# collection of all cookies
my $cookie;	# individual cookie

# setup
#
$q = new CGI;
if (cgi_error()) {
    print "Content-type: text/plain\n\n";
    print "Your browser sent bad or too much data!\n";
    print "Error: ", cgi_error(), "\n";
    exit(1);
}

# fetch all of the cookies give to us by the browser
#
%cookies = fetch CGI::Cookie;

# all/alter the cookie set
#
if (defined $q->param('name') && defined $q->param('value')) {
    $cookie = new CGI::Cookie(-name => $q->param('name'),
    			       -value => $q->param('value'));
    $cookie->domain($q->param('domain')) if defined $q->param('domain');
    $cookie->path($q->param('path')) if defined $q->param('path');
#   $cookie->secure($q->param('secure')) if defined $q->param('secure');
    $cookies{$q->param('name')} = $cookie;
}

# build up a string containing all of the cookies
#
$cookie_set = "";
foreach (keys %cookies) {
    $cookie_set .= ";" if (length($cookie_set) > 0);
    $cookie_set .= $cookies{$_}->as_string;
}

# start off HTML header output
#
if (length($cookie_set) > 0) {
    print $q->header(-cookie => $cookie_set), "\n";
} else {
    print $q->header(), "\n";
}
print $q->start_html(-title => 'CGI Example #1',
		     -bgcolor => '#98B8D8'), "\n";
print $q->h1('CGI Example #1'), "\n";

# print the HTML form
#
print $q->start_form(-method => 'POST'), "\n";
print "cookie name: ", "\n";
print $q->textfield(-name => 'name',
		    -default => 'cookie_name'), "\n";
print $q->br, "\n";
print "cookie value: ", "\n";
print $q->textfield(-name => 'value',
		    -default => 'cookie_value'), "\n";
print $q->p, "\n";
print "cookie host: ", "\n";
# NOTE: Our internal web server's hostname is different from the
#	www.isthe.com, which is bound in an external interface.
#	We cannot simply call hostname() because the browser
#	thinks it is talking to the www.isthe.com server,
#	So we must hard code our default domain.  On the other
#	hand the form allows you to change the domain value ...
print $q->textfield(-name => 'domain',
		    -default => 'www.isthe.com'), "&nbsp;(domain)\n";
print $q->br, "\n";
print "cookie path: ", "\n";
print $q->textfield(-name => 'path',
		    -default => '/'), "\n";
#print $q->p, "\n";
#print "Secure: ", "\n";
#print $q->checkbox(-name => 'secure',
#		   -checked => '',
#		   -value => 'true',
#		   -label => ' <== send only over SSL'), "\n";
print $q->p, "\n";
print $q->submit(-name => 'Submit'), "\n";
print $q->end_form, "\n";
print $q->hr, "\n";

# print the cookies we will send
#
print $q->h2('Cookies sent on Submit');
foreach (keys %cookies) {
    print $cookies{$_}->as_string;
    print $q->br, "\n";
}
print $q->hr, "\n";

# print the cookie header
#
print $q->h2('HTTP Set-Cookie header sent on Submit'), "\n";
if (length($cookie_set) > 0) {
    print $q->pre("Set-Cookie: $cookie_set"), "\n";
} else {
    print "No Set-Cookie header was sent\n";
}
print $q->hr, "\n";


# our standard trailer
#
($myself = $q->self_url) =~ s/\?.*$//;
$myself =~ s/.*\///;
$myself =~ s/\.cgi/_cgi/;
print "You can view the ";
print $q->a({-href => "/chongo/tech/comp/cgi/".$myself.".txt"},
	    'source code'), "\n";
print " to this program.\n";
print $q->hr, "\n";
print $q->end_html, "\n";

# All done!! -- Jessica Noll (Age: 2)
#
exit(0);

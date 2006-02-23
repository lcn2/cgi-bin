#!/usr/bin/perl -wT
#
# cookie.cgi - get and set cookies
#
# NOTE: We added newlines to each CGI print statement to make the HTML output
#	a little easier for humans to read.  These \n's are not required.
#
# @(#) $Revision: 1.5 $
# @(#) $Id: cookie.cgi,v 1.5 2006/02/22 02:54:38 chongo Exp chongo $
# @(#) $Source: /web/isthe/chroot/cgi-bin/RCS/cookie.cgi,v $
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
use HTML::Entities;	# prevent cross site scripting
sub xss($);		# prevent cross site scripting
use CGI::Cookie;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser set_message);
set_message("This error came from a CGI program");
use strict;

# For DOS (Denial Of Service) protection prevent file uploads and
# really big "POSTS"
#
$CGI::POST_MAX = 8192;		# max post size
$CGI::DISABLE_UPLOADS = 1;	# no uploads

# my vars
#
my $q;		# our CGI object
my $myself;	# the URL of this CGI script
my $mybaseself;	# the basename of the URL of this CGI script
my %early_cookies;	# collection of cookies received by the browser
my %cookies;		# collection of cookies sent to the browser
my $cookie_set;	# collection of all cookies
my $cookie;	# individual cookie

# setup
#
$q = new CGI;
# prevent cross site scripting
$myself = xss($q->self_url);
if (defined $myself) {
    set_message("This error came from $myself");
}
if (cgi_error()) {
    if (defined cgi_error()) {
	croak("Your browser sent bad or too much data!\n" .
	      "Error: " . cgi_error() . "\n");
    } else {
	croak("Your browser sent bad or too much data!\n" .
	      "no cgi_error value returned\n");
    }
    exit(1);	# paranoia
}

# fetch all of the cookies given to us by the browser
#
%early_cookies = fetch CGI::Cookie;
%cookies = fetch CGI::Cookie;

# form the new cookie (or old cookie with submitted values)
#
if (defined $q->param('name') && defined $q->param('value')) {

    # form a brand new cookie based on the current fields
    #
    $cookie = new CGI::Cookie(-name => xss($q->param('name')),
    			       -value => xss($q->param('value')));
    $cookie->domain(xss($q->param('domain'))) if defined $q->param('domain');
    $cookie->path(xss($q->param('path'))) if defined $q->param('path');

    # add/change the cookie set with the new cookie
    #
    $cookies{$q->param('name')} = $cookie;
}

# build up a string containing all of the cookies
#
$cookie_set = "";
foreach (keys %cookies) {
    $cookie_set .= ";" if (length($cookie_set) > 0);
    $cookie_set .= $cookies{$_}->as_string;
}
# prevent cross site scripting
$cookie_set = xss($cookie_set);

# start off HTML header output
#
if (length($cookie_set) > 0) {
    print $q->header(-cookie => $cookie_set), "\n";
} else {
    print $q->header(), "\n";
}
warningsToBrowser(1);
print $q->start_html(-title => 'Cookie Example',
		     -bgcolor => '#98B8D8'), "\n";
print $q->h1('HTTP Cookies'), "\n";

# print the cookies we initial received by the browser before submit
#
print $q->h2('Your browser sent our server these cookies');
foreach (keys %early_cookies) {
    # prevent cross site scripting
    print xss($early_cookies{$_}->as_string);
    print $q->br, "\n";
}
print $q->hr, "\n";

# print the HTML form
#
print $q->h2('Set the cookie parameters and press Submit');
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
# NOTE: We will ignore the secure cookie issue for now
#
print $q->p, "\n";
print $q->submit(-name => 'Submit'), "\n";
print $q->end_form, "\n";
print $q->hr, "\n";

# print the cookies we will send
#
print $q->h2('Cookies sent to your browser after Submit is pressed');
foreach (keys %cookies) {
    # prevent cross site scripting
    print xss($cookies{$_}->as_string);
    print $q->br, "\n";
}
print $q->hr, "\n";

# print the cookie header
#
print $q->h2('HTTP Set-Cookie header sent to your browser after ' .
	     'Submit is pressed'), "\n";
if (length($cookie_set) > 0) {
    print $q->pre("Set-Cookie: $cookie_set"), "\n";
} else {
    print "No Set-Cookie header was sent\n";
}
print $q->hr, "\n";

# our standard trailer
#
($mybaseself = $myself) =~ s/\?.*$//;
$mybaseself =~ s/.*\///;
$mybaseself =~ s/\.cgi/_cgi/;
print "You can view the ";
print $q->a({-href => "/chongo/tech/comp/cgi/".$mybaseself.".txt"},
	    'source code'), "\n";
print " to this program.\n";
print $q->p, "\n";
print "Other ",
      $q->a({-href => "/chongo/tech/comp/cgi/cgidemo.html"},
            "cgi demos"), ".\n";
print $q->hr, "\n";
print $q->end_html, "\n";

# All done!! -- Jessica Noll (Age: 2)
#
exit(0);


# xss - remove or encode cross site scripting chars and non-printable chars
#
# given:
#	$string		string to strip and encode or undef
#
# returns:
#	a safer string or undef
#
sub xss($)
{
    my $string = $_[0];		# get arg

    # firewall - undef returns undef
    #
    if (! defined $string) {
	return undef;
    }

    # paranoia - remove % & to avoid substitution recursion
    #
    $string =~ s/[%&]+//g;

    # encode anything else unsafe
    #
    $string = HTML::Entities::encode($string, "\000-\037\%\&\<\>\"\177-\377");

    # return the safe string
    #
    return $string;
}

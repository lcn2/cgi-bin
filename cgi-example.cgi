#!/usr/bin/perl -wT
#
# cgi-example.cgi - Example #1 of a CGI perl script
#
# This CGI script that creates a fill-out form and echoes back its values.
#
# NOTE: We added newlines to each CGI print statement to make the HTML output
#	a little easier for humans to read.  These \n's are not required.
#
# @(#) $Revision: 1.14 $
# @(#) $Id: cgi-example.cgi,v 1.14 2005/05/09 17:28:59 chongo Exp chongo $
# @(#) $Source: /web/isthe/chroot/cgi-bin/RCS/cgi-example.cgi,v $
#
# Copyright (c) 1998-2002 by Landon Curt Noll.  All Rights Reserved.
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
use strict;

# For DOS (Denial Of Service) protection prevent file uploads and
# really big "POSTS"
#
$CGI::POST_MAX = 4096;		# max post size
$CGI::DISABLE_UPLOADS = 1;	# no uploads

# my vars
#
my $q;		# our CGI object
my $myself;	# this URL
my $override=0;	# 1 ==> override current value to use defaults

# setup
#
$q = new CGI;
if (cgi_error()) {
    print "Content-type: text/plain\n\n";
    print "Your browser sent bad or too much data!\n";
    print "Error: ", cgi_error(), "\n";
    exit(1);
}

# determine the override value
#
if ($q->param() && defined($q->param('override'))) {
    # prevent cross site scripting
    $override = xss($q->param('override'));
}

# start off HTML header output
#
print $q->header, "\n";
print $q->start_html(-title => 'CGI Example #1',
		     -bgcolor => '#98B8D8'), "\n";
print $q->h1('CGI Example #1'), "\n";

# print the HTML form
#
print $q->start_form(-method => 'POST'), "\n";
print "What's your name? ", "\n";
print $q->textfield(-name => 'yourname',
		    -default => 'Your name here',
		    -override => $override), "\n";
print $q->p, "\n";
print "What's the combination? ", "\n";
print $q->checkbox_group(-name => 'words',
			 -values => ['eenie','meenie','minie','moe'],
			 -defaults => ['eenie','minie'],
			 -override => $override), "\n";
print $q->p, "\n";
print "What's your favorite color? ", "\n";
print $q->popup_menu(-name => 'color',
		     -values => ['green','red','blue','chartreuse'],
		     -override => $override), "\n";
print $q->p, "\n";
print "Use coconuts: ", "\n";
print $q->checkbox(-name => 'coconut',
		   -checked => '',
		   -value => 'true',
		   -label => ' <== Coconut checkbox',
		   -override => $override), "\n";
print $q->p, "\n";
print $q->submit(-name => 'Submit'), "\n";
print " ", "\n";
print $q->reset(-name => 'Reset to last values'), "\n";
print $q->end_form, "\n";
print $q->start_form, "\n";
print $q->hidden(-name => 'override',
		 -default => '1',
		 -override => 1), "\n";
print $q->submit(-name => 'Restore defaults'), "\n";
print $q->end_form, "\n";
print $q->hr, "\n";

# post the reply
#
if ($q->param() && !defined($q->param('override'))) {
    print $q->p, "\n";
    print "Your name is: ", "\n";
    # prevent cross site scripting
    print $q->b(xss($q->param('yourname'))), "\n";
    print $q->p, "\n";
    print "The keywords are: ", "\n";
    # prevent cross site scripting
    print $q->em(xss(join(", ", $q->param('words')))), "\n";
    print $q->p, "\n";
    print "Your favorite color is: ", "\n";
    # prevent cross site scripting
    print $q->tt(xss(param('color'))), "\n";
    print $q->p, "\n";
    print "The coconut value (if any) is: ", "\n";
    print $q->b('{'), "\n";
    # prevent cross site scripting
    print xss($q->param('coconut')), "\n";
    print $q->b('}'), "\n";
    print $q->p, "\n";
    print $q->hr, "\n";
}

# our standard trailer
#
# prevent cross site scripting
($myself = xss($q->self_url)) =~ s/\?.*$//;
$myself =~ s/.*\///;
$myself =~ s/\.cgi/_cgi/;
print "You can view the ";
print $q->a({-href => "/chongo/tech/comp/cgi/".$myself.".txt"},
	    'source code'), "\n";
print " to this program.\n";
print $q->hr, "\n";
print $q->end_html, "\n";

# All done!!! - Jessica Noll, Age 2
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

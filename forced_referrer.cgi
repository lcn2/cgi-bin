#!/usr/bin/perl -wT
#
# forced_referer.cgi - Example of forcing a referring URL to contain a string
#
# Copyright (c) 1999 by Landon Curt Noll.  All Rights Reserved.
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
# Comments, suggestions, bug fixes and questions about these routines
# are welcome.  Send EMail to the address given below.
#
# Happy bit twiddling,
#
#                       Landon Curt Noll
#
#                       {chongo,noll}@{toad,sgi}.com
#                       http://reality.sgi.com/chongo
#
# chongo was here       /\../\
#

# requirements
#
use CGI qw(:standard);
use strict;

# my vars
#
my $q;          # our CGI object
my $myself;     # this URL

# URL info
#
# The HTTP_REFERER must contain with $referer_url or we will
# ask them to visit $bounce_url first.
#
my $referer_url = "/chongo/misc/comp/refer/";
my $bounce_url = "/chongo/misc/comp/refer/index.html";
my $timeout = 6;

# setup
#
$q = new CGI;
$q->use_named_parameters(1);

# If we did not come from the right URL, bounce them back
# to where they should have come from in the first place.
#
if (!defined($ENV{'HTTP_REFERER'})) {
    $ENV{'HTTP_REFERER'} = ' << NO HTTP_REFERER FOUND >> ';
}
if ($ENV{'HTTP_REFERER'} !~ /\Q$referer_url\E/) {
    print $q->header('Refresh' => "$timeout; url=$bounce_url"),
	$q->start_html( 'title' => 'Forced Referer demo',
			'bgcolor' => '000000',
			'link' => '#FF0000',
			'vlink' => '#FFF000',
			'text' => '#FFFFFF'),
	$q->h2('Access Denyed'),
	"\nSorry, you may only access the\n",
	$q->a({'href' => $q->self_url}, 'forced referer demo'),
	"\nvia the URLs that contain the string:\n",
	$q->blockquote($q->b($referer_url)),
	"\nsuch as CGI demo page:\n",
	$q->blockquote($q->b($q->a({'href' => $bounce_url},
				   'forced referer demo'))),
	"\nYour previous URL:\n",
	$q->blockquote($q->b($q->a({'href' => $ENV{'HTTP_REFERER'}},
				   $ENV{'HTTP_REFERER'}))),
	"\ndid not contain that string.\n",
	$q->p,
	"\nIn $timeout seconds, you will be moved to the ",
	$q->b($q->a({'href' => $bounce_url}, 'forced referer demo')),
	"\npage or you may click on that link to go there now.\n",
	$q->p,
	"\nFYI: The\n",
	$q->a({'href' => $q->self_url . ".txt"}, 'this CGI script'),
	"\nis available.\n",
	$q->p,
	$q->end_html;
     exit(1);
}

# The HTTP_REFERER is good, so tell them they are successful.
#
print $q->header,
    $q->start_html('title' => 'Forced Referer demo',
		   'bgcolor' => '000000',
		   'link' => '#FF0000',
		   'vlink' => '#FFF000',
		   'text' => '#FFFFFF'),
    $q->h2('Success'),
    "\nBecause your previous URL:\n",
    $q->blockquote($q->a({'href' => $ENV{'HTTP_REFERER'}},
		         $ENV{'HTTP_REFERER'})),
    "\ncontained the string:\n",
    $q->blockquote($q->b($referer_url)),
    "\nand so you were allowed access to\n",
    $q->a({'href' => $q->self_url}, 'this URL'),
    ".\n",
    $q->p,
    "\nFYI: The\n",
    $q->a({'href' => $q->self_url . ".txt"}, 'this CGI script'),
    "\nis available.\n",
    $q->p,
    $q->end_html;
exit(0);

#!/usr/bin/perl -wT
#
# cgi-example2.cgi - Example of a CGI perl script done objected oriented style
#
# This CGI script that creates a fill-out form and echoes back its values.
#
# NOTE: We added newlines to each CGI print statement to make the HTML output
#	a little easier for humans to read.  These \n's are not required.
#
# @(#) $Revision$
# @(#) $Id$
# @(#) $Source$
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
use strict;

# For DOS (Denial Of Service) protection prevent file uploads and
# really big "POSTS"
#
$CGI::POST_MAX = 1024;		# max post size
$CGI::DISABLE_UPLOADS = 1;	# no uploads

# my vars
#
my $q;			# our CGI object
my $name;		# name of a parameter
my $myself;		# this URL

# set param defaults
#
my @parname = qw(
    yourname words color
);
my %pardef = (
    'yourname'	=> 'here',
    'words'	=> ['eenie','minie'],
    'color'	=> ''
);

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
print $q->start_html(-title => 'CGI Example #2',
		     -bgcolor => '#98B8D8');
print $q->h1('CGI Example #2');

# determine which action we will take
#
# The action is dependent on the action parameter:
#
#    not set	- print form with defaults
#    'default'  - print form with defaults
#    'preview'  - print values from form
#    'edit'	- print form with user modified values
#    'submit'	- receive values and ack the submission
#
my $action = 'default';
if (defined($q->param('do_default'))) {
    $action = 'default';
} elsif (defined($q->param('do_preview'))) {
    $action = 'preview';
} elsif (defined($q->param('do_edit'))) {
    $action = 'edit';
} elsif (defined($q->param('do_submit'))) {
    $action = 'submit';
}

# determine which parameter defaults have been changed by the user
#
if ($q->param() && $action ne 'default') {
    foreach $name ( @parname ) {
	if (defined($q->param($name))) {
	    $pardef{$name} = $q->param($name);
	}
    }
}

# print the HTML form for default or edit purposes
#
# The next state for 'default' or 'edit' is to go into 'preview'.
#
if ($action eq 'default' || $action eq 'edit') {

    # print the HTML form for the user to play with
    #
    print $q->start_form, "\n";
    print "What's your name? ", "\n";
    print $q->textfield(-name => 'yourname',
			-value => $pardef{'yourname'}), "\n";
    print $q->p, "\n";
    print "What's the combination? ", "\n";
    print $q->checkbox_group(-name => 'words',
			     -values => ['eenie','meenie','minie','moe'],
			     -defaults => $pardef{'words'}), "\n";
    print $q->p, "\n";
    print "What's your favorite color? ", "\n";
    print $q->popup_menu(-name => 'color',
			 -values => ['green','red','blue','chartreuse'],
			 -defaults => $pardef{'color'}), "\n";
    print $q->p, "\n";
    print $q->hidden(-name => 'do_preview',
		     -value => 'cgi-example2.cgi'), "\n";
    print $q->submit(-name => 'Preview'), "\n";
    print $q->end_form, "\n";
    print $q->start_form, "\n";
    print $q->submit(-name => 'Reset'), "\n";
    print $q->hidden(-name => 'do_default',
		     -value => 'cgi-example2.cgi'), "\n";
    print $q->end_form, "\n";
    print $q->hr, "\n";

# Allow the user to preview their results with an option to edit or submit
#
# The next state depends on user action: 'edit' or 'submit'.
#
} elsif ($action eq 'preview') {

    # preview the values
    #
    print $q->start_html(-name => 'Preview the values'), "\n";
    print $q->p, "\n";
    print $q->h2('Please review for correctness'), "\n";
    print $q->p, "\n";
    print "Your name is: ", $q->b($q->param('yourname')), "\n";
    print $q->p, "\n";
    print "The keywords are: ", $q->em(join(", ", $q->param('words'))), "\n";
    print $q->p, "\n";
    print "Your favorite color is: ", $q->tt(param('color')), "\n";
    print $q->p, "\n";
    print $q->hr, "\n";

    # give them a form to edit
    #
    print $q->start_form, "\n";
    print $q->hidden(-name => 'do_edit',
		     -value => 'cgi-example2.cgi'), "\n";
    foreach $name ( @parname ) {
	my $value = $q->param($name), "\n";
	if (defined $value) {
	    print $q->hidden(-name => $name,
	    		     -value => $value), "\n";
	}
    }
    print $q->submit(-name => 'Edit'), "\n";
    print $q->end_form, "\n";

    # give them a form to submit
    #
    print $q->start_form, "\n";
    print $q->hidden(-name => 'do_submit',
		     -value => 'cgi-example2.cgi'), "\n";
    foreach $name ( @parname ) {
	my $value = $q->param($name), "\n";
	if (defined $value) {
	    print $q->hidden(-name => $name,
	    		     -value => $value), "\n";
	}
    }
    print $q->submit(-name => 'Submit'), "\n";
    print $q->end_form, "\n";

# post the reply for the submit action
#
} else {
    print $q->start_html(-name => 'Thanks'), "\n";
    print $q->h2('Thank you for your submission'), "\n";
}

# our standard trailer
#
($myself = $q->self_url) =~ s/\?.*$//;
$myself =~ s/.*\///;
$myself =~ s/\.cgi/_cgi/;
print "You can view the ", "\n";
print $q->a({-href => "/chongo/tech/comp/cgi/".$myself.".txt"},
	    'source code'), "\n";
print " to this program.\n";
print $q->hr, "\n";
print $q->end_html, "\n";

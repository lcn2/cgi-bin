#!/usr/bin/perl -wT
#
# cgi-example.cgi - Example #1 of a CGI perl script
#
# This CGI script that creates a fill-out form and echoes back its values.

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
my $q;		# our CGI object
my $myself;	# this URL
my $h;		# HTML element
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
$q->use_named_parameters(1);

# determine the override value
#
if ($q->param() && defined($q->param('override'))) {
    $override = $q->param('override');
}

# print the HTML form
#
print $q->header;
print $q->start_html(-title => 'CGI Example #1',
		     -bgcolor => '#98B8D8');
print $q->h1('CGI Example #1');
print $q->start_form(-method => 'POST');
print "What's your name? ";
print $q->textfield(-name => 'yourname',
		    -default => 'Your name here',
		    -override => $override);
print $q->p;
print "What's the combination? ";
print $q->checkbox_group(-name => 'words',
			 -values => ['eenie','meenie','minie','moe'],
			 -defaults => ['eenie','minie'],
			 -override => $override);
print $q->p;
print "What's your favorite color? ";
print $q->popup_menu(-name => 'color',
		     -values => ['green','red','blue','chartreuse'],
		     -override => $override);
print $q->p;
print "Use coconuts: ";
print $q->checkbox(-name => 'coconut',
		   -checked => '',
		   -value => 'true',
		   -label => ' <== Coconut checkbox',
		   -override => $override);
print $q->p;
print $q->submit(-name => 'Submit');
print " ";
print $q->reset(-name => 'Reset to last values');
print $q->end_form;
print $q->start_form;
print $q->hidden(-name => 'override',
		 -default => '1',
		 -override => 1);
print $q->submit(-name => 'Restore defaults');
print $q->end_form;
print $q->hr;

# post the reply
#
if ($q->param() && !defined($q->param('override'))) {
    print $q->p,
    print "Your name is: ";
    print $q->b($q->param('yourname'));
    print $q->p;
    print "The keywords are: ";
    print $q->em(join(", ", $q->param('words')));
    print $q->p;
    print "Your favorite color is: ";
    print $q->tt(param('color'));
    print $q->p;
    print "The coconut value (if any) is: ";
    print $q->b('{');
    print $q->param('coconut');
    print $q->b('}');
    print $q->p;
    print $q->hr;
}

# our standard trailer
#
($myself = $q->self_url) =~ s/\?.*$//;
$myself =~ s/.*\///;
$myself =~ s/\.cgi/_cgi/;
print "You can view the ";
print $q->a({'href' => "/chongo/tech/comp/cgi/".$myself.".txt"}, 'source code');
print " to this program.\n";
print $q->hr, $q->end_html;

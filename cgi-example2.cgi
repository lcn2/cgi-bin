#!/usr/bin/perl -T
#!/usr/bin/perl -wT
#
# cgi-example2.cgi - Example of a CGI perl script done objected oriented style
#
# This CGI script that creates a fill-out form and echoes back its values.
#
# By: chongo <Landon Curt Noll> {noll,chongo}@{toad,sgi}.com

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
$q->use_named_parameters(1);

# start off HTML header output
#
print $q->header;

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
    print $q->start_html(-title => 'CGI Example #2',
		         -bgcolor => '#98B8D8');
    print $q->h1('CGI Example #2');
    print $q->start_form;
    print "What's your name? ";
    print $q->textfield(-name => 'yourname',
			-value => $pardef{'yourname'});
    print $q->p;
    print "What's the combination? ";
    print $q->checkbox_group(-name => 'words',
			     -values => ['eenie','meenie','minie','moe'],
			     -defaults => $pardef{'words'});
    print $q->p;
    print "What's your favorite color? ";
    print $q->popup_menu(-name => 'color',
			 -values => ['green','red','blue','chartreuse'],
			 -defaults => $pardef{'color'});
    print $q->p;
    print $q->hidden(-name => 'do_preview',
		     -value => 'cgi-example2.cgi');
    print $q->submit(-name => 'Preview');
    print $q->end_form;
    print $q->start_form;
    print $q->submit(-name => 'Reset');
    print $q->hidden(-name => 'do_default',
		     -value => 'cgi-example2.cgi');
    print $q->end_form;
    print $q->hr;

# Allow the user to preview their results with an option to edit or submit
#
# The next state depends on user action: 'edit' or 'submit'.
#
} elsif ($action eq 'preview') {

    # preview the values
    #
    print $q->start_html(-name => 'Preview the values');
    print $q->p;
    print $q->h2('Please review for correctness');
    print $q->p;
    print "Your name is: ", $q->b($q->param('yourname'));
    print $q->p;
    print "The keywords are: ", $q->em(join(", ", $q->param('words')));
    print $q->p;
    print "Your favorite color is: ", $q->tt(param('color'));
    print $q->p;
    print $q->hr;

    # give them a form to edit
    #
    print $q->start_form;
    print $q->hidden(-name => 'do_edit',
		     -value => 'cgi-example2.cgi');
    foreach $name ( @parname ) {
	my $value = $q->param($name);
	if (defined $value) {
	    print $q->hidden(-name => $name,
	    		     -value => $value);
	}
    }
    print $q->submit(-name => 'Edit');
    print $q->end_form;

    # give them a form to submit
    #
    print $q->start_form;
    print $q->hidden(-name => 'do_submit',
		     -value => 'cgi-example2.cgi');
    foreach $name ( @parname ) {
	my $value = $q->param($name);
	if (defined $value) {
	    print $q->hidden(-name => $name,
	    		     -value => $value);
	}
    }
    print $q->submit(-name => 'Submit');
    print $q->end_form;

# post the reply for the submit action
#
} else {
    print $q->start_html(-name => 'Thanks');
    print $q->h2('Thank you for your submission');
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

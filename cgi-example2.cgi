#!/usr/bin/perl -w
#
# cgi-example.cgi - Example of a CGI perl script done objected oriented style
#
# This CGI script that creates a fill-out form and echoes back its values.
#
# By: chongo <Landon Curt Noll> {noll,chongo}@{toad,sgi}.com

# requirements
#
use CGI qw(:standard);
use strict;

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
$^W = 0;
$q = new CGI;
$^W = 1;
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
    print
      $q->start_html('name' => 'Set your preferences'),
      $q->h1('A Simple Example'),
      $q->start_form,
      "What's your name? ",
      $q->textfield('name' => 'yourname',
		    'value' => $pardef{'yourname'}),
      $q->p,
      "What's the combination? ", 
      $q->checkbox_group('name' => 'words',
			 'values' => ['eenie','meenie','minie','moe'],
			 'defaults' => $pardef{'words'}), 
      $q->p,
      "What's your favorite color? ",
      $q->popup_menu('name' => 'color',
		     'values' => ['green','red','blue','chartreuse'],
		     'defaults' => $pardef{'color'}),
      $q->p,
      $q->hidden('name' => 'do_preview',
		 'value' => 'cgi-example2.cgi'),
      $q->submit('name' => 'Preview'),
      $q->end_form,
      $q->start_form,
      $q->submit('name' => 'Reset'),
      $q->hidden('name' => 'do_default',
		 'value' => 'cgi-example2.cgi'),
      $q->end_form,
      $q->hr;

# Allow the user to preview their results with an option to edit or submit
#
# The next state depends on user action: 'edit' or 'submit'.
#
} elsif ($action eq 'preview') {

    # preview the values 
    #
    print 
      $q->start_html('name' => 'Preview the values'),
      $q->p,
      $q->h2('Please review for correctness'),
      $q->p,
      "Your name is: ", $q->b($q->param('yourname')),
      $q->p,
      "The keywords are: ", $q->em(join(", ", $q->param('words'))),
      $q->p,
      "Your favorite color is: ", $q->tt(param('color')),
      $q->p,
      $q->hr;

    # give them a form to edit
    #
    print
      $q->start_form,
      $q->hidden('name' => 'do_edit',
		 'value' => 'cgi-example2.cgi');
    foreach $name ( @parname ) {
	my $value = $q->param($name);
	if (defined $value) {
	    print $q->hidden('name' => $name, 'value' => $value);
	}
    }
    print
      $q->submit('name' => 'Edit'),
      $q->end_form;

    # give them a form to submit
    #
    print
      $q->start_form,
      $q->hidden('name' => 'do_submit',
		 'value' => 'cgi-example2.cgi');
    foreach $name ( @parname ) {
	my $value = $q->param($name);
	if (defined $value) {
	    print $q->hidden('name' => $name, 'value' => $value);
	}
    }
    print
      $q->submit('name' => 'Submit'),
      $q->end_form;

# post the reply for the submit action
#
} else {
    print 
      $q->start_html('name' => 'Thanks'),
      $q->h2('Thank you for your submission');
}

# our stand trailer
#
$myself = $q->self_url;
print "The <A HREF='", $myself, ".cat'>source code</A> to this program.\n";
print $q->hr, $q->end_html;

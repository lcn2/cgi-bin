#!/usr/bin/perl -wT
#
# cgi-example.cgi - Example of a CGI perl script
#
# This CGI script that creates a fill-out form and echoes back its values.

# requirements
#
use CGI qw(:standard);
use strict;

# my vars
#
my $q;		# our CGI object
my $myself;	# this URL
my $h;		# HTML element
my $override=0;	# 1 ==> override current value to use defaults

# setup
#
$q = new CGI;
$q->use_named_parameters(1);

# determine the override value
#
if ($q->param() && defined($q->param('override'))) {
    $override = $q->param('override');
}

# print the HTML form
#
print $q->header,
      $q->start_html('title' => 'A Simple Example'),
      $q->h1('A Simple Example'),
      $q->start_form('method' => 'POST'),
      "What's your name? ",
      $q->textfield('name' => 'yourname',
		    'default' => 'Your name here',
		    'override' => $override),
      $q->p,
      "What's the combination? ",
      $q->checkbox_group('name' => 'words',
			 'values' => ['eenie','meenie','minie','moe'],
			 'defaults' => ['eenie','minie'],
			 'override' => $override),
      $q->p,
      "What's your favorite color? ",
      $q->popup_menu('name' => 'color',
		     'values' => ['green','red','blue','chartreuse'],
		     'override' => $override),
      $q->p,
      "Use coconuts: ",
      $q->checkbox('name' => 'coconut',
		   'checked' => '',
		   'value' => 'true',
		   'label' => ' <== Coconut checkbox',
		   'override' => $override),
      $q->p,
      $q->submit('name' => 'Submit'),
      " ",
      $q->reset('name' => 'Reset to last values'),
      $q->end_form,
      $q->start_form,
      $q->hidden('name' => 'override',
		 'default' => '1',
		 'override' => 1),
      $q->submit('name' => 'Restore defaults'),
      $q->end_form,
      $q->hr;

# post the reply
#
if ($q->param() && !defined($q->param('override'))) {
    print $q->p,
	  "Your name is: ",
	  $q->b($q->param('yourname')),
	  $q->p,
	  "The keywords are: ",
	  $q->em(join(", ", $q->param('words'))),
	  $q->p,
	  "Your favorite color is: ",
	  $q->tt(param('color')),
	  $q->p,
	  "The coconut value (if any) is: ",
	  $q->b('{'),
	  $q->param('coconut'),
	  $q->b('}'),
	  $q->p,
	  $q->hr;
}

# our stand trailer
#
($myself = $q->self_url) =~ s/\?.*$//;
$myself =~ s/.*\///;
$myself =~ s/\.cgi/_cgi/;
print "You can view the ",
    $q->a({'href' => "/chongo/tech/comp/cgi/".$myself.".txt"}, 'source code'),
    " to this program.\n";
print $q->hr, $q->end_html;

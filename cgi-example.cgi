#!/usr/bin/perl -w
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
my $q;	# our CGI object

# setup
#
$q = new CGI;
$q->use_named_parameters(1);

# print the HTML form
#
print $q->header,
      $q->start_html('A Simple Example'),
      $q->h1('A Simple Example'),
      $q->start_form,
      "What's your name? ",
      $q->textfield('name' => 'yourname',
		    'default' => 'Your name here'),
      $q->p,
      "What's the combination? ", 
      $q->checkbox_group('name' => 'words',
			 'values' => ['eenie','meenie','minie','moe'],
			 'defaults' => ['eenie','minie']), 
      $q->p,
      "What's your favorite color? ",
      $q->popup_menu('name' => 'color',
		     'values' => ['green','red','blue','chartreuse']),
      $q->p,
      $q->submit,
      $q->end_form,
      $q->hr;

# post the reply
#
if ($q->param()) {
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
	  $q->hr;
}

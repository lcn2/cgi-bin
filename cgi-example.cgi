#!/usr/bin/perl -w
#
# cgi-example.cgi - Example of a CGI perl script
#
# This CGI script that creates a fill-out form and echoes back its values.

# requirements
#
use CGI qw/:standard/;
use strict;

# print the HTML form
#
print header,
      start_html('A Simple Example'),
      h1('A Simple Example'),
      start_form,
      "What's your name? ",textfield('name'),p,
      "What's the combination?", p,
      checkbox_group('-name'=>'words',
		     '-values'=>['eenie','meenie','minie','moe'],
		     '-defaults'=>['eenie','minie']), p,
      "What's your favorite color? ",
      popup_menu('-name'=>'color',
		 '-values'=>['green','red','blue','chartreuse']),
      p,
      submit,
      end_form,
      hr;

# post the reply
#
if (param()) {
    print p,
	  "Your name is: ",em(param('name')),p,
	  "The keywords are: ",em(join(", ",param('words'))),p,
	  "Your favorite color is ",em(param('color')),
	  p,
	  hr;
}

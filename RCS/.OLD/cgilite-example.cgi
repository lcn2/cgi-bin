#!/usr/bin/perl -Tw
#
# cgilite-example.cgi - CGI_Lite usage example
#
# This example primes out the data keys from a form.
#
# From:
#	http://www.perl.com/CPAN-local/doc/FAQs/cgi/perl-cgi-faq.html

# modules used
#
use CGI_Lite;
use strict;

# my variables
#
my $cgi;	# CGI_Lite context
my @mine_types;	# MIME types discovered
my %form_data;	# form data returned by $cgi->parse_form_data
my @formval;	# individual elements of a form data item
my %cookies;	# cookie data returned by $cgi->parse_cookies
my $key;	# array element
my $i;		# array index

# unbuffer output so that we can see it as it comes 
# out, rather than waiting for buffers to flush
#
$| = 1;

# establish CGI_Lite context
#
$cgi = new CGI_Lite;

# assume a Un*x platform
#
$cgi->set_platform("Unix");

# prep for output
#
print "Content-type: text/plain", "\n\n";
print "This is the output from $0\n";
print "Values are printed as \<\<value\>\> or as (undef)\n\n";

# determine mime types
#
@mine_types = $cgi->get_mime_types;
#
print "=-=-=\t\$cgi->get_mime_types returned:\n";
foreach $key (@mine_types) {
    print "  ", $key, "\n";
}
print "-=-=-\tend of \$cgi->get_mime_types\n\n";

# parse form data
#
$^W = 0;	# avoid parse_form_data bogon warnings
%form_data = $cgi->parse_form_data;
$^W = 1;
if ($cgi->is_error) {
    print "WARNING: $cgi->parse_form_data error\n";
    print "Error message follows:\n$cgi->get_error_message\n";
}
#
print "=-=-=\t\$cgi->parse_form_data returned:\n";
foreach $key (keys %form_data) {

    # NOTE: We need to use the get_multiple_values method on each form value 
    #	    because some form data is returned as an array instead of as a
    #	    scalar.  The get_multiple_values method will return an array
    #	    of 1 element for scalar form values.
    #
    # NOTE: It is possible for some data to be undefined.  For example
    #	    the URL:
    #
    #		cgilite-example.cgi?query
    #
    #	    will cause the value $form_data{"query"} to be undefuned.
    #	    We must check of the value is undefined before we use it.
    #
    @formval = $cgi->get_multiple_values( $form_data{$key} );
    if ($#formval < 1) {
	if (defined($formval[0])) {
	    print "  $key = \<\<$formval[0]\>\>\n";
	    if (CGI_Lite::is_dangerous($formval[0])) {
		print "WARNING: $key contains dangerious data\n";
	    }
	} else {
	    print "  $key = (undef)\n";
	}
    } else {
	for ($i=0; $i <= $#formval; ++$i) {
	    if (defined($formval[$i])) {
		print "  $key\[$i\] = \<\<$formval[$i]\>\>\n";
		if (CGI_Lite::is_dangerous($formval[$i])) {
		    print "WARNING: $key\[$i\] contains dangerious data\n";
		}
	    } else {
		print "  $key\[$i\] = (undef)\n";
	    }
	}
    }
}
print "-=-=-\tend of \$cgi->parse_form_data\n\n";

# parse cookies
#
%cookies = $cgi->parse_cookies;
if ($cgi->is_error) {
    print "WARNING: $cgi->parse_cookies error\n";
    print "Error message follows:\n$cgi->get_error_message\n";
}
#
print "=-=-=\t\$cgi->parse_cookies returned:\n";
foreach $key (keys %cookies) {
    print "  $key = \<\<$cookies{$key}\>\>\n";
    if (CGI_Lite::is_dangerous($cookies{$key})) {
	print "WARNING: $key contains dangerious data\n";
    }
}
print "-=-=-\tend of \$cgi->parse_cookies\n\n";

exit (0);

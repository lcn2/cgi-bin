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

# establish CGI_Lite context
#
$cgi = new CGI_Lite;

# assume a Un*x platform
#
$cgi->set_platform("Unix");

# prep for output
#
print "Content-type: text/plain", "\n\n";
print "This is the output from $0\n\n";

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
%form_data = $cgi->parse_form_data;
if ($cgi->is_error) {
    print "WARNING: $cgi->parse_form_data error\n";
    print "Error message follows:\n$cgi->get_error_message\n";
}
#
print "=-=-=\t\$cgi->parse_form_data returned:\n";
foreach $key (keys %form_data) {
    @formval = $cgi->get_multiple_values( $form_data{$key} );
    if ($#formval < 1) {
	print "  $key = $formval[0]\n";
	if (CGI_Lite::is_dangerous($formval[0])) {
	    print "WARNING: $key contains dangerious data\n";
	}
    } else {
	for ($i=0; $i <= $#formval; ++$i) {
	    print "  $key\[$i\] = $formval[0]\n";
	    if (CGI_Lite::is_dangerous($formval[$i])) {
		print "WARNING: $key[$i] contains dangerious data\n";
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
    print "  ", $key, " = ", $cookies{$key}, "\n";
    if (CGI_Lite::is_dangerous($cookies{$key})) {
	print "WARNING: $key contains dangerious data\n";
    }
}
print "-=-=-\tend of \$cgi->parse_cookies\n\n";

exit (0);

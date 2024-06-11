#!/usr/bin/perl -wT
#
# cgi-example.cgi - Simple CGI Example #0
#
# If when you run this tool you see an error of the form:
#
#	Can't locate __something__ in @INC (you may need to install the __something__ module) ...
#	Undefined subroutine &__something__ called at ...
#
# Run, as root:
#
#	cpanm CGI::Tiny Text::Xslate Data::Section::Simple HTML::Entities
#
# or if you do not have the cpanm tool:
#
#	cpan CGI::Tiny Text::Xslate Data::Section::Simple HTML::Entities
#
# If needed, adjust the path from the line to be the directory under where the file,
# CGI/Tiny/Multipart.pm is found:
#
#	use lib "/usr/local/perl/perl5/lib/perl5";
#
# You may have to add this directive to your apache configuration:
#
#	<IfModule mod_env>
#
#	    # The directory where CGI/Tiny/Multipart.pm is found
#	    #
#	    SetEnv PERL5LIB /usr/local/perl/perl5/lib/perl5
#
#	</IfModule>
#
# Copyright (c) 2024 by Landon Curt Noll.  All Rights Reserved.
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
use strict;
use warnings;
use utf8;
#
# dir where perl modules such as CGI/Tiny/Multipart.pm are found
use lib "/usr/local/perl/perl5/lib/perl5";
#
use CGI::Tiny;
use Text::Xslate;
use Data::Section::Simple 'get_data_section';
use HTML::Entities 'encode_entities';


# CGI block
#
cgi {
    my $cgi = $_;	# our CGI object

    # set up error handling on $cgi
    #
    $cgi->set_error_handler(sub {
	my ($cgi, $error, $rendered) = @_;
	warn $error;

	unless ($rendered) {
	    if ($cgi->response_status_code == 413) {
		$cgi->render(json => {error => 'Request body limit exceeded'});
	    } elsif ($cgi->response_status_code == 400) {
		$cgi->render(json => {error => 'Bad request'});
	    } else {
		$cgi->render(json => {error => 'Internal server error'});
	    }
	}
    });

    # Construct page from __DATA__
    #
    my $tx = xss(Text::Xslate->new(path => [get_data_section]));

    # set response headers
    #
    my $h1 = xss("Simple CGI example");
    my $h2 = xss("Fizzbin ...");

    # render response with $cgi->render or $cgi->render_chunk
    #
    $cgi->render(html => $tx->render('webpage.tx', {h1 => $h1, h2 => $h2}));
};


# All Done!!! -- Jessica Noll, Age 2
#
exit(0);


# xss - remove or encode cross site scripting chars and non-printable chars
#
# given:
#       $string         string to strip and encode or undef
#
# returns:
#       a safer string or an empty string if string was undef
#
sub xss($)
{
    my $string = $_[0];         # get arg

    # firewall - undef returns undef
    #
    if (! defined $string) {
        return "";
    }

    # paranoia - remove % & to avoid substitution recursion
    #
    $string =~ s/[%&]+//g;

    # encode anything else unsafe
    #
    $string = encode_entities($string, "\000-\037\%\&\<\>\"\177-\377");

    # return the safe string
    #
    return $string;
}


__DATA__
@@ webpage.tx
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<html>

<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
<title>Simple CGI Example #0</title>
<meta name="description" content="Simple CGI Example #0">
<meta name="keywords" content="CGI, example">
</head>

<body bgcolor="#98B8D8">

<h1><: $h1 :></h1>
<h2><: $h2 :></h2>

You can view the <a href="/chongo/tech/comp/cgi/cgi-simple_cgi.txt">source code</a> to this program.

</body>
</html>

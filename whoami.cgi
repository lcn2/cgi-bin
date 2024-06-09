#!/usr/bin/perl -wT
#
# whoami.cgi - show what the browser sends to the server
#
# Copyright (c) 1997-2006,2013,2023 by Landon Curt Noll.  All Rights Reserved.
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
# chongo <was here> /\oo/\
#
# Share and enjoy!


# paranoia
#
delete $ENV{IFS};
delete $ENV{CDPATH};
delete $ENV{ENV};
delete $ENV{BASH_ENV};
$SIG{ALRM} = sub { die "timeout on stdin\n"; };


# setup
#
use HTML::Entities;	# prevent cross site scripting
sub xss($);		# prevent cross site scripting
use strict;
use Cwd;
use English;
select(STDOUT);
$| = 1;


# my vars
#
my $line;		# stdin line buffer
my $linelen;		# total stdin length
my $maxline = 8192;	# maximum amount of stdin we want to process
my @CGI_ENV = (
    "SERVER_SOFTWARE", "SERVER_NAME", "GATEWAY_INTERFACE",
    "SERVER_PROTOCOL", "SERVER_PORT", "REQUEST_METHOD", "SERVER_URL",
    "SERVER_ADDR", "REQUEST_URI",
    "PATH_INFO", "PATH_TRANSLATED", "SCRIPT_NAME", "QUERY_STRING",
    "REMOTE_HOST", "REMOTE_ADDR", "AUTH_TYPE", "REMOTE_USER",
    "REMOTE_IDENT", "CONTENT_TYPE", "CONTENT_LENGTH", "HTTPS"
);
my $utcnow = gmtime();
my $dev;		# device number of .
my $ino;		# inode number of .
my $cwd;		# current working directory path
my $pid = $PID;		# our process ID
my $ppid = getppid();	# our parent's process ID
my $uid = $UID;		# our user ID
my $gid = $GID;		# our group ID
my $euid = $EUID;	# our effective user ID
my $egid = $EGID;	# our effective group ID


# we must first send our MIME type
# we must next send a URL for another document, or an empty line
#
print "Content-type: text/plain\n\n";


# the text/plain data starts here
#
print "Chongo\'s whoami.cgi script. ";

# print URL for more info
#
print "For more information see:\n\n";
print "\thttp://www.isthe.com/chongo/tech/comp/cgi/whoami.html\n\n";

# print IP address
#
print "Your IP address appears to be: ";
if (defined $ENV{'REMOTE_ADDR'}) {
    print xss($ENV{'REMOTE_ADDR'});
} else {
    print "unknown";
}
print " port ";
if (defined $ENV{'REMOTE_PORT'}) {
    print xss($ENV{'REMOTE_PORT'}), "\n\n";
} else {
    print "unknown\n\n";
}

# print Process execution information
#
print "Process execution:\n\n";
print "prog: $0\n";
print "argc: ", $#ARGV+1, "\n";
print "argv:";
foreach my $arg (@ARGV) {
    print ' "', xss($arg), '"';
}
print "\n";
$cwd = getcwd();
print "current working dir: $cwd\n";
($dev,$ino) = stat(".");
print "current working dir dev/inode: ( $dev,$ino ) \n";
print "pid: $pid\n";
print "ppid: $ppid\n";
print "uid: $uid\n";
print "gid: $gid\n";
print "euid: $euid\n";
print "egid: $egid\n";
print "Seconds since the Epoch: $BASETIME\n";
print "UTC time: $utcnow\n";
print "\n";


# CGI environment variables
#
print "CGI environment variables:\n\n";
foreach my $key (sort @CGI_ENV) {
    print "$key=", xss($ENV{$key}), "\n" if defined $ENV{$key};
}
print "\n";


# HTTP environment variables
#
print "HTTP environment variables:\n\n";
foreach my $key ( sort keys %ENV ) {
    print "$key=", xss($ENV{$key}), "\n" if $key =~ "^[Hh][Tt][Tt][Pp]_";
}
print "\n";


# other environment variables
#
print "Other environment variables:\n\n";
OTHER:
foreach my $key (sort keys %ENV) {
    next OTHER if $key =~ "^[Hh][Tt][Tt][Pp]_";
    foreach my $env (@CGI_ENV) {
	next OTHER if $key =~ /^$env$/i;
    }
    print "$key=", xss($ENV{$key}), "\n";
}


# Process data on standard input - for a limited amount of time
#
print "\nData on standard input:\n\n";
alarm(5);
$linelen = 0;
$line = <STDIN>;
if (defined($line)) {
    print "***begin stdin***\n";
    $linelen += length($line);
    $line =~ s/&/\n/g;
    print xss($line);
    while ($linelen < $maxline && defined($line = <STDIN>)) {
	$linelen += length($line);
	$line =~ s/&/\n/g;
	print xss($line);
    }
    print "\n***end stdin***\n";
} else {
    print "---nothing found on stdin---\n";
}

# All done!! -- Jessica Noll (Age: 2)
#
exit(0);


# xss - remove or encode cross site scripting chars and non-printable chars
#
# given:
#	$string		string to strip and encode or undef
#
# returns:
#	a safer string or an empty string if string was undef
#
sub xss($)
{
    my $string = $_[0];		# get arg

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
    $string = HTML::Entities::encode($string, "\000-\037\%\&\<\>\"\177-\377");

    # return the safe string
    #
    return $string;
}

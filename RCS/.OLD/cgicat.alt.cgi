#!/usr/bin/perl -wT
# @(#)cgicat	1.1 10 Oct 1995 03:23:08
#
# cgicat.alt.cgi - cat a cgi-bin script in html form from the .alt file
#
# usage:
#	cat.filename.cgi
#
#	Cat the file filename.cgi.alt so that the reader does not interpret
#	the usual html magic characters.

# setup
#
use strict;
#select(STDOUT);
$| = 1;

# my vars
#
my $argv0;
my $line;

# obtain the basename of the arg without any .cat
# for backward compat, we also strip off .txt
#
$argv0 = $0;
$argv0 =~ s/^.*\///o;
$argv0 =~ s/^cat\.//o;
if ($argv0 =~ /^([-\@\w.]+)$/) {
    $argv0 = $1;
} else {
    die "Bad data in arg 0\n";
}

# open the base file
#
open(CGIFILE, "<cgi-bin/$argv0.alt") || die "cannot open $argv0.alt\n";

# special code to explain how to use cgicat
#
# This section is only invoked if we are executed as cgicat.cat
#
if ($argv0 =~ /cgicat/) {

    # we are being executed as cgicat.cat, display info about cgicat.cat
    #
    print <<HTML_INFO1;
content-type: text/html

<HTML>
<HEAD>
<TITLE> How to use cgicat </TITLE>
</HEAD>

<BODY BGCOLOR="#80A0C0">
<H1> How to use cgicat </H1>

<HR>

The <B>cgicat.cgi</B> cgi script allows one to view the source of
a selected cgi-bin script.

<P></P>

Say you want to be able to view the file <B>whoami.cgi</B>.<BR>
If the cgi-bin file <B>whoami.cgi.cat</B> is a link to <B>cgicat.cgi</B>
then invocation of the URL:

<BLOCKQUOTE>
<A HREF="/cgi-bin/whoami.cgi.cat">/cgi-bin/whoami.cgi.cat</A>
</BLOCKQUOTE>

will display the contents of:

<BLOCKQUOTE>
<A HREF="/cgi-bin/whoami.cgi">/cgi-bin/whoami.cgi</A>
</BLOCKQUOTE>

<HR>

The following are some cgi-bin scripts that you can view:

<P></P>

<UL>
<LI><A HREF="/cgi-bin/html.cgi.cat">html.cgi</A> 
(an example of an CGI returning HTML)<BR>
<LI><A HREF="/cgi-bin/whoami.cgi.cat">whoami.cgi</A> 
(determine what a Browser tells a server)<BR>
<LI><A HREF="/cgi-bin/versions-b.cgi.cat">versions-b.cgi</A> 
(display versions -b output)<BR>
<LI><A HREF="/cgi-bin/showprods-3EFn.cgi.cat">showprods-3EFn.cgi</A> 
(display showprods -3EFn output)<BR>
<LI><A HREF="/cgi-bin/MachineInfo.cgi.cat">MachineInfo.cgi</A> 
(display hinv output in table form)<BR>
<LI><A HREF="/cgi-bin/sample.cgi.cat">sample.cgi</A> 
(allows access to chongo's sample directory)
</UL>

and here is where you can run them:

<P></P>

<UL>
<LI><A HREF="/cgi-bin/html.cgi">html.cgi</A> 
(an example of an CGI returning HTML)<BR>
<LI><A HREF="/cgi-bin/whoami.cgi">whoami.cgi</A> 
(determine what a Browser tells a server)<BR>
<LI><A HREF="/cgi-bin/versions-b.cgi">versions-b.cgi</A> 
(display versions -b output)<BR>
<LI><A HREF="/cgi-bin/showprods-3EFn.cgi">showprods-3EFn.cgi</A> 
(display showprods -3EFn output)<BR>
<LI><A HREF="/cgi-bin/MachineInfo.cgi">MachineInfo.cgi</A> 
(display hinv output in table form)<BR>
<LI><A HREF="/cgi-bin/sample.cgi">sample.cgi</A> 
(allows access to chongo's sample directory)
</UL>

<HR>

This html document that you are <I>now</I>
viewing was produced by <B>cgicat.cgi</B>.  
The source to <B>cgicat.cgi</B> is as follows:

<P></P>

<CODE>
<PRE>
HTML_INFO1

    # display the source to cgicat
    #
    while (defined($line = <CGIFILE>)) {
	$line =~ s/&/&amp;/og;
	$line =~ s/</&lt;/og;
	$line =~ s/>/&gt;/og;
	$line =~ s/\"/&quot;/og;
	print $line;
    }

    # display the remainder of the info
    #
    print <<HTML_INFO2;
</PRE>
</CODE>

<HR>

<H3>Author:</H3>
<BLOCKQUOTE>
<A HREF="/chongo/index.html">chongo</A>
&lt; Landon Curt Noll &gt;
<STRONG>/\\oo/\\</STRONG>
</BLOCKQUOTE>

</BODY>
</HTML>
HTML_INFO2

    # all done with displaying information
    #
    exit(0);
}

# html header goodies
#
print <<HTML_INFO3;
content-type: text/html

<HTML>
<HEAD>
<TITLE> $argv0 source listing </TITLE>
</HEAD>

<BODY BGCOLOR="#80A0C0">
<H1> <A HREF="/cgi-bin/$argv0">/cgi-bin/$argv0</A>
source listing
</H1>

<HR>

<CODE>
<PRE>
HTML_INFO3

# display the source to cgicat
#
while (defined($line = <CGIFILE>)) {
    $line =~ s/&/&amp;/og;
    $line =~ s/</&lt;/og;
    $line =~ s/>/&gt;/og;
    $line =~ s/\"/&quot;/og;
    print $line;
}

# final html
#
print <<HTML_INFO4;
</PRE>
</CODE>

<HR>

<H3>Author:</H3>
<BLOCKQUOTE>
<A HREF="/chongo/index.html">chongo</A>
&lt; Landon Curt Noll &gt;
<STRONG>/\\oo/\\</STRONG>
</BLOCKQUOTE>

</BODY>
</HTML>
HTML_INFO4

# all done
#
exit(0);

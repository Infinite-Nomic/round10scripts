#!/usr/bin/env perl

use strict;
use warnings;

use Digest::SHA qw/sha256_hex/;

use constant {
    MODE_REPEATED => 1,
    MODE_MATCH => 2,
    MODE_TOTAL => 3,
    MODE_SEQ => 4,
};

my $mode = MODE_REPEATED;
my $modearg;

if (@ARGV >= 2) {
    my $m = shift @ARGV;

    if ($m eq '-r') {
        $mode = MODE_REPEATED;
        $modearg = shift @ARGV if (@ARGV >= 2);
    } elsif ($m eq '-rlet') {
        $mode = MODE_REPEATED;
        $modearg = "[[:alpha:]]";
    } elsif ($m eq '-rnum') {
        $mode = MODE_REPEATED;
        $modearg = "[0-9]";
    } elsif ($m eq '-match') {
        $mode = MODE_MATCH;
        $modearg = shift @ARGV;
    } elsif ($m eq '-t') {
        $mode = MODE_TOTAL;
        $modearg = shift @ARGV;
    } elsif ($m eq '-tlet') {
        $mode = MODE_TOTAL;
        $modearg = "[[:alpha:]]";
    } elsif ($m eq '-tnum') {
        $mode = MODE_TOTAL;
        $modearg = "[0-9]";
    } elsif ($m eq '-s') {
        $mode = MODE_SEQ;
        $modearg = shift @ARGV;
    } elsif ($m eq '-slet') {
        $mode = MODE_SEQ;
        $modearg = "[[:alpha:]]";
    } elsif ($m eq '-snum') {
        $mode = MODE_SEQ;
        $modearg = "[0-9]";
    } else {
        die "no such mode"
    }
}

my $template;

my $in = shift @ARGV or die "expected text";

{
    open my $temph, "<", "files/hmtemplate.txt" or die "can't load template";
    local $/;
    $template = <$temph>;
    $template =~ s/(.+)\s$/$1/;
    $template =~ s/{text}/$in/;
    close $temph;
}

my $numtobeat = 0;

my $blen = 0;

sub base95 ($) {
    my $in = shift;

    my $out = "";

    while ($in) {
        my $rem = $in % 95;
        $out .= chr $rem + 32;
        $in -= $rem;
        $in /= 95;
    }

    $out
}

open my $outh, ">", "files/hmout.txt" or die "cannot open out file";

for (my $idx = 0;; $idx++) {
    my $salt = base95 $idx;
    my $in2 = $template =~ s/{salt}/$salt/r;
    my $digest = sha256_hex $in2;

    my $lastchar;
    my $sslen = 0;

    if ($mode == MODE_MATCH) {
        if ($digest =~ /$modearg/) {
            print "$numtobeat: $digest ($idx)\n$in2\n";
        } 
        next;
    }

    if ($mode == MODE_TOTAL) {
        for (split //, $digest) {
            $sslen++ if ($_ =~ /$modearg/);
        }

        if ($sslen >= $blen) {
            $blen = $sslen;
            $numtobeat = $blen if ($blen > $numtobeat);

            print "$numtobeat: $digest ($idx)\n$in2\n";
        }

        next;
    }

    for (split //, $digest) {
        if (defined $lastchar &&
            ($mode == MODE_REPEATED &&
             (($modearg && $_ =~ $modearg) || $lastchar eq $_) ||
            ($mode == MODE_SEQ &&
              ($_ =~ /$modearg/ && $_ eq chr(ord($lastchar)+1))))) {
            $sslen++;
        } else {
            $sslen = 1;
        }

        if ($sslen >= $blen) {
            $blen = $sslen;
            $numtobeat = $blen if ($blen > $numtobeat);
            
            print "$numtobeat: $digest ($idx)\n$in2\n";
        }

        $lastchar = $_;
    }
}

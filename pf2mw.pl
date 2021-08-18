#!/usr/bin/env perl

# a perl script to turn the Poker Face bot's output into a MediaWiki-formatted lot table.

use warnings;
use strict;

use POSIX qw/printf/;

my %suits = (
    1 => 'L',
    2 => 'D',
    3 => 'Cp',
    4 => 'C',
    5 => 'A',
    6 => 'R',
    7 => 'B',
    8 => 'Sw',
    9 => 'Sh',
    10 => 'H',
    11 => 'Cn',
    12 => 'S'
);

my %ranks = (
    1 => 'A',
    2 => '2',
    3 => '3',
    4 => '4',
    5 => '5',
    6 => '6',
    7 => '7',
    8 => '8',
    9 => '9',
    10 => 'T',
    11 => 'E',
    12 => 'D',
    13 => 'H',
    14 => 'U',
    15 => 'O',
    16 => 'N',
    17 => 'B',
    18 => 'R',
    19 => 'Q',
    20 => 'K',
);

my $pairmatch = '\[\s*(?<a#>\d+?)\]\s*\[\s*(?<b#>\d+?)\]';
my $linum = 1;

while (<>) {
    my $regex = '';
    
    for (my $i = 1;; $i++) {
        my $newregex = $regex . $pairmatch =~ s/#/$i/rg . '\s*';
        if ($_ =~ /$newregex/) {
            $regex = $newregex;
        } else {
            last;
        }
    }

    if ($_ =~ /$regex/) {
        printf '|Lot %02d || ', $linum++;
        for (my $i = 1;; $i++) {
            my ($a, $b) = ($+{'a' . $i}, $+{'b' . $i});
            last if (not defined $a or not defined $b);
            print "{{Card|" . $ranks{$a} . "|" . $suits{$b} . "}} ";
        }
    }

    print "\n|-\n";
}

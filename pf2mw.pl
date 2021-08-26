#!/usr/bin/env -S perl -I.

# a perl script to turn the Poker Face bot's output into a MediaWiki-formatted lot table.

use warnings;
use strict;

use InfiniteNomic qw/@suitorder @rankorder/;

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
            print "{{Card|" . $rankorder[$a-1] . "|" . $suitorder[$b-1] . "}} ";
        }
    }

    print "\n|-\n";
}

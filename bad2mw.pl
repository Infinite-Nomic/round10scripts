#!/usr/bin/env -S perl -I.

use strict;
use warnings;

use InfiniteNomic qw/@suitorder @rankorder/;

my @suits = split /,\s+/, <>;
my @tarotranks = split /,\s+/, <>;
my @normalranks = split /,\s+/, <>;

my $CPL = 3;

while (my ($sidx, $suit) = each @suits) {
    my ($ridx, $rank);

    printf "\n|-\n|Lot %02d || ", $sidx / $CPL + 1 if ($sidx % $CPL == 0);

    if ($suit > 12) {
        ($ridx, $rank) = each @tarotranks;
        $rank =~ s/(.+)\s+/$1/;
        print "{{Tarot|$rank}} ";
    } else {
        ($ridx, $rank) = each @normalranks;
        print "{{Card|$rankorder[$rank-1]|$suitorder[$suit-1]}} ";
    }
}

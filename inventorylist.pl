#!/usr/bin/env -S perl -I.

# A perl script to show the contents of your inventory in a very nice layout.

use strict;
use warnings;

use InfiniteNomic qw/@suitorder @rankorder %colors @regionorder %regions/;

my $fh = undef;
my $reg = undef;
my $col = undef;
my $width = 4;

while (my $fa = shift @ARGV) {
    if ($fa =~ /^-/) {
        my $a = substr $fa, 1;

        if ($a eq "reg") {
            $reg = shift @ARGV or die "Expected argument for -reg";
        } elsif ($a eq "col") {
            $col = shift @ARGV or die "Expected argument for -col";
        } elsif ($a eq "w") {
            $width = shift @ARGV or die "Expected argument for -w";
            die "Invalid width $width" if ($width < 3);
        }
    } else {
        open $fh, "<", $fa or die "Could not open file $fa";
    }
}

@suitorder = grep { $regions{$_}->{$reg} } @suitorder if $reg;
@suitorder = grep { $colors{$_} eq $col } @suitorder if $col;

die "invalid region $reg" if (@suitorder == 0);

my %inventory = ();

my $string;
{
    local $/;
    if ($fh) {
        $string = <$fh>;
    } else {
        $string = <STDIN>;
    }
}

for (split /\s+/s, $string) {
    if (/\{\{Card\|\s*(.+?)\|\s*(.+?)\}\}/) {
        my ($suit, $rank) = ($2, $1);
        if (not defined $inventory{$suit}) {
            $inventory{$suit} = {};
        }

        if (not defined $inventory{$suit}->{$rank}) {
            $inventory{$suit}->{$rank} = 1;
        } else {
            $inventory{$suit}->{$rank}++;
        }
    }
}

print " |";
for my $s (@suitorder) {
    printf "\e[1;$colors{$s}m%${width}s\e[0m|", $s;
}
print "\n";

for my $r (@rankorder) {
    print "$r|";
    for my $s (@suitorder) {
        my $amount = 0;

        if (defined $inventory{$s}) {
            $amount = $inventory{$s}->{$r};
            $amount = 0 unless (defined $amount);
        }

        my $out = $amount > $width ? "($amount)" : $r x $amount;

        printf "\e[1;$colors{$s}m%${width}s\e[0m|", $out;
    }

    print "\n";
}

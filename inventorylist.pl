#!/usr/bin/env perl

# A perl script to show the contents of your inventory in a very nice layout.

use strict;
use warnings;

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

my @suitorder = (
    'L',
    'D',
    'Cp',
    'C',
    'A',
    'R',
    'B',
    'Sw',
    'Sh',
    'H',
    'Cn',
    'S'
);

my @rankorder = (
    'A',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'T',
    'E',
    'D',
    'H',
    'U',
    'O',
    'N',
    'B',
    'R',
    'Q',
    'K',
);

my %colors = (
    'L'  => '36',
    'D'  => '31',
    'Cp' => '33',
    'C'  => '30',
    'A'  => '36',
    'R'  => '31',
    'B'  => '33',
    'Sw' => '30',
    'Sh' => '36',
    'H'  => '31',
    'Cn' => '33',
    'S'  => '30',
);

my @regionorder = ('fr', 'es', 'de', 'ch');

my %regions = (
    'L'  => {'de' => 1},
    'D'  => {'fr' => 1},
    'Cp' => {'es' => 1},
    'C'  => {'fr' => 1, 'es' => 1},
    'A'  => {'de' => 1, 'ch' => 1},
    'R'  => {'ch' => 1},
    'B'  => {'de' => 1, 'ch' => 1},
    'Sw' => {'es' => 1},
    'Sh' => {'ch' => 1},
    'H'  => {'de' => 1, 'fr' => 1},
    'Cn' => {'es' => 1},
    'S'  => {'fr' => 1},
);

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

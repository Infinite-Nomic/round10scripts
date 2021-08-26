package InfiniteNomic;

use strict;
use warnings;
use parent 'Exporter';

our @suitorder = (
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

our @rankorder = (
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

our %colors = (
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

our @regionorder = ('fr', 'es', 'de', 'ch');

our %regions = (
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

our @EXPORT = qw/@suitorder @rankorder %colors @regionorder %regions/;

1;

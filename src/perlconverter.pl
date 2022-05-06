sub ParsePfcFile
{
    open PFC, $_[0] or die "Couldn't open $_[0]\n";
    binmode PFC;

    # The pfc file seems to start with the following header
    # struct PfcHead
    # {
    #    long id1;            // Seems to contain 0x005344f4
    #    long id2;            // Seems to contain 0x01234567
    #    long rsvd[13];       // Zeros
    #    short s1;            // Seems like number of fields minus one?
    #    short s2;            // Number of field structures
    # };
    #
    (read PFC, my $raw, 64) == 64 or die "Unable to read PFC header structure";

    my @header = unpack "L2L13SS", $raw;

    $header[0] == 0x005344F4 && $header[1] == 0x01234567 or
        die sprintf( "%s: Unexpected header code 0x%08x 0x%08x\n", $_[0], $header[0], $header[1] );

    for( my $i=0; $i<13; $i++ )
    {
        $header[2+$i]==0 or
            die sprintf( "%s: Reserved part of header contains 0x%08x at offset %d\n", $_[0], $header[2+$i], $i );
    }

    my $numFields = $header[16];

    # The header is followed by an array of field structures
    # struct PfcField
    # {
    #    char  name[28];    // name of field
    #    char  count;       // Number of elements
    #    char  type;        // element type (2 = ascii, 4 = short, 6 = long)
    #    short s2;          // Offset (bytes) from start of entry
    # };

    my %hash;
    my (@fname, @fcount, @ftype, @foffset);

#   print "\n" . $_[0] . ":\n" ;
    for( my $i=0; $i<$numFields; $i++ )
    {
        read( PFC, $raw, 32 ) == 32 or
            die sprintf( "%s: Error reading field structure, field number %d\n", $_[0], $i );
        ($fname[$i], $ftype[$i], $fcount[$i], $foffset[$i]) = unpack "A28CCS", $raw;

        # Create a hash entry using the field name as the key
        # and containing a reference to an empty array
        $hash{ $fname[$i] } = [];
    }

    # I'll use what I know about the file structure to
    # create the proper unpack format string.

    my $parseFmt;

    for( my $i=0; $i<$numFields; $i++ )
    {
        if( $ftype[$i] == 2 )
        {
            # ASCII string (Note that some strings have a count field set to 0)
            # this indicates that it starts with a short giving the length of the string
            # For now I can only handle this if it's the last field
            die "fcount of zero must be last element!\n" if( $fcount[$i]==0 && $i+1 != $numFields );

            $parseFmt .= "A*" if $fcount[$i] == 0;
            $parseFmt .= sprintf( "A%d", $fcount[$i] ) if $fcount[$i] > 0;
        }
        elsif( $ftype[$i] == 4 )
        {
            # Short integer
            $fcount[$i] == 1 or die "Can't handle a count > 1 for a short!\n";
            $parseFmt .= 'S';
        }
        elsif( $ftype[$i] == 6 )
        {
            # Short integer
            $fcount[$i] == 1 or die "Can't handle a count > 1 for a long!\n";
            $parseFmt .= 'L';
        }
        else
        {
            die sprintf( "Unknown type 0x%02x, %s\n", $ftype[$i], $_[0] );
        }
        print $parseFmt;
        print "\t";
        print sprintf( "%3d 0x%02x %3d  %s\n", $fcount[$i], $ftype[$i], $foffset[$i], $fname[$i] );
    }

    my $recIndex = 0;
    while( read( PFC, $raw, 6 ) == 6 )
    {
        # Each data record starts with a structure
        # struct PfcRecordHead
        # {
        #    short recLen;     // Length of each data record (bytes)
        #    short next;       // offset in bytes to next record
        #    short zero;       // seems to always be zero
        # };
        my @recHead = unpack "S3", $raw;

        read( PFC, $raw, $recHead[0]-6 ) == $recHead[0]-6 or die "Error reading record data\n";

        my @data = unpack $parseFmt, $raw;

        for( my $i=0; $i<$numFields; $i++ )
        {
            my $junk;
            ($junk, $data[$i]) = unpack "SA*", $data[$i] if $fcount[$i] == 0;

            $hash{ $fname[$i] }[$recIndex] = $data[$i];

#            print " " . $data[$i] if $ftype[$i] == 2;
#            print sprintf( " 0x%04x", $data[$i] ) if $ftype[$i] == 4;
#            print sprintf( " 0x%08x", $data[$i] ) if $ftype[$i] == 6;
        }
        $recIndex++;
#        print "\n";
    }
    close PFC;

    return %hash;

}

my %hash = ParsePfcFile("tests/data/_PFC._PS");
use Data::Dumper;

print Dumper(\%hash);
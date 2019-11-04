#!/bin/bash

function usage {
    echo "Incorrect number of arguments: $#"
    echo "usage: pdf_to_text.sh INFILE OUTFILE [-v]"
    echo "INFILE / OUTFILE must be *either* file paths or directory paths"
    exit 1
}

if [ $# -lt 2 ]
  # minimum of two arguments
  then
    usage
fi

function convert_pdf() {
    java -jar $PDFBOX_HOME ExtractText "$1" "$1.tmp"

    # we do this so that the script can be called form a folder other than the one it is in
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
    "$DIR/clean_txt.py" -o "$2" "$1.tmp" $3
    rm "$1.tmp"
}

if [[ -d $1  && -d $2 ]]; then
    # do an entire directory of conversions

    # required as most of the design briefs have spaces in their name
    # which breaks bash for loops
    SAVEIFS=$IFS
    IFS=$(echo -en "\n\b")

    # loop over the pdf files in the specified directory
    for filename in $1/*.pdf; do
        [ -e "$filename" ] || continue
        echo "Filename $filename"
        # generate the outputfile name
        OUTFILE=`basename $filename`
        OUTFILE="${OUTFILE%.*}"
        OUTFILE="$2/$OUTFILE".txt
        # actually convert the pdf
        convert_pdf "$filename" "$OUTFILE" "$3"
    done
    IFS=$SAVEIFS
elif [[ -f $1  ]]; then
    # just do one file
    convert_pdf "$@"
else
    echo "Arguments do not fit expected file/directory input structure"
    exit 1
fi


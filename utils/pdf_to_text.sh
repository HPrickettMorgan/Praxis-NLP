
function usage {
    echo "Incorrect number of arguments: $#"
    echo "usage: pdf_to_text.sh INFILE OUTFILE"
    exit 1
}

if [ $# -ne 2 ]
  then
    usage
fi

java -jar $PDFBOX_HOME ExtractText $1 "$1.tmp"
./clean_txt.py -o $2 $1.tmp
rm $1.tmp

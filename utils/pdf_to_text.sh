java -jar $PDFBOX_HOME ExtractText $1 "$1.tmp"
./clean_txt.py -o $2 $1.tmp
rm $1.tmp

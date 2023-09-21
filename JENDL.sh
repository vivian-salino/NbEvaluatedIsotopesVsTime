#!/bin/sh
# URL retrived from :
# https://wwwndc.jaea.go.jp/jendl/jendl.html#jendl-gp

for version in "2" "3.1" "3.2" "3.3" "4.0" "5"
do
    if [[ "$version" == "2" ]]; then
        url="https://wwwndc.jaea.go.jp/cgi-bin/evlret?Z=&A=&Selection=1&Lib=25"
    elif [[ "$version" == "3.1" ]]; then
        url="https://wwwndc.jaea.go.jp/cgi-bin/evlret?Z=&A=&Selection=1&Lib=39"
    elif [[ "$version" == "3.2" ]]; then
        url="https://wwwndc.jaea.go.jp/cgi-bin/evlret?Z=&A=&Selection=1&Lib=14"
    elif [[ "$version" == "3.3" ]]; then
        url="https://wwwndc.jaea.go.jp/cgi-bin/evlret?Z=&A=&Selection=1&Lib=0&Lib=17"
    elif [[ "$version" == "4.0" ]]; then
        url="https://wwwndc.jaea.go.jp/cgi-bin/evlret?Z=&A=&Selection=1&Lib=31"
    elif [[ "$version" == "5" ]]; then
        url="https://wwwndc.jaea.go.jp/cgi-bin/evlret?Z=&A=&Selection=1&Lib=60"
    fi
    wget -q -O webpage.html $url
    NbIso=$(grep ".dat.gz" webpage.html | wc -l)
    echo "NbIso['JENDL-"$version"'] =" $NbIso
    rm -f webpage.html
done

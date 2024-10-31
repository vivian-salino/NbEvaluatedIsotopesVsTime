#!/bin/sh

# JEF-2.2
cut -c 67-70 JEF-2.2/tape*.asc > cut.txt
NbIso=$(sort -un cut.txt | sed 's/ //g' | awk '{if(length() >= 3) print $0}' | wc -l)
rm -f cut.txt
echo "NbIso['JEF-2.2'] = "$NbIso

# Subsequent versions
for version in "3.0" "3.1" "3.1.1" "3.1.2" "3.3" "4T4"
do
    if [[ "$version" == "3.0" ]]; then
        prefix="JEFF30N"
    elif [[ "$version" == "3.1" ]]; then
        prefix="JEFF31N"
    elif [[ "$version" == "3.1.1" ]]; then
        prefix="JEFF311N"
    elif [[ "$version" == "3.1.2" ]]; then
        prefix="JEFF312N"
    elif [[ "$version" == "3.3" ]]; then
        prefix=""
    elif [[ "$version" == "4T4" ]]; then
        prefix=""
    fi
    NbIso=$(ls JEFF-"$version"/"$prefix"* | wc -l)
    echo "NbIso['JEFF-"$version"'] = "$NbIso
done






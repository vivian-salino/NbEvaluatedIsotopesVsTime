#!/bin/sh

# ENDF-B/II
tail -n +2 II/bnlendfb2tape20*.txt | cut -c 67-70 > cut.txt
NbIso=$(sort -un cut.txt | sed 's/ //g' | awk '{if(length() >= 3) print $0}' | wc -l)
rm -f cut.txt
echo "NbIso['ENDF-B/II'] = "$NbIso # Results has been checked by hand, scrolling in that file : 61

# ENDF-B/III
tail -n +2 III/bnlendfb3tape30*.txt | cut -c 67-70 > cut.txt
NbIso=$(sort -un cut.txt | sed 's/ //g' | awk '{if(length() >= 3) print $0}' | wc -l)
rm -f cut.txt
echo "NbIso['ENDF-B/III'] = "$NbIso # Results has been checked by hand, scrolling in that file : 133

# ENDF-B/IV
cut -c 67-70 IV > cut.txt
NbIso=$(sort -un cut.txt | sed 's/ //g' | awk '{if(length() >= 3) print $0}' | wc -l)
rm -f cut.txt
echo "NbIso['ENDF-B/IV'] = "$NbIso # Results has been checked by hand, scrolling in that file : 90

# ENDF-B/V.2
# MAT numbers (998, 999) are repeated in nt666a, nt666b, nt998, nt999, u_fiss_frags, pu_fiss_frags
# To account for that, we shall count the number of materials per tape, and then only perform the sum
sum=""
for tape in V.2/*
do
    tail -n +2 $tape | cut -c 67-70 > cut.txt
    NbIso=$(sort -un cut.txt | sed 's/ //g' | awk '{if(length() >= 3) print $0}' | wc -l)
    rm -f cut.txt
    if [ -z "$sum" ]; then
        sum=$NbIso
    else
        sum=$sum"+"$NbIso
    fi
done
echo "NbIso['ENDF-B/V.2'] = "$sum # Results has been checked by hand, scrolling in that file : 130

#---
#  ENDF-B/VI is much more complete than previous libraries (which had mostly only neutron data and a few TSL files)
#  As laid out by https://www.nndc.bnl.gov/endf-b6.8/summary.html, it also includes:
#  * Thermal neutron scattering on tapes 118, 119, 132, 133
#  * Fission product yields and radioactive decay data : 125, 126, 130, 131, 136, 210->211
#  * Proton, deuteron, triton on tapes 300->340
#  * Atomic/electronic/electro-atomic/photon on tapes 700->711
#  * High Energy (tapes 80*)
#  Here, we're only interested in the neutron data:
#    ENDF-B/VI.0 = tape100 to tape117
#    ENDF-B/VI.1 = tape120 to tape124
#    ENDF-B/VI.2 = tape127 to tape129
#    ENDF-B/VI.3 = tape134 to tape135
#    ENDF-B/VI.4 = tape137
#    ENDF-B/VI.5 = tape139 to tape144
#    ENDF-B/VI.6 = tape145 to tape153
#    ENDF-B/VI.7 = tape154 to tape155
#    ENDF-B/VI.8 = tape156 to tape163
#  Materials already present (at the same MAT number) are meant to replace their predecessors,
#  keeping from previous versions only materials without replacements.
#---
VI0=$(seq 100 117)
VI1=$(seq 120 124)
VI2=$(seq 127 129)
VI3=$(seq 134 135)
VI4=137
VI5=$(seq 139 144)
VI6=$(seq 145 153)
VI7=$(seq 154 155)
VI8=$(seq 156 163)
full=$VI0" "$VI1" "$VI2" "$VI3" "$VI4" "$VI5" "$VI6" "$VI7" "$VI8

# That portion of script (a bit long to execute) allows to find the tapes that contain a specific MAT (for all MATs)
#rm -f TapeForEachMAT.txt
## https://stackoverflow.com/questions/1521462/looping-through-the-content-of-a-file-in-bash
#while IFS="" read -r MAT || [ -n "$MAT" ]
#do
#    echo "MAT "$MAT >> TapeForEachMAT.txt
#    for tape in $full
#    do
#        if [ ${#MAT} -lt 4 ]; then
#            # https://unix.stackexchange.com/questions/48535/can-grep-return-true-false-or-are-there-alternative-methods
#            if tail -n +2 VI/tape.$tape | grep -q -E '^.{66} '$MAT; then
#                echo "tape."$tape >> TapeForEachMAT.txt
#            fi
#            #tail -n +2 VI/tape.$tape | grep --color=None -E '^.{66} '$MAT
#        else # MAT number is 4 character long
#            if tail -n +2 VI/tape.$tape | grep -q -E '^.{66}'$MAT; then
#                echo "tape."$tape >> TapeForEachMAT.txt
#            fi
#        fi
#    done
#    echo " " >> TapeForEachMAT.txt
#done < MAT_nums_VI8.txt

for minor in $(seq 0 8)
do
    rm -f cut.txt # Covering my back
    for i in $(seq 0 $minor)
    do
        tapes=VI$i
        for tape in ${!tapes}
        do
            tail -n +2 VI/tape.$tape | cut -c 67-70 >> cut.txt
        done
    done
    NbIso=$(sort -un cut.txt | sed 's/ //g' | awk '{if(length() >= 3) print $0}' | wc -l)
    rm -f cut.txt
    echo "NbIso['ENDF-B/VI."$minor"'] = "$NbIso # Results has been checked by hand for ENDF/B-VI.8 : 329
    # For other minor versions, they seem very reasonnable.
done

# ENDF-B/VII.0
echo "NbIso['ENDF-B/VII.0'] = "$(ls VII.0 | wc -l)
# ENDF-B/VII.1
echo "NbIso['ENDF-B/VII.1'] = "$(ls VII.1 | wc -l)
# ENDF-B/VIII.0
echo "NbIso['ENDF-B/VIII.0'] = "$(ls VIII.0 | wc -l)

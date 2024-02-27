rm -rf *_formatted
mkdir recombined_formatted depth10_formatted depth20_formatted
./formatter recombined recombined_formatted
./formatter depth10 depth10_formatted
./formatter depth20 depth20_formatted

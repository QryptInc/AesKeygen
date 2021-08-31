#!/bin/bash -e

apiToken=**COPY API TOKEN**
outFile=outfile.csv
keySize=32
ivSize=16
testKeys=1

let totSize=$keySize+$ivSize

curl "https://api-eus.qrypt.com/api/v1/quantum-entropy?size=100" \
    -H "accept: application/json" \
    -H "Authorization: Bearer $apiToken" \
    | jq --raw-output -j '.random[]' \
    | base64 --decode \
    > tmp.qrand

len=$(stat -ffz %s tmp.qrand)
 
echo "KEY, IV" > $outFile

for (( i=0; i<len/totSize; i++ ));
do 
    let keyOffset=$totSize*i
    let ivOffset=$totSize*i+$keySize

    aeskey="$(xxd -c 1000000 -ps -s $keyOffset -l $keySize)" 
    aesiv="$(xxd -c 1000000 -ps -s $ivOffset -l $ivSize)"

    echo "$aeskey, $aesiv" >> $outFile

    #test keys
    if [ $testKeys ]; then 
        echo 'test data' > plaintext.txt
        openssl enc -nosalt -e -aes-256-cbc -iv $aesiv -K $aeskey -in plaintext.txt -out ciphertext.txt
        openssl enc -nosalt -d -aes-256-cbc -iv $aesiv -K $aeskey -in ciphertext.txt > /dev/null
    fi 
   
done < tmp.qrand

rm tmp.qrand

echo 'success!'
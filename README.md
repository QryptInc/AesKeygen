# AES Keygen
The AES Keygen scripts demonstrates use of the EaaS API (https://www.qrypt.com/docs/eaas) to download Quantum Random, and convert that random to AES keys.  It will output a CSV file, each row being a keys and IV.

## How to Use
### Install Dependencies 

This script utilizes curl, jq, xxd.  These must be installed, e.g. for Debian based machines: 
```
apt-get install -y curl jq xxd
```

### Set Script Variables

The top of the script will contain some parameters to customize the behavior, as shown:   
```
apiToken=**COPY API TOKEN**
outFile=outfile.csv
keySize=32
ivSize=16
testKeys=1
```

- apiToken - __Required__.  This can be obtained by following the instructions at https://www.qrypt.com/docs/eaas, and copying from there the access token.
- outFile - Output path for the CSV file
- keySize - AES key size in bytes
- iv - IV size in bytes
- testKeys - Flag to test each key by encryption/decryption a string, using OpenSSL

### Run the script

The script itself is aes-key.sh, no parameters necessary.  


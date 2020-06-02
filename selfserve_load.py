#!/usr/bin/python3
import base58
import random

def rand_str(length):
    res = ''
    lower = 'abcdefghijklmnopqrstuvwxyz'
    upper = lower.upper()
    num = '01234567890'
    charset = lower + upper + num
    for i in range(0, length): #pylint: disable=unused-variable
        res += random.choice(charset)
    return res

for i in range(50):
    shell_snippet="""(
    DID='{DID}'
    VKEY='~{VKEY}'
    resp=$(curl -sSd "{{\\"network\\":\\"stagingnet\\",\\"did\\":\\"{DID}\\",\\"verkey\\":\\"~{VKEY}\\",\\"paymentaddr\\":\\"\\"}}" http://127.0.0.1:8080/nym 2>&1)
    if [ $? -ne 0 ] ; then
        echo "Request for DID: {DID} and VerKey: ~{VKEY} FAILED!!"
        echo "$resp"
    else
        if echo "$resp" | grep -q '"statusCode": 200' ; then
            echo "Request for DID: {DID} and VerKey: ~{VKEY} was successful"
        else
            echo "Request for DID: {DID} and VerKey: ~{VKEY} FAILED!!"
            echo "$resp"
        fi
    fi
) &""".format(DID=base58.b58encode(rand_str(16)).decode(), VKEY=base58.b58encode(rand_str(16)).decode())
    print(shell_snippet)
print('echo')
print('wait')

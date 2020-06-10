#!/usr/bin/python3
import base58
import random

REQUESTS=10
PMT_FREQ=10
PMT_ADDRESSES = [
    'pay:sov:2jubCfXhtK1MJzU4KzZj921NF4iYZ4mmumaPsfXfSxe3ALf3Zp',
    'pay:sov:2E8Tx64iBnV4w6YozcQcPEq2GqmotYo4YMGMpb5Ma6inDVVzhL',
    'pay:sov:8gdt4FLbeXtqoEjQaxCtCzTETDERJTWs7rkoEmGkbir6g4EEC',
    'pay:sov:ArDVLSbAfd2gz4CvRSnYN7LabHUsFGjPKL25taajv3fZHmXQP',
    'pay:sov:2YwWcFJFkv2E9dEVDVcTvtRmbaoJViJMJvkcP5qVeZiLjMpeHL',
    'pay:sov:2eV6Cs6aUNUZKr24iGoRrmCAyr6QyYXyEzsFCU3JfDr15kX2W7',
    'pay:sov:2jRRxETR8hhQf2Lh26PPpd1y3kuLg3AUJEZbwqx8RD7jyTURxB',
    'pay:sov:7Uv86XCr1SZnCq9WVFZvRigbNfbSUZPD6L8ff4wM7B68WzN7H',
    'pay:sov:2ZkeSgER8w4QmYEWVDms4sW9NwB5G1LAQzJREx3FpnEkyrTgGy',
    'pay:sov:2ViUZnYGwYxx2EztvxAYq8re9ysmCVbzF72jTCXMKzrxUqGqut',
    'pay:sov:KYzskWwFPFA1QnKagPMu88byekjpycMmGU3uGGSNUhHtJkAJ1',
    'pay:sov:uFrfH2RsiUTUR3XfKj51Pucg4y68ngdtVaTmQEqtCJgaAKCy1',
    'pay:sov:y69V629dvZdC5sTk4EpuboNWFz7TjKos57cTzDGJeJ8YWMnAv',
    'pay:sov:yufGBdSNLNHj8UuCXAtvWQqajEQQHD8PbSiL3P18r8x1FhQde',
    'pay:sov:2vpvEKBciqduz3qyj4FiKxgYnqi1bhsY2Ro1v8bWBpMt2ZhmLR',
    'pay:sov:2vJAHeMP4CtPmiWuGaY1QK4g6AKSu1LvxruQwQLYay31hisVNy',
    'pay:sov:2HEig5A9X6J1X4ujxR1mAizjXLNaimiNb1hVNarokvohxgYVJs',
    'pay:sov:XRD9HMv7yHKPKX18uvGwhgBamKxPr1yiFiYsKBY2orS4uptvH',
    'pay:sov:2bYQJ1nDCTt4DeqLnwktXaqq1y7w9iLGqFyYmpFWnC9qWLT4yk',
    'pay:sov:88UuxqXT9PGyQ5AYyjQZB5HoC8PCmkq96iMTrdRm4GCyVfiYG',
    'pay:sov:2WN3sCng32mYMomvoNNViufLcizxHuVWPAiqph1C9D9gsqFaz4',
    'pay:sov:ZYA3syg1VGwi1aCZaJwkn7DJXgMhf1Ysqg6CKoDjNzmtvrTnU',
    'pay:sov:fnET6LDp56Nk6dWBtjhQ3NSZk9PNLkQN59HWV2agxE9A2Y6bD',
    'pay:sov:2qAnTs6NtiKdNd4ERBPUT3FaeQv3f7wTBs16p9CWeG1vRYBRCD',
    'pay:sov:28HcwEduRBnjXnEeVU5bnEZW23Xb41FWNGAadUSciBS2oWHzLJ',
    'pay:sov:knnDaBLUbGKcwe6zsZsbfYCMf9Ttw6rdrCS9DXV2wUyoxdPfK',
    'pay:sov:CLVWoSzDTNoezEZMTquKHj5EuPFGv7GR8EgF7GxUSKS7vNQuC',
    'pay:sov:26BXR7tJksqUhnXrBAQnZ1b4B1JDkrZQbENs2xJTojKsgLaouP',
    'pay:sov:2VLawnEyKraMjQZcs7N65EAVyuAzNZaduC5QznVySHghJvmZss',
    'pay:sov:aSvSQFGTg36AwymrpqkvgXQCk4jZnsvpYZ5JGXs9PdYsLVstm',
    'pay:sov:K1pNHhD8mPWPJMszv6TvdEUjnA2C93h9mkahWqnkwnDdHKy5T',
    'pay:sov:U4PmSSNjeDvGKcMcPzN459moEBPVgvTDinL5uvz8sBCdM4ti5',
    'pay:sov:8NEiuuXj3aFtsVPEY23C7YroSxm6SLxrfsx8bDzPV1tkeGyAK',
    'pay:sov:ne3tDPSi8Dy1EZbRn6d562o4pDbjhL8HSK4fv4zK5DAJSzJkZ',
    'pay:sov:2jhGPuFBehvVnU66Vs9exyS8dNEYQj6FmjKNDXnDRbJaWtAxMP',
    'pay:sov:2KQZUZSJT8YLdghnw5Wkv4Qrx3Fr2f41B3LqYVMmxrsMfT9yQo',
    'pay:sov:ZH7auXKhaRN73S4wQEqw4J7tEiRw4bXB1RDFWFCD84kxUUchK',
    'pay:sov:2hx1ATByb41QcoBbfSByojniqskChxcBHq3UbqBsourpdnYcnu',
    'pay:sov:277RjnXtfr8ofest7acCNBBkFPuTLpYCK8hjexpfTzKnkz9711',
    'pay:sov:TaNwmPQojDdebbP55QYNnHRhJWX4rdBvBB6wCfe28uW5Y5zBg',
    'pay:sov:2ZGJYgXnjxeWfCESeBpHJTCFZyQAjxPcAnEJ3zMeLVMSaJaLDj',
    'pay:sov:2k5NPbfEAFWnSRCgs1REduyjdAC2frWSCAbQMPDvP7CFqZ1mDQ',
    'pay:sov:2F1fNgvQLL75mtrKcL35CUASd2Rc9k58Ys526HqRTv7yJths6o',
    'pay:sov:JV3FGt2gSi8QSTz6kEFjK5a9bWmp7LQnGwjfkyLhGuhzqMKZ2',
    'pay:sov:2UzoExS3eMRhtTghypDAJRb5xKXU1gwM3JUHUN1AN2aY4XnwPP',
    'pay:sov:t1xij7pDsrFtGjgZmf2f39yKsVwFE3Viz6Rk1eh2tjmepASX3',
    'pay:sov:2jGA39baT6hkNMfYyC1dwEtMFrxAkeQFcUAFEVxZ6HgYuSKGvt',
    'pay:sov:ptgE5B1RBPS1p6J1mtZ71oKz16mhKaAz2Usmuaynw7tf64KZr',
    'pay:sov:2SEfU5xZRnczdmLQ1btbHbGK9WkedyxL9DVcfG6xumDHLzPjbM',
    'pay:sov:2d8eomWx6eQCNtemDzpvzTk1NCkgDX136ecLtEPFzbe3eiwCQC'
]

def rand_str(length):
    res = ''
    lower = 'abcdefghijklmnopqrstuvwxyz'
    upper = lower.upper()
    num = '01234567890'
    charset = lower + upper + num
    for i in range(0, length): #pylint: disable=unused-variable
        res += random.choice(charset)
    return res

for i in range(REQUESTS):
    pmt_static_idx = 0
    if i % PMT_FREQ == 0:
        pmt = PMT_ADDRESSES[pmt_static_idx]
        pmt_static_idx += 1
        if pmt_static_idx > len(PMT_ADDRESSES):
            pmt_static_idx = 0
    shell_snippet="""(
    resp=$(curl -sSd "{{\\"network\\":\\"stagingnet\\",\\"did\\":\\"{DID}\\",\\"verkey\\":\\"~{VKEY}\\",\\"paymentaddr\\":\\"{PMT}\\"}}" http://127.0.0.1:8080/nym 2>&1)
    if [ $? -ne 0 ] ; then
        echo "Request for DID: {DID} and VerKey: ~{VKEY} FAILED!!"
        echo "$resp"
    else
        if echo "$resp" | grep -q '"statusCode": 200' ; then
            echo "Request for DID: '{DID}' VerKey: '~{VKEY}' and Payment address: '{PMT}' was successful"
        else
            echo "Request for DID: '{DID}' VerKey: '~{VKEY}' and Payment address: '{PMT}' FAILED!!"
            echo "$resp"
        fi
    fi
) &""".format(DID=base58.b58encode(rand_str(16)).decode(), VKEY=base58.b58encode(rand_str(16)).decode(), PMT=pmt)
    pmt = ''
    print(shell_snippet)
print('echo')
print('wait')

import asyncio
import json
import random
import logging
import argparse
from ctypes import cdll
from time import sleep
from twilio.rest import Client

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from indy import anoncreds, crypto, did, ledger, pool, wallet, payment, blob_storage

# check arguments
parser = argparse.ArgumentParser()
parser.add_argument("pool_name", help="the pool you want to connect to.")
parser.add_argument("wallet_name", help="wallet name to be used")
parser.add_argument("wallet_key", help="wallet key for opening the wallet")
parser.add_argument("signing_did", help="did used to sign requests sent to the ledger")


config = {}
creds = {}
async def main():

    args = parser.parse_args()

    pool_name = args.pool_name
    wallet_name = args.wallet_name
    wallet_key = args.wallet_key
    submitter_did = args.signing_did

    config["id"] = wallet_name
    creds ["key"]= wallet_key

    logger.info("==============================")
    logger.info("=== Connecting to pool ==")
    logger.info("------------------------------")
    # Set protocol version 2 to work with Indy Node 1.4
    await pool.set_protocol_version(2)
    pool_handle   = await pool.open_pool_ledger(pool_name, None) 
    wallet_handle = await wallet.open_wallet(json.dumps(config),json.dumps(creds))

    logger.info("get validator info")
    validator_info_request = await ledger.build_get_validator_info_request(submitter_did)
    resp = await ledger.sign_and_submit_request(pool_handle, wallet_handle, submitter_did, validator_info_request)
    #print(resp)

    #-----------------------------
    #parse response for report
    errors = ''
    nodeversions = {}
    for key,val in json.loads(resp).items():
        print("* " + key)
        #print("     Total_nodes_count "+ str(json.loads(val)["result"]["data"]["Pool_info"]["Total_nodes_count"]))
        #print(val)
        if val in {"timeout"}:
            print("ERROR: No validator info found for Node: "+key)
            errors = errors + " "+ "ERROR: No validator info found for Node: " + key + " "
            continue
        print("     Unreachable_nodes_count: "+ str(json.loads(val)["result"]["data"]["Pool_info"]["Unreachable_nodes_count"]) + " " + str(json.loads(val)["result"]["data"]["Pool_info"]["Unreachable_nodes"]))
        print("     Installed Packages: ")
        #print(str(json.loads(val)["result"]["data"]["Software"]["Installed_packages"]))
        nodeversions[key] = {}
        for packandver in json.loads(val)["result"]["data"]["Software"]["Installed_packages"]: 
            package, version = packandver.split()
            nodeversions[key][package] = version
            #print("        %s: %s" % (package, version))
        if json.loads(val)["result"]["data"]["Pool_info"]["Total_nodes_count"] != json.loads(val)["result"]["data"]["Pool_info"]["Reachable_nodes_count"]:
            errors = errors + " "+ key+ " "+ "Unreachable_nodes_count "+ str(json.loads(val)["result"]["data"]["Pool_info"]["Unreachable_nodes_count"])+"\r"
    #-----------------------------

    #print(nodeversions)
    for node in nodeversions:
        for package in nodeversions[node]:  #change this to a list of packages that we care about 
            #print(node + ":" + package + "\n")
            compval = nodeversions[node][package]
            total = 0
            same = 0
            otherval = ''
            for nodecomp in nodeversions:
                if package in nodeversions[nodecomp]:
                    total += 1
                    if compval == nodeversions[nodecomp][package]:
                        same += 1
                    else: 
                        otherval = nodeversions[nodecomp][package]
            if (same/total) < .5:
                print("Same = %d" % same)
                print("Total = %d" %total) 
                print(" MISMATCH: The %s node has version %s of the %s package and most nodes have version %s" % (node, compval, package, otherval))

    if errors != '':
        account_sid = 'ACd6de81bdde5d5f6d7772b96126dedf92'
        auth_token = 'cb677df10228c95ed6fc8fd7f1e8bc98'
        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                            body= errors,
                            from_='+18019809747',
                            to=   '+18017356453'
                        )

        #print(message.sid)

    logger.info("Close pool and wallet")
    await wallet.close_wallet(wallet_handle)
    await pool.close_pool_ledger(pool_handle)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

import json
import logging
import sys
import asyncio
import os
import configparser
import tempfile
import argparse
import datetime
import base58
import re
from aiohttp import web
import platform
from ctypes import cdll

# Set this flag to true if running this script in an AWS VM or a lambda. False if in a Virtualbox VM.
AWS_ENV=False

if AWS_ENV:
    import aioboto3

from indy import ledger, did, wallet, pool, payment
from indy.error import ErrorCode, IndyError

#BuilderNetPool = "testpool" #"buildernet"
#StagingNetPool = "testpool" #"stagingnet"
Wallet = "stewardauto" #"test"
WalletKey = "stewardauto" #"test"
StewardDID = "V5qJo72nMeF7x3ci8Zv2WP" #"Th7MpTaRZVRYnPiabds81Y" #"V5qJo72nMeF7x3ci8Zv2WP"
BuilderPaymentAddress="pay:sov:52CuALbWKBX66sDnmf8zL5HvxFYyjzFNuaibERRNhPgKP1bBu"
StagingPaymentAddress="pay:sov:2k8PCrjjMZUpQo6XGef1duDpeFQrhHf3A2BnWKmMBh5nuegNuD"
TrainingPaymentAddress="pay:sov:4RqyLsoQokLaYRuqb8YS3z6Rr7ouTy8UBGzB6QzjiYRaiZiK1"
text="Transaction Author Agreement V1.1\n\n1\n\n\fApproved by the Sovrin Board of Trustees 22 May 2019\nThis Transaction Author Agreement (the “<200b>Agreement<200b>”) is entered into between the Sovrin\nFoundation, a nonprofit corporation organized under the laws of the State of Utah, United States\nof America, and ___________ (“<200b>Transaction <200b>Author<200b>”), either a natural person acting as an\nIndividual or a _________ organized under the laws of _________. Sovrin Foundation and\nTransaction Author are individually referred to herein as a “Party” and collectively as the\n“Parties.”\nWHEREAS, the Transaction Author desires to write Transactions to the Sovrin Ledger;\nWHEREAS, the Sovrin Foundation desires to grant permission to the Transaction Author to\nwrite Transactions to the Sovrin Ledger;\nWHEREAS, subject to the Transaction Author complying with the terms and conditions of this\nAgreement, the Sovrin Foundation grants permission to the Transaction Author to write\nTransactions to the Sovrin Ledger;\nWHEREAS, subject to the Transaction Author complying with the terms and conditions of this\nAgreement, the Transaction Author accepts permission from the Sovrin Foundation to write\nTransactions to the Sovrin Ledger;\nFOR GOOD AND VALUABLE CONSIDERATION, THE SUFFICIENCY OF WHICH IS HEREBY\nACKNOWLEDGED, THE PARTIES AGREE AS FOLLOWS:\n\n1) Definitions\nUnless otherwise defined above, all capitalized terms used in this Agreement shall have the\nmeanings given to them in this Agreement or in the <200b>Sovrin Governance Framework and\ncorresponding <200b>Sovrin Glossary<200b>. The Sovrin Governance Framework and Sovrin Glossary is\nincorporated into this Agreement by reference only for purposes of use of such defined\nterms.\n\n2) Permission to Write to the Sovrin Ledger\na. The Sovrin Foundation grants to the Transaction Author the revocable right to write to\nthe Sovrin Ledger provided that the Transaction Author remains in compliance with all of\nits obligations under this Agreement.\nb. When authoring transactions under the policy of Permissioned Write Access, a\nTransaction Author may only write to the Sovrin Ledger by using an authorized\n\n2\n\n\fTransaction Endorser. In the event that Sovrin Foundation enables Public Write Access\nto the Sovrin Ledger, the Transaction Author will not need a Transaction Endorser to\nendorse a Transaction.\nc. Once an initial Transaction has been written to the Sovrin Ledger by the Transaction\nAuthor (“Initial Transaction”), the Transaction Author is granted permission to make\nadditional Transactions to update the state of a previous Transaction (“Update\nTransactions”). A Transaction Author may make Update Transactions if and only if the\nTransaction Author was the Author of the Initial Transaction. Update Transactions are\nTransactions and are subject to all the terms of this Agreement.\n\n3) Transaction Author Obligations\na. With regard to all Transactions written by or on behalf of the Transaction Author to the\nSovrin Ledger (“<200b>Authored Transactions<200b>”), the Transaction Author represents and\nwarrants that:\n1. it has all necessary rights and permissions to write the Authored Transactions;\n2. the Authored Transactions do not and will not violate any applicable law;\n3. the Authored Transactions will not contain data or information that infringes or\nmisappropriates the intellectual property rights of any third party;\n4. it will comply with any requirements imposed by the Transaction Endorser on the\nTransaction Author and any Authored Transactions endorsed by the Transaction\nEndorser;\n5. it will not author Transactions containing Personal Data as that term is defined in\nthe European Union’s General Data Protection Regulation (“<200b>GDPR<200b>”), except:\ni.\nIn the event that Sovrin Foundation permits Authored Transactions to\ncontain Personal Data, then the Transaction Author represents and\nwarrants that:\nA. it has received express, written consent, in the form required by all\napplicable laws, for the Personal Data to be permanently stored\non the Sovrin Ledger prior to writing such Personal Data to the\nSovrin Ledger;\nB. the consent includes a provision that permits the Data Subject to\nwithdraw its consent or exercise its right to be forgotten pursuant\nto applicable law; and\nC. if the Data Subject who provided express, written consent for the\nstorage of Personal Data on the Sovrin Ledger withdraws its\nconsent or if the Data Subject exercises a right to be forgotten, the\nwithdrawn consent and right to be forgotten request will be\neffectuated by marking the applicable Transaction(s) with a\nTombstone (if such functionality is enabled on the Sovrin Ledger)\nand that such marking will fully satisfy the withdrawn consent\nand/or right to be forgotten request, as applicable.\n6. the Transaction Author shall maintain such written consents (referenced in\n\n3\n\n\fSection 3(a)(5)) for a period of seven (7) years thereafter.\nb. Transaction Author may request that a Steward mark a Transaction as a Node-Specific\nTombstone (if such functionality is enabled on the Sovrin Ledger) if it is invoking a Data\nSubject’s right to erasure of Personal Data.\n\n4\n\n\f4) Governing Law and Forum\nThis Agreement is governed by the law of the State of Delaware, without reference to\nconflict of laws principles. All disputes arising out of or in connection with this Agreement\nshall be finally settled by binding arbitration under the Rules of Arbitration of the International\nChamber of Commerce by a single arbitrator appointed in accordance with the said Rules.\nUnless the Parties otherwise mutually agree, such arbitration shall be conducted in the\nEnglish language by electronic exchange of documents and by videoconference. The\narbitrator shall issue a reasoned decision, including findings of fact and conclusions of law.\nThe arbitrator shall require exchange by the Parties of documents relevant to the issues\nraised by any claim, defense, or counterclaim or on which the producing Party may rely in\nsupport of or in opposition to any claim, defense, or counterclaim, with due regard for\neliminating undue burden and expense and the expedited and lower cost nature of\narbitration. At the request of a Party, the arbitrator may at his or her discretion order the\ndeposition of witnesses. Depositions shall be limited to a maximum of three depositions per\nParty, each of a maximum of four hours duration, unless the arbitrator otherwise determines.\nDemand for arbitration may be initiated by either Party on fifteen (15) days written notice by\nemail to the other Party’s designated representative, together with a written specification of\nthe grounds for the dispute and the relief requested. By agreeing to binding and\nnon-appealable arbitration, each party understands that they each forever give up and waive\nany right which each Party may have to resolve any such claim, difference or dispute by\ncourt or jury trial. Notwithstanding the foregoing, either Party may bring a proceeding\nseeking equitable or injunctive relief solely and exclusively in the state and federal courts\nlocated in Wilmington, Delaware, to prevent the infringement of intellectual property rights or\nthe disclosure of confidential information. Each Party hereto consents to the exclusive\njurisdiction of such courts for the adjudication of any such equitable or injunctive relief, as\nwell as for any such matters that are excluded from or fall outside of this arbitration\nprovision.\n\n5) Representations and Warranties; Disclaimer\na. By Sovrin Foundation<200b>.\n1. SOVRIN FOUNDATION MAKES NO WARRANTY CONCERNING THE\nACCURACY, RELIABILITY, OR COMPLETENESS OF ANY INFORMATION OR\nDATA OBTAINED OR DERIVED THROUGH THE USE OF THE SOVRIN LEDGER,\nAND DISCLAIMS ANY OTHER REPRESENTATIONS OR WARRANTIES,\nEXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION, ANY WARRANTIES\nOF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE,\nNON-INFRINGEMENT, ACCURACY OR COMPLETENESS OF DATA.\nb. By Transaction Author.\n1. Transaction Author represents that it understands that the Sovrin Ledger operates on\na distributed network and that Sovrin Foundation disclaims any responsibilities with\n\n5\n\n\frespect to access of data from the Sovrin Ledger.\n2. Transaction Author represents that it understands and acknowledges that Sovrin\nFoundation does not control the transfer of data between Nodes and over\ncommunications facilities, including the internet, and that the Sovrin Ledger may be\nsubject to limitations, delays, and other problems inherent in the use of such\ncommunications facilities.\n3. Transaction Author represents that it understands and acknowledges that there is\nregulatory uncertainty regarding the Sovrin Ledger’s compliance with GDPR as it\nrelates to Permissioned Write Access, Public Write Access, and Personal Data,\nincluding as it relates to cross-border transfers of data, restrictions of processing\ndata, the right to effective erasure of data, as well as the scope and nature of\nPersonal Data itself. Transaction Author further represents that it understands and\nacknowledges that Sovrin Foundation may modify, at any time, its Sovrin Ledger\nAccess Policies and the terms of this Agreement and any other agreement or\ndocument related to the Sovrin Ledger based on new information, guidance, or law\nrelated to GDPR compliance.\n4. Transaction Author represents that it understands and acknowledges that a Steward\nhas discretion to mark a Transaction as a Node-Specific Tombstone (if such\nfunctionality is enabled on the Sovrin Ledger) if (i) the Transaction Author makes a\nrequest pursuant to Section 3(b); (ii) the Steward or Sovrin Foundation is required to\ndo so by a court order; (iii) or if the Steward or Sovrin Foundation has evidence that\nthe Transaction violates the terms of this Agreement.\n\n6) Limitation of Liability\nEXCEPT IN THE EVENT OF EITHER PARTY’S GROSS NEGLIGENCE, WILLFUL\nMISCONDUCT OR FRAUD, IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY\nINDIRECT,\nINCIDENTAL,\nEXEMPLARY,\nPUNITIVE,\nSPECIAL, OR OTHER\nCONSEQUENTIAL DAMAGES UNDER THIS AGREEMENT, INCLUDING, WITHOUT\nLIMITATION, ANY LOST PROFITS, BUSINESS INTERRUPTION, LOSS OF PROGRAMS\nOR DATA, OR OTHERWISE, EVEN IF THE OTHER PARTY IS EXPRESSLY ADVISED OF\nTHE POSSIBILITY OR LIKELIHOOD OF SUCH DAMAGES.\nEXCEPT IN THE EVENT OF EITHER PARTY’S GROSS NEGLIGENCE, WILLFUL\nMISCONDUCT OR FRAUD, IN NO EVENT SHALL EITHER PARTY’S LIABILITY UNDER\nTHIS AGREEMENT EXCEED $250,000 USD IN THE AGGREGATE. IN THE EVENT OF\nEITHER PARTY’S GROSS NEGLIGENCE, SUCH PARTY’S LIABILITY UNDER THIS\nAGREEMENT SHALL NOT EXCEED $500,000 USD IN THE AGGREGATE. IN THE\nEVENT OF EITHER PARTY’S WILLFUL MISCONDUCT OR FRAUD, THERE SHALL BE\nNO DOLLAR CAP ON SUCH PARTY’S LIABILITY UNDER THIS AGREEMENT.\n\n7) Miscellaneous\na. Notice<200b>. Any notice, payment, demand or communication required or permitted to be\n\n6\n\n\fb.\n\nc.\n\nd.\n\ne.\n\nf.\n\ng.\n\nh.\n\ni.\n\n7\n\ndelivered or given by the provisions of this Agreement shall be deemed to have been\neffectively delivered or given and received on the date personally or electronically\ndelivered to the respective Party to whom it is directed, or when deposited by registered\nor certified mail, with postage and charges prepaid and addressed to the Parties at the\naddresses set forth below opposite their signatures to this Agreement.\nSeverability<200b>. If any provision of this Agreement is held invalid, illegal, or unenforceable,\nthe validity, legality, and enforceability of any of the remaining provisions of this\nAgreement shall not in any way be affected or impaired.\nRelationship of the Parties<200b>. This Agreement does not create a partnership, franchise,\njoint venture, agency, fiduciary or employment relationship between the Parties. Neither\nParty will represent that it has any authority to assume or create any obligation, express\nor implied, on behalf of the other Party, nor to represent the other Party as agent,\nemployee, franchisee, or in any other capacity. There are no third-party beneficiaries to\nthis Agreement. Neither Party shall make any proposals, promises, warranties,\nguarantees, or representations on behalf of the other Party or in the other Party’s name.\nAssignment<200b>. Neither Party will voluntarily, or by operation of law, assign or otherwise\ntransfer this Agreement without the other Party’s express prior written consent which will\nnot be unreasonably withheld, provided that no such consent is required for an\nassignment or transfer to a wholly or majority owned subsidiary or to a successor in\ninterest by reason of merger or consolidation or sale of all or substantially all of the\nassets of such Party relating to the subject matter of this Agreement.\nWaiver<200b>. The waiver by either Party of a breach, default, delay or omission of any of the\nprovisions of this Agreement by the other Party will not be construed as a waiver of any\nsubsequent breach of the same or other provisions.\nEntire Agreement<200b>. This Agreement, including all documents incorporated into this\nAgreement by reference, constitutes the entire agreement of the Parties with respect to\nthe subject matter of this Agreement, and supersedes any and all prior agreements and\nunderstandings of the Parties, whether written or oral, with respect to such subject\nmatter.\nModification of This Agreement<200b>. Sovrin Foundation reserves the right to modify this\nAgreement at any time in accordance with this provision, including, but not limited to,\nchanges in applicable law or guidance from any jurisdiction. Sovrin Foundation will post\nan amended version of this Agreement on its website at least ninety (90) days prior to\nthe effective date of the amendment (the “Amendment Effective Date”). If Transaction\nAuthor continues to Author Transactions to the Sovrin Ledger after the Amendment\nEffective Date, such continued use will constitute acceptance of the amended\nAgreement.\nCounterparts<200b>. This Agreement may be executed in two or more counterparts, each of\nwhich will be deemed an original, but all of which taken together will constitute one and\nthe same instrument\nSurvival<200b>. Any terms that by their nature survive termination or expiration of this\nAgreement shall survive.\n\n\f8) Signatures\nThe Parties hereto have caused this Agreement to be executed by their duly authorized\nrepresentatives as of the Effective Date.\n\nSovrin Foundation\nBy:\n\n________________________\n\nName:\n\n_____________________\n\nTitle:\n\n______________________\n\nDate:\n\n______________________\n\nTransaction Author\nBy:\n\n________________________\n\nName:\n\n_____________________\n\nTitle:\n\n______________________\n\nDate:\n\n______________________\n\nIn the presence of:\nName:\n\n_____________________\n\nTitle:\n\n______________________\n\nAddress: ______________________\n\n8\n\n\f"

PAYMENT_LIBRARY = 'libsovtoken'
PAYMENT_METHOD = 'sov'
PAYMENT_PREFIX = 'pay:sov:'
DEFAULT_TOKENS_AMOUNT=200000000000

logger = logging.getLogger('indy') #(__name__)
logger.setLevel(logging.DEBUG)

# Uncomment the following to write logs to STDOUT
#
#stdoutHandler = logging.StreamHandler(sys.stdout)
#stdoutHandler.setLevel(logging.DEBUG)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#stdoutHandler.setFormatter(formatter)
#logger.addHandler(stdoutHandler)

async def writeEndorserRegistrationLog(entry, status, reason, isotimestamp):
    if AWS_ENV:
           # Write an item to the trust_anchor_registration table in DynamoDB
            async with aioboto3.resource('dynamodb', region_name='us-west-2', endpoint_url="https://dynamodb.us-west-2.amazonaws.com") as dynamo_resource:
                table = dynamo_resource.Table('trust_anchor_registration')
                await table.put_item(
                    Item={
                        'did': entry['DID'],
                        'timestamp': isotimestamp,
                        'paymentaddr': entry['paymentaddr'],
                        'sourceIP': 'unknown',
                        'verkey': entry['verkey'],
                        'status': status,
                        'reason': reason
                    }
                )

async def addNYMs(network, NYMs):
    # A dict to hold the results keyed on DID
    result = {
        "statusCode": 200
    }

    steward_did = StewardDID
    # Open pool ledger
    pool_name = network
    await pool.set_protocol_version(2)

    logger.debug("Before open pool ledger %s.", pool_name)
    pool_handle = await pool.open_pool_ledger(pool_name, None)
    logger.debug("After open pool ledger %s.", pool_name)
 
    # Open Wallet and Get Wallet Handle
    logger.debug("Before open steward_wallet")
    wallet_name = Wallet
    wallet_config = json.dumps({"id": wallet_name})
    wallet_credentials = json.dumps({"key": WalletKey})
    steward_wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)

    # Use Steward DID
    #logger.debug("Before use steward did")
    #steward_did_info = {'did': steward_did}
    #print(steward_did_info)
    #await did.store_their_did(steward_wallet_handle, json.dumps(steward_did_info))
    #logger.debug("After use steward did")

    # Prepare and send NYM transactions
    isotimestamp = datetime.datetime.now().isoformat()
    for entry in NYMs:
        status = "Pending"
        statusCode = 200
        reason = "Check if DID already exists."
        logger.debug("Check if did >%s< is an emptry string" % entry["DID"])
        if (len(entry["DID"]) == 0):
           break

        # Log that a check for did on Network is in progress. Logging this
        # status/reason may be useful in determining where interation with the Network
        # may be a problem (timeouts).
        #logger.debug("Before write Endorser registration log")
        #await writeEndorserRegistrationLog(entry, status, reason, isotimestamp)
        #logger.debug("After write Endorser registration log")
  
        # Does the DID we are assigning Endorser role exist on the ledger?
        logger.debug("Before build_get_nym_request")
        get_nym_txn_req = await ledger.build_get_nym_request(steward_did, entry["DID"])
        logger.debug("After build_get_nym_request")
        logger.debug("Before submit_request")
        get_nym_txn_resp = await ledger.submit_request(pool_handle, get_nym_txn_req)
        logger.debug("After submit_request")
        logger.debug("submit_request JSON response >%s<", get_nym_txn_resp)
        get_nym_txn_resp = json.loads(get_nym_txn_resp)
  
        # Create identity owner if it does not yet exist
        if (get_nym_txn_resp['result']['data'] == None):
            reason = "DID does not exist. Creating Endorser identity."
            # Log that a check for did on STN is in progress. Logging this
            # status/reason may be useful in determining where interation with the STN
            # may be a problem (timeouts).
            #logger.debug("Before write Endorser registration log")
            #await writeEndorserRegistrationLog(entry, status, reason, isotimestamp)
            #logger.debug("After write Endorser registration log")

            logger.debug("DID %s does not exist on the ledger. Will create identity owner with role %s.", entry["DID"], entry["role"])
            logger.debug("Before build_nym_request")
            nym_txn_req = await ledger.build_nym_request(steward_did, entry["DID"], entry["verkey"], entry["name"], entry["role"])
            logger.debug("After build_nym_request")
            logger.debug("Before sign_and_submit_request")
            await ledger.sign_and_submit_request(pool_handle, steward_wallet_handle, steward_did, nym_txn_req)
            logger.debug("After sign_and_submit_request")
            logger.debug("Before sleep 3 seconds")
            await asyncio.sleep(3)
            logger.debug("After sleep 3 seconds")

            reason = "Endorser identity written to the ledger. Confirming DID exists on the ledger."
            # Log that a check for did on STN is in progress. Logging this
            # status/reason may be useful in determining where interation with the STN
            # may be a problem (timeouts).
            #logger.debug("Before write Endorser registration log")
            #await writeEndorserRegistrationLog(entry, status, reason, isotimestamp)
            #logger.debug("After write Endorser registration log")

            # Make sure the identity was written to the ledger with the correct role
            logger.debug("Make sure DID was written to the ledger with a ENDORSER role")
            logger.debug("Before build_get_nym_request")
            get_nym_txn_req = await ledger.build_get_nym_request(steward_did, entry["DID"])
            logger.debug("After build_get_nym_request")
            logger.debug("Before submit_request")
            get_nym_txn_resp = await ledger.submit_request(pool_handle, get_nym_txn_req)
            logger.debug("After submit_request")
            logger.debug("submit_request JSON response >%s<", get_nym_txn_resp)
            get_nym_txn_resp = json.loads(get_nym_txn_resp)
            if (get_nym_txn_resp['result']['data'] != None):
                get_nym_txn_resp = json.loads(get_nym_txn_resp['result']['data'])
                # TODO: figure out how to map "ENDORSER" to the numeric "101"
                #       without hardcoding it.
                if (get_nym_txn_resp['role'] != "101"):
                    # TODO: Give a more accurate reason why the write to the ledger failed.
                    status = "Error"
                    statusCode = 404
                    reason = "Failed to write NYM identified by %s to the ledger with role %s. NYM exists, but with the wrong role. Role ID is %s" % (entry["DID"], entry["role"], get_nym_txn_resp['role'])
                    logger.error(reason)
                else:
                    status = "Success"
                    statusCode = 200
                    reason = "Successfully wrote NYM identified by %s to the ledger with role %s" % (entry["DID"], entry["role"])
                    logger.debug(reason)
            else:
                # TODO: Give a more accurate reason why the write to the ledger failed.
                status = "Error"
                statusCode = 500
                reason = "Attempted to get NYM identified by %s from the ledger to verify role %s was given. Did not find the NYM on the ledger." % (entry["DID"], entry["role"])
                logger.error(reason)
        else:
            # TODO: DID already exists on the ledger. A Steward cannot modify an
            #       existing identity.
            status = "Success"
            statusCode = 200
            reason = "NYM %s already exists on the ledger. Proceeding to transfer test tokens if payment address supplied" % entry["DID"]
            logger.debug(reason)
      #await writeEndorserRegistrationLog(entry, status, reason, isotimestamp)

      # Add status and reason for the status for each DID to the result
        result[entry["DID"]] = {
            'status': status,
            'statusCode': statusCode,
            'reason': reason
        }

        # Possible status codes: 200, 400, 500. From less severe 200 to most severe 500.
        # Return the overall status using the most severe status code.
        if statusCode > result['statusCode']:
            logger.debug("Status code >%d< is greater than result.statusCode >%d<", statusCode, result['statusCode'])
            result['statusCode'] = statusCode

    # Close wallets and pool
    logger.debug("Before close_wallet")
    await wallet.close_wallet(steward_wallet_handle)
    logger.debug("After close_wallet")
    logger.debug("Before close_pool_ledger")
    await pool.close_pool_ledger(pool_handle)
    logger.debug("After close_pool_ledger")

    return result 
#    logger.debug("Before set future result")
#    future.set_result(result)
#    logger.debug("After set future result")

async def getTokenSources(pool_handle, wallet_handle, steward_did, payment_address):
    payment_sources = {}
    logger.debug("Before build_get_payment_sources_request")
    get_payment_sources_req, payment_method = \
        await payment.build_get_payment_sources_request(wallet_handle, steward_did, payment_address)
    logger.debug("After build_get_payment_sources_request")

    logger.debug("Before submit_request")
    get_payment_sources_resp = await ledger.submit_request(pool_handle, get_payment_sources_req)
    logger.debug("After submit_request")
    logger.debug("submit_request JSON response >%s<", get_payment_sources_resp)
    sources_resp_dict=json.loads(get_payment_sources_resp)
    print("Gothere1")
    print(sources_resp_dict['op'])
    print("Gothere1.1")

    if sources_resp_dict['op'] == "REQNACK":
        print("Gothere2")
        logger.debug("Invalid Payment Source - Received REQNACK from get_payment_sources")
        return None
    else:
        print("Gothere3")
        logger.debug("Before parse_get_payment_sources_response")
        parse_get_payment_sources_resp = await payment.parse_get_payment_sources_response(payment_method,
                                                                              get_payment_sources_resp)
        logger.debug("After parse_get_payment_sources_resp")
        logger.debug("parse_get_payment_sources_response Sources JSON >%s<", parse_get_payment_sources_resp)

    payment_sources = json.loads(parse_get_payment_sources_resp)
    return payment_sources

def getSufficientTokenSources(token_sources, target_tokens_amount):
    sources_amount = 0
    sources = []

    for source in token_sources:
        sources_amount += source['amount']
        sources.append(source['source'])
        if sources_amount >= target_tokens_amount:
            break

    remaining_tokens_amount = sources_amount - target_tokens_amount

    return sources, remaining_tokens_amount

async def createPaymentAddess(wallet_handle, address_seed):
    logger.debug("Before create and store source payment address")
    payment_address_config = {'seed': address_seed}
    source_payment_address = await payment.create_payment_address(wallet_handle, PAYMENT_METHOD,
                                                                json.dumps(payment_address_config))
    logger.debug("After create and store source payment address")
    return source_payment_address

async def transferTokens(pool_handle, wallet_handle, steward_did, source_payment_address, target_payment_address,
                         target_tokens_amount):
    logger.debug("Before getting all token sources")
    token_sources = await getTokenSources(pool_handle, wallet_handle, steward_did, source_payment_address)
    print(token_sources)
    if len(token_sources) == 0:
        print("Gothere4")
        err = Exception("No token sources found for source payment address %s" % source_payment_address)
        err.status_code = 400
        logging.error(err)
        raise err
    logger.debug("After getting all token sources")

    target_tokens_amount = target_tokens_amount or DEFAULT_TOKENS_AMOUNT
    logger.debug("Tokens amount to transfer >%s<", target_tokens_amount)

    logger.debug("Before getting necessary token sources")
    token_sources, remaining_tokens_amount = getSufficientTokenSources(token_sources, target_tokens_amount)
    logger.debug("After getting necessary token sources")

    logger.debug("Token sources %s", token_sources)
    logger.debug("Remaining tokens amount %s", remaining_tokens_amount)

    logger.debug("Before build_payment_req")

    inputs = token_sources
    outputs = [
        {"recipient": target_payment_address, "amount": target_tokens_amount},
        {"recipient": source_payment_address, "amount": remaining_tokens_amount}
    ]
    #extras={'taaAcceptance': {'taaDigest': e1135b9882119714728457e520bff94942359295cd06ba5caed9286bda565f4a,'mechanism': 'service_agreement','time': 1568937395}}
    payment_req, payment_method = await payment.build_payment_req(wallet_handle, steward_did,
                                                                json.dumps(inputs), json.dumps(outputs), None)
    logger.debug("Before TAA")
#    taa_req = await ledger.build_get_txn_author_agreement_request()
#    print(taa_req)
#    taa_resp = await ledger.submit_request(pool_handle, wallet_handle, steward_did, taa_req)
#    print(taa_resp)
#    if taa_resp:
    if 1:
        
        print("Gothere7")
        #time=datetime.datetime.now().utcformat()
        #payment_req = await ledger.append_txn_author_agreement_acceptance_to_request(payment_req, text, '1', None, 'service_agreement', 1568937395)
        #payment_req = await ledger.append_txn_author_agreement_acceptance_to_request(payment_req, None, None, '022bbdd0e22b2ae83498304cd8fe2ba3e33d828f0fe6614ffcbfdcb46c5fd2a7', 'service_agreement', 1568937395)
        payment_req = await ledger.append_txn_author_agreement_acceptance_to_request(payment_req, None, None, 'db6810310ea1bfc740f6eeade1bb65c26ac9627dda9023328d84117066f39495', 'service_agreement', 1568937395)
        #payment_req = await ledger.AppendTxnAuthorAgreementAcceptanceToRequest(payment_req, None, None, 'e1135b9882119714728457e520bff94942359295cd06ba5caed9286bda565f4a', 'service_agreement', 1568937395)
    print("Gothere8")
    logger.debug("Payment request >%s<", payment_req)
    logger.debug("After build_payment_req")

    logger.debug("Before sign_and_submit_request")
    payment_resp = await ledger.sign_and_submit_request(pool_handle, wallet_handle, steward_did, payment_req)
    logger.debug("After sign_and_submit_request")
    logger.debug("sign_and_submit_request JSON response >%s<", payment_resp)

    logger.debug("Before parse_payment_response")
    receipts = await payment.parse_payment_response(payment_method, payment_resp)
    logger.debug("After get_payment_sources_resp")
    logger.debug("parse_payment_response Receipts JSON >%s<", receipts)

    receipts = json.loads(receipts)

    if len(receipts) != 2:
        err = Exception(
            "Failed to transfer %s tokens to %s payment address. Wrong number of receipts has been created: %s." % (
            target_tokens_amount, target_payment_address, receipts))
        err.status_code = 500
        raise err

async def xferTokens(network, NYMs):
# A dict to hold the results keyed on DID
    logger.debug("Begin xferTokens Function")
    result = {
        "statusCode": 200
    }

    status = "Pending"
    statusCode = 200

    steward_did = StewardDID
    # Open pool ledger
    pool_name = network
    await pool.set_protocol_version(2)
 
    logger.debug("Before open pool ledger %s.", pool_name)
    pool_handle = await pool.open_pool_ledger(pool_name, None)
    logger.debug("After open pool ledger %s.", pool_name)

    # Open Wallet and Get Wallet Handle
    logger.debug("Before open steward_wallet")
    wallet_name = Wallet
    wallet_config = json.dumps({"id": wallet_name})
    wallet_credentials = json.dumps({"key": WalletKey})
    steward_wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)

    isotimestamp = datetime.datetime.now().isoformat()

    try:
        entry=NYMs[0] #I expect that there will only ever be 1 entry in NYMs because I only expect this to ever be called from the Browser.
        print(entry)
        if entry.get('paymentaddr'):
            reason = "Check if Payment Address already contains tokens."

            # Log that a check for target payment address on STN is in progress.
            logger.debug("Before write Endorser registration log")
            await writeEndorserRegistrationLog(entry, status, reason, isotimestamp)
            logger.debug("After write Endorser registration log")

            #This should already be loaded on the server..
            loadPaymentLibrary()

            # Verify target Payment Address and that address does not contain tokens exceeding the maximum token amount
            await validateTargetPaymentAddress(pool_handle, steward_wallet_handle, steward_did,
                                           entry.get('paymentaddr'), DEFAULT_TOKENS_AMOUNT) #entry.get('tokensAmount'))

            reason = "Payment Address does not contain tokens. Transferring tokens is allowed."
            # Log that a check for target payment address on STN is in done.
            logger.debug("Before write Endorser registration log")
            await writeEndorserRegistrationLog(entry, status, reason, isotimestamp)
            logger.debug("After write Endorser registration log")

            reason = "Check if Source Payment Address contains enough tokens for transferring."

            # Log that a check for source payment address on STN is in progress.
            logger.debug("Before write Endorser registration log")
            await writeEndorserRegistrationLog(entry, status, reason, isotimestamp)
            logger.debug("After write Endorser registration log")

            # Verify source Payment Address contains enough tokens
            if pool_name == "buildernet":
                source_payment_address=BuilderPaymentAddress 
            elif pool_name == "stagingnet":
                source_payment_address=StagingPaymentAddress
            else:   # Testing
                source_payment_address=TrainingPaymentAddress 
            await validateSourcePaymentAddress(pool_handle, steward_wallet_handle, steward_did,
                                           source_payment_address, DEFAULT_TOKENS_AMOUNT) #entry.get('tokensAmount'))

            reason = "Source Payment Address contains enough tokens. Transferring is allowed."
            # Log that a check for source payment address on STN is in done.
            logger.debug("Before write Endorser registration log")
            await writeEndorserRegistrationLog(entry, status, reason, isotimestamp)
            logger.debug("After write Endorser registration log")

            # Transfer tokens to DID specified payment the address
            status = "Pending"
            reason_inner = "Transfer tokens to payment address."

            logger.debug("Before write token transferring log")
            await writeEndorserRegistrationLog(entry, status, reason_inner, isotimestamp)
            logger.debug("After write token transferring log")

            target_payment_address = entry['paymentaddr']
            target_tokens_amount = DEFAULT_TOKENS_AMOUNT #entry.get('tokensAmount')

            await transferTokens(pool_handle, steward_wallet_handle, steward_did, source_payment_address,
                             target_payment_address, target_tokens_amount)

            status = "Success"
            reason_inner = "Successfully transferred %s Sovatoms to %s payment address" % (
                  target_tokens_amount, target_payment_address)
            logger.debug(reason_inner)

            logger.debug("Before write token transferring log")
            await writeEndorserRegistrationLog(entry, status, reason_inner, isotimestamp)
            logger.debug("After write token transferring log")

            reason += '\n' + reason_inner
        else:
            return
    except Exception as err:
        status = "Error"
        statusCode = err.status_code
        reason = str(err)
        logger.error(err)

    await writeEndorserRegistrationLog(entry, status, reason, isotimestamp)

    # Close wallets and pool
    logger.debug("Before close_wallet")
    await wallet.close_wallet(steward_wallet_handle)
    logger.debug("After close_wallet")
    logger.debug("Before close_pool_ledger")
    await pool.close_pool_ledger(pool_handle)
    logger.debug("After close_pool_ledger")

    # Add status and reason for the status for each DID to the result
    result[entry["DID"]] = {
      'status': status,
      'statusCode': statusCode,
      'reason': reason
    }

    # Possible status codes: 200, 400, 500. From less severe 200 to most severe 500.
    # Return the overall status using the most severe status code.
    if statusCode > result['statusCode']:
        logger.debug("Status code >%d< is greater than result.statusCode >%d<", statusCode, result['statusCode'])
        result['statusCode'] = statusCode
    return result

def isPaymentAddress(payment_address: str):
    logger.debug("Validating payment address %s" % payment_address)
    payment_address = payment_address[8:] if payment_address.startswith(PAYMENT_PREFIX) else payment_address

    if not isb58ofLength(payment_address, 36):
        return "Unqualified payment address %s is not a 32 byte base58 encoded string." % payment_address

async def validateSourcePaymentAddress(pool_handle, wallet_handle, steward_did, source_payment_address,
                                       target_tokens_amount):
    logger.debug("Check for existence of token sources")
    token_sources = await getTokenSources(pool_handle, wallet_handle, steward_did, source_payment_address)

    if len(token_sources) == 0:
        err = Exception("No token sources found for source payment address %s" % source_payment_address)
        err.status_code = 400
        logging.error(err)
        raise err

    target_tokens_amount = target_tokens_amount or DEFAULT_TOKENS_AMOUNT
    logger.debug("Tokens amount to transfer >%s<", target_tokens_amount)

    if sum(source['amount'] for source in token_sources) < target_tokens_amount:
        err = Exception("Not enough payment sources found to transfer %s tokens" % target_tokens_amount)
        err.status_code = 400
        logging.error(err)
        raise err

async def validateTargetPaymentAddress(pool_handle, wallet_handle, steward_did, target_payment_address, target_tokens_amount):
    logger.debug("Check for valid target payment address")
    isvalid=isPaymentAddress(target_payment_address)
    print(isvalid)
    if isvalid is not None:
        err = Exception(isvalid)
        err.status_code = 409
        logging.error(err)
        raise err

    logger.debug("Check for non existence of token sources for target payment address")
    target_payment_sources = await getTokenSources(pool_handle, wallet_handle, steward_did, target_payment_address)
    if target_payment_sources is None:
        err = Exception("Invalid Payment Source")
        err.status_code = 409
        logging.error(err)
        raise err

    target_tokens_amount = target_tokens_amount or DEFAULT_TOKENS_AMOUNT

    token_amount=sum(source['amount'] for source in target_payment_sources)
    if token_amount > target_tokens_amount:
        err = Exception(
            "Target payment address %s already contains %s tokens. No more tokens allowed for this address" % (
            target_payment_address, token_amount))
        err.status_code = 409
        logging.error(err)
        raise err

def isb58ofLength(value, length):
    try:
        if len(base58.b58decode(value)) != length:
            logger.debug("%s base58 decoded is not the required length of %d bytes." % (value, length))
            return False
    except Exception as e:
        logging.exception("Failed to decode %s" % value)
        return False

    return True

def isValidDID(did):
    return isb58ofLength(did, 16)

def isValidFullVerkey(did, verkey):
    logger.debug("Validating full verkey %s with DID %s" % (verkey, did))
    if isb58ofLength(verkey, 32):
        decodedValue = base58.b58decode(verkey)
        logger.debug("Full verkey %s is the following 32 byte base58 encoded string: %s" % (verkey, decodedValue))
        decodedDIDValue = base58.b58decode(did)
        logger.debug("Full verkey %s is the following 32 byte base58 encoded string: %s" % (verkey, decodedValue))
        if decodedValue[0:16] == decodedDIDValue:
            logger.debug("The first 16 bytes of %s are the DID %s" % (decodedValue, decodedDIDValue))
            return True
        else:
            logger.debug("The first 16 bytes of %s are NOT the DID %s" % (decodedValue, decodedDIDValue))
    else:
        logger.debug("Full verkey %s is not a 32 byte base58 encoded string." % verkey)

    return False

def isValidAbbreviatedVerkey(verkey):
    # Are we validating an abbreviated verkey?
    if len(verkey) > 0 and verkey[0] == '~':
        # Abbreviated verkey
        return isb58ofLength(verkey[1:], 16)
    return False

def validateVerkey(did, verkey):
    if len(verkey) > 1:
        if verkey[0] == '~':
           if not isValidAbbreviatedVerkey(verkey):
               return "Abbreviated verkey %s must be a 16 byte base58 encoded string." % verkey
        else:
           if not isValidFullVerkey(did, verkey):
               return "Full verkey %s must be a 32 byte base58 encoded string." % verkey
    else:
        return "A verkey must be either a 16 byte base58 encoded string that begins with a tilde (a.k.a. abbreviated verkey), or a 32 byte base58 encoded string."

#def isValidEmail(email):
#    if len(email) > 7:
#        if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) != None:
#            return True
#    return False

def validateNym(nym):
    # Validate entry
    #
    # Must contain DID, verkey, and  optional paymentaddr. All other fields are added by
    # the lambda(unless this is the version where lambdas are not used).
    errors = []
    if 'did' in nym:
        # Validate DID
        if not isValidDID(nym['did']):
            errors.append("DID %s must be a 16 byte base58 encoded string." % nym['did'])
    else:
        # When a request comes from API Gateway, this is unreachable code
        errors.append("A DID is required to create an identity on the ledger.")

    if 'verkey' in nym:
        did = nym['did'] if 'did' in nym else None
        verkey = nym['verkey']
        # Validate verkey
        error = validateVerkey(did, verkey)
        if error:
            errors.append(error)
    else:
        # When a request comes from API Gateway, this is unreachable code
        errors.append("An abbreviated or full verkey is required to create an identity on the ledger.")

    return errors

def endorserNym(request): #, event):
    return {
        "DID": request['did'],
        "verkey": request['verkey'],
        "role": "ENDORSER",
        "name": request['name'] if 'name' in request else " ",
        #"sourceIP": event['requestContext']['identity']['sourceIp'],
        "sourceIP": "UNKNOWN",
        "paymentaddr": request['paymentaddr']
    }

def addErrors(did, errorsDict, errors):
    currentErrors = []

    # Do errors already exists keyed on did?
    if did in errorsDict:
        currentErrors = errorsDict[did]

    currentErrors.extend(errors)
    errorsDict[did] = currentErrors

    return errorsDict

EXTENSION = {"darwin": ".dylib", "linux": ".so", "win32": ".dll", 'windows': '.dll'}

def file_ext():
  your_platform = platform.system().lower()
  return EXTENSION[your_platform] if (your_platform in EXTENSION) else '.so'

def loadPaymentLibrary():
  if not hasattr(loadPaymentLibrary, "loaded"):
    try:
      logger.debug("Before loading payment library")

      payment_plugin = cdll.LoadLibrary(PAYMENT_LIBRARY + file_ext())
      payment_plugin.sovtoken_init()
      loadPaymentLibrary.loaded = True

      logger.debug("After loading payment library")
    except Exception:
      err = Exception("Payment library %s could not found." % (PAYMENT_LIBRARY + file_ext()))
      err.status_code = 404
      logging.error(err)
      raise err

def my_handler(event, context):
    # Local file system access, child processes, and similar artifacts may not
    # extend beyond the lifetime of the request, and any persistent state should
    # be stored in Amazon S3, Amazon DynamoDB, or another Internet-available
    # storage service. Lambda functions can include libraries, even native ones.
    # Each Lambda function receives 500MB of non-persistent disk space in its
    # own /tmp directory.

    logging.debug("In my_handler")
    responseCode = 200

    os.environ['HOME'] = tempfile.gettempdir()
    os.environ['RUST_LOG'] = 'trace'

    lambdaTaskRoot = os.environ['LAMBDA_TASK_ROOT']
    stewardSeed = os.environ['STEWARD_SEED']

    ## TODO: Lock the handler down to just POST requests?
    #if event['httpMethod'] != 'POST':
    #    # Return unsupported method error/exception

    nyms = []
    # TODO: Change the default for 'name' from " " to None once
    #       ledger.build_nym_request accepts None
    logging.debug("Event body >%s<" % event['body'])
    body = json.loads(event['body'])

    # Validate and build nyms from request body; setting name and sourceIP for
    # each nym.
    # TODO: Currently a non-empty 'name' is required. Set the default to None
    #       once ledger.build_nym_request accepts None for the NYM 'name/alias'
    # NOTE: errors is a dict keyed on the DID. This Lambda is fronted by AWS
    #       API Gateway with JSON Schema validation that ensures we will never
    #       reach this point without a DID for each NYM in the request body.
    errors = {}
    if 'batch' in body:
        logging.debug("Processing batch request...")
        for nym in body['batch']:
            did = nym['did']
            tmp_errors = validateNym(nym)
            if len(tmp_errors) == 0:
                nyms.append(endorserNym(nym, event))
            else:
                errors = addErrors(did, errors, tmp_errors)
    else:
        logging.debug("Processing single (non-batch) request...")
        did = body['did']
        tmp_errors = validateNym(body)
        if len(tmp_errors) == 0:
            nyms.append(endorserNym(body, event))
        else:
            errors = addErrors(did, errors, tmp_errors)

    # Check if errors is an empty dict
    if bool(errors) == False:
        logging.debug("No errors found in request...")
        # Get the steward seed and pool genesis file
        config = configparser.ConfigParser()
        try:
            configFile = os.path.join(lambdaTaskRoot, "nym.ini")
            config.read_file(open(configFile))
            #stewardSeed = config['steward']['Seed']
            genesisFile = os.path.join(lambdaTaskRoot, config['pool']['GenesisFile'])
        except FileNotFoundError as exc:
            raise Exception("Service configuration error. Configuration file {} not found".format(str(configFile)))
        except KeyError as exc:
            raise Exception("Service configuration error. Key {} not found.".format(str(exc)))

        poolName = genesisFile.split("_")[-2]

        logging.debug("Get asyncio event loop...")
        loop = asyncio.get_event_loop()
        # Pass the 'future' handle to addNYMs to allow addNYMs to set the
        # future's 'result'.
        logging.debug("Get future handle...")
        future = asyncio.Future()
        logging.debug("Call addNYMs...")
        asyncio.ensure_future(addNYMs(future, poolName, genesisFile, stewardSeed, nyms))
        logging.debug("Wait for future to complete...")
        loop.run_until_complete(future)
        logging.debug("Future is complete...")

        responseBody = future.result()
    else:
        logging.debug("Errors found in request...")
        # Return validation errors. Validation errors are keyed on DID. Just add
        # a statusCode of 400 and set responseBody to the errors dict.
        errors['statusCode'] = 400
        responseBody = errors

    responseCode = responseBody['statusCode']

    # The output from a Lambda proxy integration must be of the following JSON
    # object. The 'body' property must be a JSON string. For base64-encoded
    # payload, you must also set the 'isBase64Encoded' property to 'true'.
    response = {
        'statusCode': responseCode,
        'headers': {
            'Access-Control-Allow-Origin':'*'
        },
        'body': json.dumps(responseBody)
    }
    logging.debug("response: %s" % json.dumps(response))
    return response

async def handle_nym_req(request):
    responseCode = 200
    responseBody={}
    tmp_errors=[]

    nyms = []
    #logging.debug("Event body >%s<" % event['body'])
    msgbody = await request.json() #written by dbluhm (not copied)

    # Validate and build nyms from request body; setting name and sourceIP for
    # each nym.

    response = {
        'statusCode': responseCode,
        'headers': {
            'Access-Control-Allow-Origin':'*'
        },
        'body': json.dumps(responseBody)
    }

    errors = {}
    logger.debug("Processing single (non-batch) request...")
    if (msgbody['did'] == "") and (msgbody['verkey'] == "") and (msgbody['paymentaddr'] == ""):
        return web.Response(body=json.dumps(response))   
    if msgbody['did'] or msgbody['verkey']:
        did = msgbody['did']
        tmp_errors = validateNym(msgbody)
    if len(tmp_errors) == 0:
        nyms.append(endorserNym(msgbody)) #, event)) @@@Remove event from this function call? (might mess up Main)
    else:
        errors = addErrors(did, errors, tmp_errors)

    # Check if errors is an empty dict
    if bool(errors) == False:
        #print("Got here 1\n")
        logger.debug("No errors found in request...")
        # Get the steward seed and pool genesis file

        poolName = msgbody['network'] 

        if nyms[0]['DID'] and nyms[0]['verkey']:
            logger.debug("Call addNYMs...")
            responseBody = await addNYMs(poolName, nyms)
            logger.debug("Adding nym is complete...")
        if nyms[0]['paymentaddr']:
            logger.debug("Call xferTokens...")
            #TODO need to append to responsebody here rather than overwriting it
            responseBody = await xferTokens(poolName, nyms)
            logger.debug("Xfer Tokens is complete...")
        else:
            print("The payment address was blank, did not try to transfer tokens this time.")
            #Add appropriate messaging to error handling stuff?  Its okay if this is  blank and all they wanted was nore a nym, so this is not an error 

    else:
        #print("Got here 2\n")
        logger.debug("Errors found in request...")
        # Return validation errors. Validation errors are keyed on DID. Just add
        # a statusCode of 400 and set responseBody to the errors dict.
        errors['statusCode'] = 400
        responseBody = errors

    #print(responseBody)
    if responseBody:
        responseCode = responseBody['statusCode']
    else:
        responseCode = 0

    response = {
        'statusCode': responseCode,
        'headers': {
            'Access-Control-Allow-Origin':'*'
        },
        'body': json.dumps(responseBody)
    }
    logger.debug("response: %s" % json.dumps(response))
    return web.Response(body=json.dumps(response))

#    return web.Response(body=json.dumps(msgbody)) #Written by dbluhm


# --------- Main -----------
def main():
    # TODO: make DID and verkey optional if a --csv is given.
    #       The csv file would take the form: "<DID>,<verkey>\n"
    parser = argparse.ArgumentParser()
    parser.add_argument('genesisFile', action="store")
    parser.add_argument('DID', action="store")
    parser.add_argument('verkey', action="store")
    parser.add_argument('stewardSeed', action="store")
    parser.add_argument('--role', action="store", dest="role", default=None,
        choices=["STEWARD", "TRUSTEE", "ENDORSER"],
        help="Assumed to be an Identity Owner (role=None) if not provided")
    parser.add_argument('--name', action="store", dest="name", default=None,
        help="A name/alias of the NYM")
    parser.add_argument('--source-ip', action="store", dest="sourceIP",
        default='128.0.0.1',
        help="The source IP address of the client requesting the NYM.")
    parser.add_argument('--payment-address', action="store", dest="paymentaddr",
        help="The Endorser's email address.")
    args = parser.parse_args()
  
    # TODO: Add the logic to either add a single record or many from a CSV file.
    nyms = []
  
    # Validate and build nyms from request body; setting name and sourceIP for
    # each nym.
    # TODO: Currently a non-empty 'name' is required. Set the default to None
    #       once ledger.build_nym_request accepts None for the NYM 'name/alias'
    errors = {}
  
    # Mock a body from the client
    body = {
        "did": args.DID,
        "verkey": args.verkey,
        "name": args.name,
        "paymentaddr": args.paymentaddr
    }
  
    # Mock an event from the AWS API Gateway
    event = {
        "requestContext": {
            "identity": {
                "sourceIp": "127.0.0.1"
            }
        }
    }

    tmp_errors = validateNym(body)
    if len(tmp_errors) == 0:
        nyms.append(endorserNym(body, event))
    else:
        errors = addErrors(args.DID, errors, tmp_errors)
  
    if bool(errors) == False:
        poolName = args.genesisFile.split("_")[-2]
  
        loop = asyncio.get_event_loop()
        # Pass the 'future' handle to addNYMs to allow addNYMs to set the future's
        # 'result'.
        future = asyncio.Future()
        asyncio.ensure_future(addNYMs(future, poolName, args.genesisFile,
          args.stewardSeed, nyms))
        loop.run_until_complete(future)
        loop.close()
  
        responseBody = future.result()
    else:
        # Return validation errors
        errors['statusCode'] = 400
        responseBody = errors
  
    responseCode = responseBody['statusCode']
  
    # The output from a Lambda proxy integration must be
    # of the following JSON object. The 'headers' property
    # is for custom response headers in addition to standard
    # ones. The 'body' property  must be a JSON string. For
    # base64-encoded payload, you must also set the 'isBase64Encoded'
    # property to 'true'.
    response = {
        'statusCode': responseCode,
        'headers': {
            'Access-Control-Allow-Origin':'*'
        },
        'body': json.dumps(responseBody)
    }
    logging.debug("response: %s" % json.dumps(response))
    print("%s" % json.dumps(response))
  
    if responseCode != 200:
       sys.exit(1)
    else:
       sys.exit(0)


if __name__ == "__main__":
        main()

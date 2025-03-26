from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from web3 import Web3
import json
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
account = os.getenv("ACCOUNT_ADDRESS")
PRIVATE_KEY = "0xf305aa0d2ae3c41a7c291a50e077402c59583e922a3662e78c629a5f825ded95"
CHAIN_ID = int(os.getenv("CHAIN_ID"))

# Load ABIs & Contract Addresses
with open('./artifacts/contracts/RBAC.sol/RBAC.json') as f:
    rbac = json.load(f)
with open('./artifacts/contracts/ProductRegistry.sol/ProductRegistry.json') as f:
    product = json.load(f)
with open('./artifacts/contracts/TrialManager.sol/TrialManager.json') as f:
    trial = json.load(f)

RBAC_ADDRESS = "0xeD9D3CC8a062394BC3157b8ca7a76638A457Ce28"
PRODUCT_ADDRESS = "0x9793db790c286CF8AcA9d2B4295FDa0dEc1Af58F"
TRIAL_ADDRESS = "0xA6EC2E5ABE7604DdeDf1c43222806237748C3a2A"

rbac_contract = w3.eth.contract(address=RBAC_ADDRESS, abi=rbac['abi'])
product_contract = w3.eth.contract(address=PRODUCT_ADDRESS, abi=product['abi'])
trial_contract = w3.eth.contract(address=TRIAL_ADDRESS, abi=trial['abi'])


class RegisterUserSchema(BaseModel):
    name: str
    address: str
    wallet_address: str


class RequestRoleSchema(BaseModel):
    role: int
    user: str


class ApproveRoleSchema(BaseModel):
    user: str

@app.post("/api/v1/registerUser")
async def register_user(user_data: RegisterUserSchema):
    """ Registers a new user """
    try:
        logger.debug(f"Received Data: {user_data}")

        # Get the sender's nonce
        nonce = w3.eth.get_transaction_count(user_data.wallet_address)

        # Build transaction
        txn = rbac_contract.functions.registerUser(
            user_data.name, user_data.address
        ).build_transaction({
            'from': user_data.wallet_address,
            'gas': 2000000,
            'gasPrice': w3.to_wei('10', 'gwei'),
            'nonce': nonce
        })
        return {"message": "User registered"}
    
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/role/{user_address}")
async def get_user_role(user_address: str):
    """ Fetch user role """
    try:
        role = rbac_contract.functions.getUserRole(user_address).call()
        return {"user": user_address, "role": role}
    
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/login")
async def get_user_role(data: dict):
    """ Fetch user role via POST request """
    try:
        logger.debug(f"Received Data: {data}")
        user_address = data.get("user_address")

        if not user_address:
            raise HTTPException(status_code=400, detail="user_address is required")

        login = rbac_contract.functions.getUser(user_address).call()  # ✅ Fetch user role
        logger.info(f"User Details: {login}")  # ✅ Log details

        return {"user_address": user_address, "role": login,"success": True}
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/request-role")
async def request_role(data: RequestRoleSchema):
    """ Request a new role """
    try:
        nonce = w3.eth.get_transaction_count(data.user)
        
        txn = rbac_contract.functions.requestRole(data.role).build_transaction({
            'from': data.user,
            'gas': 2000000,
            'gasPrice': w3.to_wei('10', 'gwei'),
            'nonce': nonce
        })
        
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        return {"message": "Role requested", "tx_hash": tx_hash.hex(), "receipt": receipt}
    
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/approve-role")
async def approve_role(data: ApproveRoleSchema):
    """ Approve a role request """
    try:
        nonce = w3.eth.get_transaction_count(CONTRACT_ADDRESS)
        
        txn = rbac_contract.functions.approveRole(data.user).build_transaction({
            'from': CONTRACT_ADDRESS,
            'gas': 2000000,
            'gasPrice': w3.to_wei('10', 'gwei'),
            'nonce': nonce
        })
        
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        return {"message": f"Role approved for {data.user}", "tx_hash": tx_hash.hex(), "receipt": receipt}
    
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/role-request/{user_address}")
async def get_pending_request(user_address: str):
    """ Get pending role request """
    try:
        role_request = rbac_contract.functions.roleRequests(user_address).call()
        return {
            "user": user_address,
            "requestedRole": role_request[0],
            "isPending": role_request[1]
        }
    
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

### ------------------------- PRODUCT ROUTES ------------------------- ###

class RegisterProductSchema(BaseModel):
    productName: str
    user: str


@app.post("/api/v1/register")
async def register_product(data: RegisterProductSchema):
    try:
        nonce = w3.eth.get_transaction_count(account)
        txn = product_contract.functions.registerProduct(data.productName).build_transaction({
            'chainId': CHAIN_ID,
            'gas': 300000,
            'gasPrice': w3.to_wei('20', 'gwei'),
            'nonce': nonce,
            'from': data.user
        })
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"message": "Product registered", "tx_hash": tx_hash.hex()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/{product_id}")
async def get_product(product_id: int):
    try:
        product = product_contract.functions.getProduct(product_id).call()
        return {
            "productId": product_id,
            "productName": product[0],
            "company": product[1],
            "exists": product[2]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/{product_id}/exists")
async def check_product_exists(product_id: int):
    try:
        exists = product_contract.functions.productExists(product_id).call()
        return {"productId": product_id, "exists": exists}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/{product_id}/company")
async def get_product_company(product_id: int):
    try:
        company = product_contract.functions.getProductCompany(product_id).call()
        return {"productId": product_id, "company": company}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


### ------------------------- TRIAL ROUTES ------------------------- ###

class SubmitTrialSchema(BaseModel):
    productId: int
    patient: str
    trialName: str
    dataHash: str
    doctor: str

class ApproveTrialSchema(BaseModel):
    trialId: int
    admin: str


@app.post("/api/v1/submit")
async def submit_trial(data: SubmitTrialSchema):
    try:
        nonce = w3.eth.get_transaction_count(account)
        txn = trial_contract.functions.submitTrial(
            data.productId, data.patient, data.trialName, data.dataHash
        ).build_transaction({
            'chainId': CHAIN_ID,
            'gas': 400000,
            'gasPrice': w3.to_wei('20', 'gwei'),
            'nonce': nonce,
            'from': data.doctor
        })
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"message": "Trial submitted", "tx_hash": tx_hash.hex()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/approve")
async def approve_trial(data: ApproveTrialSchema):
    try:
        nonce = w3.eth.get_transaction_count(account)
        txn = trial_contract.functions.approveTrial(
            data.trialId
        ).build_transaction({
            'chainId': CHAIN_ID,
            'gas': 200000,
            'gasPrice': w3.to_wei('20', 'gwei'),
            'nonce': nonce,
            'from': data.admin
        })
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"message": "Trial approved", "tx_hash": tx_hash.hex()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/{trial_id}")
async def view_trial(trial_id: int):
    try:
        trial = trial_contract.functions.viewTrial(trial_id).call()
        return {
            "trialId": trial_id,
            "productId": trial[0],
            "trialName": trial[1],
            "dataHash": trial[2],
            "approved": trial[3],
            "doctor": trial[4],
            "patient": trial[5],
            "company": trial[6]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/patient")
async def view_my_trials(patient: str):
    try:
        trials = trial_contract.functions.viewMyTrials().call({'from': patient})
        return format_trials(trials)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/doctor")
async def view_doctor_trials(doctor: str):
    try:
        trials = trial_contract.functions.viewDoctorTrials().call({'from': doctor})
        return format_trials(trials)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/company")
async def view_company_trials(company: str):
    try:
        trials = trial_contract.functions.viewCompanyTrials().call({'from': company})
        return format_trials(trials)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def format_trials(trials):
    return [{
        "trialId": t[0],
        "productId": t[1],
        "trialName": t[2],
        "dataHash": t[3],
        "approved": t[4],
        "doctor": t[5],
        "patient": t[6],
        "company": t[7]
    } for t in trials]

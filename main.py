from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="PayShield Disputes", description="Chargeback and dispute management API for payments. Educational project.")

# Models
class Transaction(BaseModel):
    id: str
    customer_id: str
    amount: float
    currency: str
    timestamp: datetime
    merchant: Optional[str] = None
    status: str = "completed"

class ChargebackRequest(BaseModel):
    reason: str
    description: Optional[str] = None

class Evidence(BaseModel):
    type: str
    content: str

class EvidenceRequest(BaseModel):
    evidence: List[Evidence]

# In-memory storage
a_all_transactions = {}
chargebacks: dict[str, List[ChargebackRequest]] = {}
evidences: dict[str, List[Evidence]] = {}

@app.post("/transactions", response_model=Transaction)
def create_transaction(tx: Transaction):
    if tx.id in a_all_transactions:
        raise HTTPException(status_code=400, detail="Transaction already exists")
    a_all_transactions[tx.id] = tx
    return tx

@app.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: str):
    tx = a_all_transactions.get(transaction_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx

@app.get("/disputes/{transaction_id}/chargebacks", response_model=List[ChargebackRequest])
def get_chargeback_history(transaction_id: str):
    return chargebacks.get(transaction_id, [])

@app.post("/disputes/{transaction_id}/chargebacks")
def file_chargeback(transaction_id: str, cb: ChargebackRequest):
    if transaction_id not in a_all_transactions:
        raise HTTPException(status_code=404, detail="Transaction not found")
    history = chargebacks.setdefault(transaction_id, [])
    history.append(cb)
    return {"message": "Chargeback filed", "count": len(history)}

@app.get("/disputes/{transaction_id}/evidence", response_model=List[Evidence])
def get_evidence(transaction_id: str):
    return evidences.get(transaction_id, [])

@app.post("/disputes/{transaction_id}/evidence")
def add_evidence(transaction_id: str, request: EvidenceRequest):
    if transaction_id not in a_all_transactions:
        raise HTTPException(status_code=404, detail="Transaction not found")
    existing = evidences.setdefault(transaction_id, [])
    existing.extend(request.evidence)
    return {"message": "Evidence added", "count": len(existing)}

# Simple risk scoring

def calculate_score(tx: Transaction) -> int:
    score = 0
    if tx.amount > 1000:
        score += 30
    hour = tx.timestamp.hour
    if hour < 6 or hour > 22:
        score += 20
    # Count chargebacks for same customer
    count_cb = 0
    for t_id, cbs in chargebacks.items():
        existing_tx = a_all_transactions.get(t_id)
        if existing_tx and existing_tx.customer_id == tx.customer_id:
            count_cb += len(cbs)
    score += min(count_cb * 10, 30)
    return min(score, 100)

@app.get("/disputes/{transaction_id}/score")
def get_risk_score(transaction_id: str):
    tx = a_all_transactions.get(transaction_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    score = calculate_score(tx)
    decision = "APPROVE"
    if score >= 70:
        decision = "DECLINE"
    elif score >= 40:
        decision = "REVIEW"
    return {"transaction_id": transaction_id, "risk_score": score, "decision": decision}

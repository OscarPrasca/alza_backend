from sqlalchemy.orm import Session
from app.models.wallet_model import Wallet
from app.serializers.wallet_serializer import WalletCreateSerializer, WalletUpdateSerializer
from app.permissions.ownership import check_ownership
from app.utils.exceptions import not_found_exception

def get_all_wallets(db: Session, user_id: str):
    return db.query(Wallet).filter(Wallet.user_id == user_id).all()

def get_wallet_by_id(db: Session, wallet_id: str, user_id: str):
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        not_found_exception("Wallet")
    check_ownership(wallet.user_id, user_id)
    return wallet

def create_wallet(db: Session, data: WalletCreateSerializer, user_id: str):
    wallet = Wallet(
        user_id=user_id,
        name=data.name,
        balance=data.balance
    )
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet

def update_wallet(db: Session, wallet_id: str, data: WalletUpdateSerializer, user_id: str):
    wallet = get_wallet_by_id(db, wallet_id, user_id)
    if data.name is not None:
        wallet.name = data.name
    if data.balance is not None:
        wallet.balance = data.balance
    db.commit()
    db.refresh(wallet)
    return wallet

def delete_wallet(db: Session, wallet_id: str, user_id: str):
    wallet = get_wallet_by_id(db, wallet_id, user_id)
    db.delete(wallet)
    db.commit()
    return True
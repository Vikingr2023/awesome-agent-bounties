import pytest
from utxo_db import UTXO_DB, Transaction, UTXO

def test_double_spend():
    db = UTXO_DB()
    utxo = UTXO(amount=100)
    db.add_utxo(utxo)

    tx1 = Transaction(inputs=[utxo], outputs=[UTXO(amount=50), UTXO(amount=50)])
    db.apply_transaction(tx1)

    with pytest.raises(ValueError, match="Double-spending detected"):
        tx2 = Transaction(inputs=[utxo], outputs=[UTXO(amount=50)])
        db.apply_transaction(tx2)

def test_fund_creation_from_nothing():
    db = UTXO_DB()
    utxo = UTXO(amount=100)
    db.add_utxo(utxo)

    with pytest.raises(ValueError, match="Transaction invalid: Output amount exceeds input amount"):
        tx = Transaction(inputs=[utxo], outputs=[UTXO(amount=150)])
        db.apply_transaction(tx)
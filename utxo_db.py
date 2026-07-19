def apply_transaction(self, transaction):
    # Check if any of the inputs have already been spent
    for input_utxo in transaction.inputs:
        if self.is_spent(input_utxo):
            raise ValueError("Double-spending detected: UTXO already spent")

    # Check if the sum of outputs exceeds the sum of inputs
    total_input = sum(input_utxo.amount for input_utxo in transaction.inputs)
    total_output = sum(output.amount for output in transaction.outputs)
    if total_output > total_input:
        raise ValueError("Transaction invalid: Output amount exceeds input amount")

    # Existing code to process the transaction
    #...

    # Mark the UTXOs as spent
    for input_utxo in transaction.inputs:
        self.mark_spent(input_utxo)

def is_spent(self, utxo):
    return utxo in self.spent_utxos

def mark_spent(self, utxo):
    self.spent_utxos.add(utxo)
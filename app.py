# app.py
import os
from flask import Flask, request, jsonify

app = Flask(__name__, static_folder='.', static_url_path='')

# Import your blockchain (adjust the import based on your file structure)
try:
    from blockchain import Blockchain, Transaction
    blockchain = Blockchain()
except ImportError:
    print("WARNING: Could not import blockchain. Using mock data.")
    blockchain = None

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/chain")
def get_chain():
    if blockchain is None:
        # Mock data for testing
        return jsonify([{
            "index": 0,
            "timestamp": 0,
            "transactions": [],
            "hash": "0",
            "previous_hash": "0",
            "nonce": 0
        }])
    
    return jsonify(blockchain.get_chain_data())

@app.route("/pending")
def get_pending():
    if blockchain is None:
        return jsonify([])
    
    return jsonify([{
        "from_address": tx.from_address,
        "to_address": tx.to_address,
        "amount": tx.amount
    } for tx in blockchain.pending_transactions])

@app.route("/transaction", methods=["POST"])
def add_transaction():
    if blockchain is None:
        return jsonify({"success": False, "error": "Blockchain not initialized"})
    
    data = request.json
    tx = Transaction(
        from_address=data["from"],
        to_address=data["to"],
        amount=data["amount"]
    )
    blockchain.add_transaction(tx)
    return jsonify({"success": True})

@app.route("/mine", methods=["POST"])
def mine():
    if blockchain is None:
        return jsonify({"success": False, "message": "Blockchain not initialized"})
    
    if not blockchain.pending_transactions:
        return jsonify({"success": False, "message": "No transactions to mine"})
    
    block = blockchain.mine_pending()
    return jsonify({
        "success": True,
        "message": "Block mined!",
        "block": {
            "index": block.index,
            "hash": block.hash,
            "previous_hash": block.previous_hash
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n🚀 Starting Flask server on http://localhost:{port}")
    print(f"📊 Open http://localhost:{port} in your browser\n")
    app.run(host="0.0.0.0", port=port, debug=True)

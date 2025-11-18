# app.py
import os
from flask import Flask, render_template, request, jsonify
from blockchain import blockchain, Transaction

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chain")
def get_chain():
    return jsonify(blockchain.get_chain_data())

@app.route("/pending")
def get_pending():
    return jsonify([{
        "from_address": tx.from_address,
        "to_address": tx.to_address,
        "amount": tx.amount
    } for tx in blockchain.pending_transactions])

@app.route("/transaction", methods=["POST"])
def add_transaction():
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
    app.run(host="0.0.0.0", port=5000, debug=True)
else:
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

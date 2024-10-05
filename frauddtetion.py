import heapq
import time
from collections import deque

# Global data structures
user_transactions = {}          # Stores transaction history per user
recent_transactions = deque()    # Sliding window for recent transactions (24-hour window)
suspicious_transactions = []     # Priority queue for suspicious transactions
transaction_graph = {}           # Graph representing user transactions

# Function to add a transaction to the user's transaction history
def add_transaction(user_id, amount, location, timestamp):
    if user_id not in user_transactions:
        user_transactions[user_id] = []
    user_transactions[user_id].append({
        'amount': amount,
        'location': location,
        'timestamp': timestamp
    })

# Function to add a transaction to the sliding window (last 24 hours)
def add_recent_transaction(user_id, amount, location):
    current_time = time.time()
    recent_transactions.append({
        'user_id': user_id,
        'amount': amount,
        'location': location,
        'timestamp': current_time
    })

    # Remove old transactions (older than 24 hours)
    while recent_transactions and (current_time - recent_transactions[0]['timestamp']) > 86400:
        recent_transactions.popleft()

# Function to add a transaction to the priority queue based on risk score
def add_suspicious_transaction(user_id, amount, risk_score):
    heapq.heappush(suspicious_transactions, (-risk_score, user_id, amount))

# Function to get the highest priority suspicious transaction
def get_most_suspicious_transaction():
    return heapq.heappop(suspicious_transactions)

# Function to add a transaction to the transaction graph
def add_transaction_to_graph(sender_id, receiver_id):
    if sender_id not in transaction_graph:
        transaction_graph[sender_id] = set()
    if receiver_id not in transaction_graph:
        transaction_graph[receiver_id] = set()
    
    transaction_graph[sender_id].add(receiver_id)
    transaction_graph[receiver_id].add(sender_id)

# Function to check if a transaction is suspicious based on thresholds
def is_suspicious_transaction(transaction, threshold_amount=10000, unusual_location=''):
    if transaction['amount'] > threshold_amount:
        return True
    if unusual_location and transaction['location'] != unusual_location:
        return True
    return False

# Function to detect anomalies in user transactions
def detect_anomaly(transaction, user_id):
    history = user_transactions.get(user_id, [])
    if history:
        average_spent = sum([t['amount'] for t in history]) / len(history)
        if transaction['amount'] > 2 * average_spent:
            return True
    return False

# Function to check for frequent transactions in a sliding window (within 24 hours)
def check_frequent_transactions_in_window(user_id):
    count = sum(1 for t in recent_transactions if t['user_id'] == user_id)
    if count > 5:  # Threshold for too many transactions in a short time
        return True
    return False

# Example flow of processing a new transaction
def process_transaction(user_id, amount, location, receiver_id):
    current_time = time.time()
    transaction = {
        'user_id': user_id,
        'amount': amount,
        'location': location,
        'timestamp': current_time
    }

    # Add transaction to history and recent transactions
    add_transaction(user_id, amount, location, current_time)
    add_recent_transaction(user_id, amount, location)
    
    # Add the transaction to the graph (representing connections between users)
    add_transaction_to_graph(user_id, receiver_id)

    # Check if the transaction is suspicious
    if is_suspicious_transaction(transaction) or detect_anomaly(transaction, user_id):
        risk_score = calculate_risk_score(transaction, user_id)
        add_suspicious_transaction(user_id, amount, risk_score)
        print(f"Suspicious transaction detected for user {user_id}: ${amount}")
    
    # Check for frequent transactions in a short time
    if check_frequent_transactions_in_window(user_id):
        print(f"User {user_id} has made frequent transactions within a short period.")

# Function to calculate the risk score of a transaction (you can improve this logic)
def calculate_risk_score(transaction, user_id):
    # Example risk scoring logic: Higher amounts and anomalies result in higher scores
    risk_score = transaction['amount'] / 1000  # Basic scoring based on amount
    if detect_anomaly(transaction, user_id):
        risk_score += 10  # Add more weight if the transaction is anomalous
    return risk_score

# Function to detect fraud patterns (like loops) in the transaction graph
def detect_fraud_patterns_in_graph():
    # Implement a graph traversal algorithm to detect suspicious patterns
    pass

# Example use case of processing a batch of transactions
if __name__ == "__main__":
    # Simulate some transactions
    process_transaction("user_1", 15000, "New York", "user_2")
    process_transaction("user_1", 12000, "Los Angeles", "user_3")
    process_transaction("user_2", 5000, "Chicago", "user_4")
    process_transaction("user_3", 20000, "Houston", "user_5")
    process_transaction("user_4", 8000, "Miami", "user_1")

    # Get the highest-priority suspicious transaction
    print("Most suspicious transaction: ", get_most_suspicious_transaction())

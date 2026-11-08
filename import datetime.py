import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)
USERS = {
    "admin_user": {"role": "Admin"},
    "guest_user": {"role": "Guest"},
}

DOCUMENTS = {
    "doc_001": {"title": "Confidential Project Report", "allowed_role": "Admin"}
}
def log_access(username, doc_id, status):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] User: '{username}' tried accessing Doc: '{doc_id}' -> Result: {status}\n"

    # Saves to a simple text file as an undeniable proof/audit trail
    with open("audit_trail.txt", "a") as log_file:
        log_file.write(log_entry)
    print(log_entry.strip())
@app.route("/access-document", methods=["GET"])
def access_document():
    username = request.args.get("username")
    doc_id = request.args.get("doc_id")
    if username not in USERS:
        log_access(username or "Unknown", doc_id, "DENIED (Invalid User)")
        return (
            jsonify({"error": "Wrong Person! Access Denied instantly."}),
            401,
        )

    user_role = USERS[username]["role"]
    if doc_id not in DOCUMENTS:
        return jsonify({"error": "Document not found"}), 404

    required_role = DOCUMENTS[doc_id]["allowed_role"]
    if user_role == required_role:
        log_access(username, doc_id, "ALLOWED")
        return jsonify(
            {
                "status": "Success",
                "document_content": DOCUMENTS[doc_id]["title"],
                "message": f"Authorized successfully as {user_role}.",
            }
        )
    else:
        log_access(username, doc_id, f"DENIED (Role Mismatch: {user_role})")
        return (
            jsonify(
                {"error": "Authorization Failed. You do not have permission."}
            ),
            403,
        )


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify
import socket
import ipaddress
import re

app = Flask(__name__)

@app.route("/check", methods=["POST"])
def check_port():
    data = request.json
    host = data.get("host", "").strip()
    port = data.get("port")

    if not host or not port:
        return jsonify({"error": "Enter host and port"}), 400

    try:
        port = int(port)

        if port < 1 or port > 65535:
            return jsonify({"error": "Invalid port number"}), 400

        try:
            ipaddress.ip_address(host)
        except ValueError:
            if not re.fullmatch(r"(?i)(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)*", host):
                return jsonify({"error": "Invalid hostname or IP address"}), 400

        with socket.create_connection((host, port), timeout=3):
            status = "OPEN"

        return jsonify({"host": host, "port": port, "status": status})

    except socket.timeout:
        return jsonify({"host": host, "port": port, "status": "CLOSED"})
    except OSError:
        return jsonify({"host": host, "port": port, "status": "CLOSED"})

if __name__ == "__main__":
    app.run(debug=True)
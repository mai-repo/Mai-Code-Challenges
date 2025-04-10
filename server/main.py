from flask import Flask, jsonify, request
from GPT import generateCodeChallenge, evaluateProblem
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def connectDatabase():
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

    try:
        connection = psycopg2.connect(
                host=DATABASE_HOST,
                port=DATABASE_PORT,
                database=DATABASE_NAME,
                user=DATABASE_USER,
                password=DATABASE_PASSWORD
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")



@app.get("/generateChallenge")
def getChallenge():
    try:
        codeChallenge = generateCodeChallenge()
        if codeChallenge:
            return jsonify(codeChallenge), 200
        else:
            return jsonify({"error": "Failed to generate challenge"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.post("/evaluateAnswer")
def evaluateAnswer():
    try:
        data = request.get_json()
        challenge = data.get("challenge")
        answer = data.get("answer")

        if not challenge or not answer:
            return jsonify({"error": "Missing either challenge or answer"}), 400

        evaluation = evaluateProblem(challenge, answer)
        return jsonify(evaluation), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)




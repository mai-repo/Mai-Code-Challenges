from db_connection import connectDatabase
from flask import Blueprint, jsonify, request

rejected = Blueprint('rejected', __name__)

@rejected.get('/getRejected')
def getRejected():
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing field information."}), 400

    try:
        connection = connectDatabase()
        cursor = connection.cursor()

        cursor.execute('''
                        SELECT REJECTED_PROBLEMS
                        FROM REJECTED
                        WHERE USER_ID = %s
                        ''', (user_id,))
        rejected_problems = cursor.fetchall()

        problem_ids = [[row[0]] for row in rejected_problems]


        cursor.execute('''
            SELECT *
            FROM QUESTIONS
            WHERE ID = ANY(%s)
            ''', (problem_ids,))

        questions = cursor.fetchall()

        return jsonify(questions)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@rejected.post("/addRejected")
def addRejected():
    data = request.get_json()
    user_id = data.get("user_id")
    questions_id = data.get("questions_id")

    if not all ([user_id and questions_id]):
        return jsonify({"error": "Missing field information."}), 400
    try:
        connection = connectDatabase()
        cursor = connection.cursor()

        cursor.execute('''
                        INSERT INTO REJECTED (USER_ID, REJECTED_PROBLEMS)
                        VALUES (%s, %s)
                        ''', (user_id, questions_id))
        connection.commit()
        return jsonify({"message":"Successfully added problem"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        connection.close()

@rejected.put('/updateRejected')
def updateRejected():
    data = request.get_json()
    user_id = data.get("user_id")
    rejected_id = data.get("rejected_id")
    name = data.get('name').lower()

    if not all ([user_id, rejected_id, name]):
        return jsonify({"error":"Missing field information"}), 400

    try:
        connection = connectDatabase()
        cursor = connection.cursor()

        cursor.execute('''
                        SELECT REJECTED_PROBLEMS
                        FROM REJECTED
                        WHERE ID = %s and USER_ID = %s
                        ''', (rejected_id, user_id))
        result = cursor.fetchone()
        question_id = result[0]

        cursor.execute('''
                        UPDATE QUESTIONS
                        SET NAME = %s
                        WHERE ID = %s
                        ''', (name, question_id))
        connection.commit()
        return jsonify({"message": "Successfully updated name."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()


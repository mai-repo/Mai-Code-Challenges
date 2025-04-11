from db_connection import connectDatabase
from flask import Blueprint, jsonify, request

completed = Blueprint("completed", __name__)

@completed.get("/getCompleted")
def getCompleted():
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing field information."}), 400

    try:
        connection = connectDatabase()
        cursor = connection.cursor()

        cursor.execute('''
                        SELECT COMPLETED_PROBLEMS
                        FROM COMPLETED
                        WHERE USER_ID = %s
                        ''', (user_id,))

        results = cursor.fetchall()

        problem_ids = [row[0] for row in results]

        if not problem_ids:
            return jsonify([])

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

@completed.post('/addCompleted')
def addCompleted():
    data = request.get_json()
    user_id = data.get('user_id')
    questions_id = data.get('questions_id')

    if not all ([user_id and questions_id]):
        return (jsonify({"error": "Missing field information."}))

    try:
        connection = connectDatabase()
        cursor = connection.cursor()

        cursor.execute('''
                        INSERT INTO COMPLETED (USER_ID, COMPLETED_PROBLEMS)
                        VALUES (%s, %s)
                       ''', (user_id, questions_id))

        connection.commit()
        return jsonify({"message": "Completed Problem added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
            cursor.close()
            connection.close()

@completed.put('/updateCompleted')
def updateCompleted():
    data = request.get_json()
    user_id = data.get('user_id')
    name = data.get('name')
    completed_id = data.get('completed_id')

    if not all([user_id, name, completed_id]):
        return jsonify({"error": "Missing field information."})

    try:
        connection = connectDatabase()
        cursor = connection.cursor()

        cursor.execute('''
                        SELECT ID
                        FROM COMPLETED
                        WHERE ID = %s and USER_ID = %s
                       ''', (completed_id, user_id))

        result = cursor.fetchone()
        questions_id = result[0]

        cursor.execute('''
                        UPDATE QUESTIONS
                        SET NAME = %s
                        WHERE USER_ID = %s and ID = %s
                       ''', (name, user_id, questions_id))
        connection.commit()
        return jsonify({"error": "Successfully updating name."})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        connection.close()

@completed.delete('/deleteCompleted')
def deleteCompleted():
    data = request.get_json()
    user_id = data.get('user_id')
    completed_id = data.get('completed_id')

    if not all([user_id, completed_id]):
        return jsonify({"error": "Missing field information."})

    try:
        connection = connectDatabase()
        cursor = connection.cursor()

        cursor.execute('''
                        DELETE FROM COMPLETED
                        WHERE ID = %s and USER_ID = %s
                       ''', (completed_id, user_id))
        connection.commit()
        return jsonify({"message": "Successfully deleted problem"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()
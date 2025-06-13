from flask import Flask, request, jsonify
from json_handler import (
    LoadJsonFile,
    SaveJsonFile,
    AddStudent,
    RemoveStudent,
    UpdateStudentGrade,
    GetStudentDetails,
    GetCourseStudents
)

app = Flask(__name__)

# file where storing all student data
DATA_FILE = "students_data.json"

# function to load data from the file
def LoadData():
    return LoadJsonFile(DATA_FILE)

# saves any changes that make back to the file
def SaveData(data):
    SaveJsonFile(DATA_FILE, data)

# main route to handle all CRUD operations
@app.route('/api/students', methods=['POST', 'GET', 'PUT', 'DELETE'])
def ManageStudents():
    try:
        # load the current data every time when a request is asked
        data = LoadData()

        # POST method to add a new student 
        if request.method == 'POST':
            # get the data sent in the request
            studentInfo = request.get_json()
            if not studentInfo:
                return jsonify({'error': 'Missing JSON body'}), 400

            try:
                # try to add the student to the data
                AddStudent(data, studentInfo)
                SaveData(data)
                return jsonify({'message': 'Student added successfully'}), 201
            except ValueError as e:
                # error like duplicate ID or missing fields
                return jsonify({'error': str(e)}), 400

        # GET method to fetch student or course info 
        elif request.method == 'GET':
            # check if the user passed an ID
            studentId = request.args.get('id', type=int)

            # or maybe they passed a course code instead
            courseCode = request.args.get('course', type=str)

            # if it's an ID, then return that student's full info
            if studentId:
                try:
                    student = GetStudentDetails(data, studentId)
                    return jsonify(student), 200
                except ValueError as e:
                    return jsonify({'error': str(e)}), 404

            # if it's a course code, then return all students enrolled in it
            elif courseCode:
                try:
                    students = GetCourseStudents(data, courseCode)
                    return jsonify(students), 200
                except ValueError as e:
                    return jsonify({'error': str(e)}), 404

            # if nothing is provided error case to fill any id/course
            else:
                return jsonify({'error': 'Provide either "id" or "course" query parameter'}), 400

        #  PUT method to update a student grade
        elif request.method == 'PUT':
            # get the payload sent from the user
            payload = request.get_json()
            if not payload:
                return jsonify({'error': 'Missing JSON body'}), 400

            # grab all required fields
            studentId = payload.get('id')
            courseCode = payload.get('course_code')
            newGrade = payload.get('new_grade')

            # make sure nothing is missing
            if not all([studentId, courseCode, newGrade]):
                return jsonify({'error': 'Missing one or more fields: id, course_code, new_grade'}), 400

            try:
                # try updating the grade
                UpdateStudentGrade(data, studentId, courseCode, newGrade)
                SaveData(data)
                return jsonify({'message': 'Grade updated successfully'}), 200
            except ValueError as e:
                return jsonify({'error': str(e)}), 404

        #  DELETE method to remove a student
        elif request.method == 'DELETE':
            # get the ID from query params
            studentId = request.args.get('id', type=int)
            if not studentId:
                return jsonify({'error': 'Missing "id" query parameter'}), 400

            try:
                # try to remove the student
                RemoveStudent(data, studentId)
                SaveData(data)
                return jsonify({'message': 'Student removed successfully'}), 200
            except ValueError as e:
                return jsonify({'error': str(e)}), 404

    # handle any file issues or bad JSON 
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 500
    except ValueError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        # in case something totally unexpected happens
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

# running the Flask server for testing
if __name__ == '__main__':
    app.run(debug=True)

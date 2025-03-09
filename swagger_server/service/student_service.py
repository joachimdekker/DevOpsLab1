import os
from pymongo import MongoClient
from bson.objectid import ObjectId

# Get from environmental variables
uri = os.getenv("MONGO_URI")
if not uri:
    raise EnvironmentError("MONGO_URI is not set in environment variables!")

client = MongoClient(uri)
db = client["student_db"]
student_collection = db["students"]

def add(student=None):
    # Check if a student with the same first_name and last_name exists
    query = {"first_name": student.first_name, "last_name": student.last_name}
    existing_student = student_collection.find_one(query)
    if existing_student:
        return 'already exists', 409

    # Insert the student document and store the generated ObjectId
    result = student_collection.insert_one(student.to_dict())
    return str(result.inserted_id)

def get_by_id(student_id=None):
    # Convert the student_id to ObjectId and retrieve the document
    student = student_collection.find_one({"_id": ObjectId(student_id)})

    if not student:
        return 'not found', 404

    # Add a student_id field to the document for consistency
    student['student_id'] = str(student['_id'])
    return student

def delete(student_id=None):
    # Attempt to delete the document by its ObjectId
    result = student_collection.delete_one({"_id": ObjectId(student_id)})

    if result.deleted_count == 0:
        return 'not found', 404

    return student_id

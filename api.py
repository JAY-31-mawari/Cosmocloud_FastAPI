from fastapi import FastAPI, HTTPException
from typing import List,Optional
from bson import ObjectId
from models import Student, UpdateStudent
from db import client, database, collection
from starlette.responses import JSONResponse

app = FastAPI()

# TO GET EVERY INFORMATION FROM DATABASE TO EASE THE TESTING API PROCESS WHICH REQUIRE ID
@app.get("/")
async def mainpage():
    data=[]
    for student in collection.find({}):
        student["id"]=str(student["_id"])
        del student["_id"]
        data.append(student)
    return {"msg":"Welcome! To the main page here you will get students information","data":data}


# POST METHOD
@app.post("/students")
async def CreateStudent( student: Student ):
    try:
        student_data = student.dict()
        result = collection.insert_one(student_data)
        data={"id": str(result.inserted_id)}
        return JSONResponse(content=data, status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# GET METHOD ALONG WITH QUERY PARAMETER TO FILTER OUT STUDENTS DATA ON BASIS OF 'COUNTRY' AND 'AGE'
@app.get("/students")
async def ListStudents(country:str|None= None, age:int|None= None):
    try:
        query = {}
        if country:
            query["address.country"] = country
        if age is not None:
            query["age"] = {"$gte": age}

        result = list(collection.find(query , {"_id": 0, "address":0}))
        return {"data": result}

    except Exception as e:
        raise HTTPException(status_code = 500, detail="Internal server error")


# GET SPECIFIC STUDENT - get the student id from the "/" endpoint
@app.get("/students/{id}")
async def FetchStudent( id: str):
    if not collection.find_one({"_id": ObjectId(id)}):
        raise HTTPException(status_code=404,detail="Student ID not found")

    result = list(collection.find({"_id": ObjectId(id)}))
    student = result[0]

    if student is not None:    
        return {"name":student["name"],"age":student["age"],"address":{"city":student["address"]["city"],"country":student["address"]["country"]}}
    else:
        raise HTTPException(status_code = 500, detail="Internal server error")


# UPDATE STUDENT - get the student id to update from the "/" endpoint
@app.patch("/students/{id}")
async def UpdateStudent(id: str, student: UpdateStudent = None):
    student_data = student.dict(exclude_unset=True)
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": student_data})

    if result.modified_count == 1:
        return JSONResponse(content={},status_code=204)
    else:
        raise HTTPException(status_code=500, detail="Internal server error")



# DELETE STUDENT - get the student id to delete from the "/" endpoint
@app.delete("/students/{id}")
async def DeleteStudent( id: str ):
    if not collection.find_one({"_id": ObjectId(id)}):
        raise HTTPException(status_code=404,detail="Student ID not found")

    result = collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 1:
        return {"msg":"Student account deleted duccessfully"}
    else:
        raise HTTPException(status_code=500,detail="Internal server error")

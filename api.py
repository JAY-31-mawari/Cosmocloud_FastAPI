from fastapi import FastAPI, HTTPException
from typing import List,Optional
from bson import ObjectId
from models import Student, Student_Patch, Address
from db import client, database, collection

app = FastAPI()

@app.get("/")
def mainpage():
    return {"Success":"true", "msg":"Welcome! you got to the first main page and eveything is successfully running"}

@app.post("/students") # post method
async def CreateStudent( student: Student ):
    try:
        student_object = student.dict()
        result = collection.insert_one(student_object)
        return {"id": str(result.inserted_id)}

    except Exception as e:
        raise HTTPException(status_code = 500, detail="Internal server error")



@app.get("/students")
async def GetStudents(
    country: str|None= None, 
    age: int|None= None
):

    try:
        query = {}
        result = collection.find({})
        if country:
            query["address.country"] = country
        if age is not None:
            query["age"] = {"$gte": age}

        result = list(collection.find(query , {"_id": 0, "address":0}))
        return {"data": result}

    except Exception as e:
        raise HTTPException(status_code = 500, detail="Internal server error")


@app.get("/students/{id}")
async def GetStudent( id: str):
    if not collection.find_one({"_id": ObjectId(id)}):
        raise HTTPException(status_code=404,detail="Student ID not found")

    result = list(collection.find({"_id": ObjectId(id)}))
    student = result[0]

    return {"name":student["name"],"age":student["age"],"address":{"city":student["address"]["city"],"country":student["address"]["country"]}}


@app.patch("/students/{id}")
async def Update_Student( id: str ,student_update: Student_Patch):
    student_data = student_update.dict(exclude_unset=True)

    if not collection.find_one({"_id":ObjectId(id)}):
        raise HTTPException(status_code=404,detail="Student ID not found")

    result = await collection.update_one({"_id": ObjectId(id)}, {"$set": student_data}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    else:
        return {}


@app.delete("/students/{id}")
async def Delete_Student( id: str):
    if not collection.find_one({"_id": ObjectId(id)}):
        raise HTTPException(status_code=404,detail="Student ID not found")

    result = collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 1:
        return {"msg":"Student account deleted duccessfully"}
    else:
        raise HTTPException(status_code=500,detail="Internal server error")
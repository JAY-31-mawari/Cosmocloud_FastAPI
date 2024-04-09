# Cosmocloud API assignment for the internship role

- I tried to implement everything specification as you mentioned in google docs and swagger like correct status code, id instead of _id, correct api endpoints, correct request and response body

# API routes

-GET("/")               - default route to get every fields from the mongoDB collection, for ease of testing api 

-POST("/students")      - to create the students data in the database

-GET("/students")       - to get the students data of "name" and "age". Optional Query paramater is there to filter out students data on basis of "country" and "age" greater than.

-GET("/students/{id})   - to get data of specific student

-PATCH("/students/{id}) - to update little information about students data

-DELETE("/students/{id})- to delete the student data from database


- common Error is handle by the status code of 500 i.e Internal server error
- successful response status code - 200
- if Id is incomplete or not found - status code - 404

# NOTE
-Thankyou for giving this opportunity for internship assignemnt, gain some knowledge and hoping to look forward working with you and learn a lot from you.

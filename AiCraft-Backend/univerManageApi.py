#########################################
# University Management Supabase Client #
#########################################

from Supabase import supabase
from fastapi import APIRouter, Query


router = APIRouter(prefix="/api/university-management")


@router.get("/")
def university_management_root():
    return {"message": "Welcome to the University Management API"}


@router.get("/students")
def get_students(
    name: str | None = Query(default=None),
    department: str | None = Query(default=None)
):
    query = (
        supabase
        .table("student")
        .select("id, name, dept_name, tot_cred")
        .eq("deleted", False)
    )

    if name:
        query = query.ilike("name", f"%{name}%")

    if department:
        query = query.ilike("dept_name", f"%{department}%")

    response = query.execute()
    return response.data

@router.get("/instructors")
def get_instructors(
    name: str | None = Query(default=None),
    department: str | None = Query(default=None)
):
    query = (
        supabase
        .table("instructor")
        .select("id, name, dept_name, salary")
        .eq("deleted", False)
    )

    if name:
        query = query.ilike("name", f"%{name}%")

    if department:
        query = query.ilike("dept_name", f"%{department}%")

    response = query.execute()
    return response.data

@router.get("/courses")
def get_courses(
    title: str | None = Query(default=None),
    department: str | None = Query(default=None)
):
    query = (
        supabase
        .table("course")
        .select("course_id, title, dept_name, credits")
        .eq("deleted", False)
    )

    if title:
        query = query.ilike("title", f"%{title}%")

    if department:
        query = query.ilike("dept_name", f"%{department}%")

    response = query.execute()
    return response.data

@router.get("/departments")
def get_departments(
    dept_name: str | None = Query(default=None),
    building: str | None = Query(default=None)
):
    query = (
        supabase
        .table("department")
        .select("dept_name, building, budget")
        .eq("deleted", False)
    )

    if dept_name:
        query = query.ilike("dept_name", f"%{dept_name}%")

    if building:
        query = query.ilike("building", f"%{building}%")

    response = query.execute()
    return response.data

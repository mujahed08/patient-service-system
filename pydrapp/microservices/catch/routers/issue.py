import pprint
from datetime import datetime
from typing import List
from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydrapp.microservices.\
    catch.pylidate.models import Issue, IssuePg
from pydrapp.commons.mongodb_connector import get_mongodb

def get_catch_db() -> AsyncIOMotorDatabase:
    return get_mongodb()

app = APIRouter()

@app.post("/catch/issues", response_model=Issue)
async def create_issue(issue: Issue):
    issue_db = get_catch_db()

    result = await issue_db.issues_sequence.update_one({'key': 'ISU'},
        {'$inc': {'next': 1}})
    print('updated %s document' % result.modified_count)

    document = await issue_db.issues_sequence.find_one({'key' : 'ISU'})
    pprint.pprint(document)
    issue.id = document.get('next')
    issue.app_id = 100
    issue.created_on = datetime.now()
    issue.updated_on = datetime.now()
    isu_dict = issue.dict()
    pprint.pprint(isu_dict)
    result = await issue_db.issues.insert_one(isu_dict)
    issue.object_id = str(result.inserted_id)
    return issue

@app.get("/catch/issues", response_model=IssuePg)
async def get_issues(page_number: int = 1, limit: int = 10):
    issue_db = get_catch_db()
    total = await issue_db.issues.count_documents({})
    cursor = issue_db.issues.find().skip((( page_number - 1 ) * limit )
        if page_number > 0 else 0 ).limit( limit )
    data:List[Issue] = []
    async for document in cursor:
        issue = Issue(summary=document.get('summary'), app_id=document.get('app_id'),
            type=str(document.get('type')))
        issue.object_id = str(document.get('_id'))
        issue.id = document.get('id')
        issue.created_on = document.get('created_on')
        issue.updated_on = document.get('updated_on')
        issue.status = document.get('status')
        issue.description = document.get('description')
        issue.weightage = document.get('weightage')
        issue.remarks = document.get('remarks')
        issue.expectations = document.get('expectations')
        issue.estimate = document.get('estimate')
        issue.remaining = document.get('remaining')
        data.append(issue)

    return IssuePg(page=page_number, total=total, data=data)

@app.get("/catch/issues/{issue_id}", response_model=Issue)
async def get_issue(issue_id: int):
    issue_db = get_catch_db()

    document = await issue_db.issues.find_one( {'id' : issue_id})
    issue = Issue(summary=document.get('summary'), app_id=document.get('app_id'),
        type=str(document.get('type')))
    issue.object_id = str(document.get('_id'))
    issue.id = document.get('id')
    issue.app_id = document.get('app_id')
    issue.created_on = document.get('created_on')
    issue.updated_on = document.get('updated_on')
    issue.status = document.get('status')
    issue.description = document.get('description')
    issue.weightage = document.get('weightage')
    issue.remarks = document.get('remarks')
    issue.expectations = document.get('expectations')
    issue.estimate = document.get('estimate')
    issue.remaining = document.get('remaining')
    return issue

@app.put("/catch/issues/{issue_id}", response_model=Issue)
async def update_issue(issue_id: int, updates: dict):
    issue_db = get_catch_db()

    updates['updated_on'] = datetime.now()
    result = await issue_db.issues.update_one( {'id' : issue_id},
        {'$set': updates})
    print('updated %s document' % result.modified_count)

    document = await issue_db.issues.find_one( {'id' : issue_id})
    issue = Issue(summary=document.get('summary'), app_id=document.get('app_id'),
        type=str(document.get('type')))
    issue.object_id = str(document.get('_id'))
    issue.id = document.get('id')
    issue.app_id = document.get('app_id')
    issue.created_on = document.get('created_on')
    issue.updated_on = document.get('updated_on')
    issue.status = document.get('status')
    issue.description = document.get('description')
    issue.weightage = document.get('weightage')
    issue.remarks = document.get('remarks')
    issue.expectations = document.get('expectations')
    issue.estimate = document.get('estimate')
    issue.remaining = document.get('remaining')
    return issue

@app.delete("/catch/issues/{issue_id}", response_model=dict)
async def del_patient(issue_id: int):
    issue_db = get_catch_db()

    result = await issue_db.issues.delete_many( {'id' : issue_id})
    print('deleted %s document' % result.deleted_count)

    return {'message' : 'SUCCESS'}

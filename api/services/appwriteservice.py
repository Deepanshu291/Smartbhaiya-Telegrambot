# from appwrite.client import Client
import os
from appwrite.client import Client
from appwrite.query import Query
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage, AppwriteException
from typing import List,Dict,Any
import logging
from dotenv import load_dotenv

load_dotenv()


projectID = os.getenv('PROJECT_ID')
appwriteapi = os.getenv('APPWRITE_API')
databaseId = os.getenv('DATABASE_ID')
collectionID = os.getenv('COLLECTION_ID')
collectionID2 = os.getenv('COLLECTION_ID2')


client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1') # Your API Endpoint
client.set_project(projectID) # Your project ID
client.set_key(appwriteapi)# Your secret API key

databases = Databases(client)
storage = Storage(client)


# from fastapi import HTTPException

def getcategory(cate: str) -> str:
    match cate:
        case 'notes': return 'Notes'
        case 'solution': return 'Book_solution'
        case 'book': return 'Books'
        case 'markwise': return 'markswisequestion'
        case _: return 'Unknown category'

async def fetchurl(class_name: str) -> List[Dict[str, Any]]:
    # query = getcategory(query)
    try:
        if class_name == '10th':
            collection_id = collectionID
        elif class_name == '9th':
            collection_id = collectionID2
        else:
            raise ValueError("Invalid class name. Please specify '9th' or '10th'.")

        response = databases.list_documents(
            databaseId,
            collection_id,
            queries = [
                Query.select(['chapterno','Chapter_Name','Notes','Books','Book_solution','markswisequestion'])
                ]
        )
        # Fetching documents from the appropriate collection
        # if chpno == 0:
        #     response = databases.list_documents(
        #     databaseId,
        #     collection_id,
        #     queries = [
        #         Query.select(['chapterno','Chapter_Name',query])
        #         ]
        #     )
        # else:
        #     response = databases.list_documents(
        #     databaseId,
        #     collection_id,
        #     queries = [
        #         Query.select(['chapterno','Chapter_Name',query]),
        #         Query.equal('chapterno',chpno)
        #         ]
        #     )

        if 'documents' in response:
            res = response['documents']
            result = [
                {
                    'name': doc['Chapter_Name'],
                    'notes': doc['Notes'],
                    'book':doc['Books'],
                    'solution':doc['Book_solution'],
                    'markswise':doc['markswisequestion'],
                }
                for doc in res
            ]
            # result = [
            #     {
            #         'name': doc['Chapter_Name'],
            #         'url': doc[query]
            #     }
            #     for doc in res
            # ]
            return result
        else:
            return []

    except AppwriteException as e:
        logging.error(f"Appwrite Error: {str(e)}")
        # raise HTTPException(status_code=500, detail=f"Appwrite Error: {str(e)}")
    except ValueError as ve:
        logging.error(f"Value Error: {str(ve)}")
        # raise HTTPException(status_code=400, detail=str(ve))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
dotenv_path = '/.env'
load_dotenv(dotenv_path)
# load_dotenv()

# Define FastAPI app
app = FastAPI()

# Define a Pydantic model for the data you want to read from the Google Sheet
class SheetData(BaseModel):
    cell_value: int

# Google Sheets credentials file (JSON file downloaded from Google Cloud Console)
# Retrieve the JSON string from the environment variable
# cred_json_string = os.getenv('GOOGLE_CREDENTIALS_JSON')

# json_keyfile_data = {
#     "type": os.getenv('type'),
#     "project_id": os.getenv('project_id'),
#     "private_key_id":os.getenv('private_key_id'),
#     "private_key":os.getenv('private_key'),
#     "client_email": os.getenv('client_email'),
#     "client_id": os.getenv('client_id'),
#     "auth_uri": os.getenv('auth_uri'),
#     "token_uri": os.getenv('token_uri'),
#     "auth_provider_x509_cert_url": os.getenv('auth_provider_x509_cert_url'),
#     "client_x509_cert_url": os.getenv('client_x509_cert_url'),
#     "universe_domain":os.getenv('universe_domain')
#   }

# default_values = {
#     "type": "service_account",
#     "project_id": "your_default_project_id",
#     "private_key_id": "your_default_private_key_id",
#     "private_key": "your_default_private_key",
#     "client_email": "your_default_client_email",
#     "client_id": "your_default_client_id",
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your_client_email%40your_project_id.iam.gserviceaccount.com",
#     "universe_domain": "default_universe_domain"
# }
# json_keyfile_data = {
#     "type": os.getenv('type', default_values['type']),
#     "project_id": os.getenv('project_id', default_values['project_id']),
#     "private_key_id": os.getenv('private_key_id', default_values['private_key_id']),
#     "private_key": os.getenv('private_key', default_values['private_key']),
#     "client_email": os.getenv('client_email', default_values['client_email']),
#     "client_id": os.getenv('client_id', default_values['client_id']),
#     "auth_uri": os.getenv('auth_uri', default_values['auth_uri']),
#     "token_uri": os.getenv('token_uri', default_values['token_uri']),
#     "auth_provider_x509_cert_url": os.getenv('auth_provider_x509_cert_url', default_values['auth_provider_x509_cert_url']),
#     "client_x509_cert_url": os.getenv('client_x509_cert_url', default_values['client_x509_cert_url']),
#     "universe_domain": os.getenv('universe_domain', default_values['universe_domain'])
# }
# Parse the JSON string back into a Python dictionary
# credentials_file = json.loads(cred_json_string)
# Google Sheets API scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Google Sheet key (ID of the Google Sheet)
sheet_key = '178Jr7nTOk24Iac-f3-OdXz9vWgmLFp1D419B0w00Meg'

# Google Sheet name
sheet_name = 'RENDER'

# Authenticate with Google Sheets API
# creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
# creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_file, scope)
creds = ServiceAccountCredentials.from_json_keyfile_dict(json_keyfile_data, scope)

client = gspread.authorize(creds)

# Endpoint to read data from the Google Sheet
@app.get("/")
async def increment_cell():
    try:
        # Open the Google Sheet by its key
        sheet = client.open_by_key(sheet_key)

        # Select the worksheet by its name
        worksheet = sheet.worksheet(sheet_name)

        # Read the current value from the cell
        current_value = int(worksheet.acell('A1').value)

        # Increment the value by 1
        new_value = current_value + 1

        # Write the updated value back to the cell
        worksheet.update_acell('A1', str(new_value))

        return {"message": "Cell incremented successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hello")
async def hello():
    print(os.getenv('type'),"pawan")
    print(os.getenv('project_id'),"pawan")

    return {"message": "Hello from Endpoint !"}


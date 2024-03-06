from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# /etc/secrets/credentials.json
# Define FastAPI app
app = FastAPI()

# Define a Pydantic model for the data you want to read from the Google Sheet
class SheetData(BaseModel):
    cell_value: int


# Google Sheets API scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Google Sheet key (ID of the Google Sheet)
sheet_key = '178Jr7nTOk24Iac-f3-OdXz9vWgmLFp1D419B0w00Meg'

# Google Sheet name
sheet_name = 'RENDER'

# Authenticate with Google Sheets API
creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/credentials.json", scope)

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


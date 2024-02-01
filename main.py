# This code need the "credentials.json" file of your OAuth client from Google Cloud to work well!!
import os.path
from math import ceil
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of the spreadsheet.
SPREADSHEET_ID = "1p8eLFplL6IE5H_z9pWUJdi2bQ1JZNC5Up9thNa4TN54"
RANGE_NAME = "engenharia_de_software!A1:H27"

# Function Code from Google Sheets API documentation
def get_credentials(creds):
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  return creds


def main():
  # Get user's acess
  creds = get_credentials(None)
  try:
    service = build("sheets", "v4", credentials=creds)

    # Read Sheets Infos
    sheet = service.spreadsheets()
    result = (sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute())
    values = result.get("values", [])

    # Get how many classes has the semester
    classes_per_semester = [int(i) for i in values[1][0].split() if i.isdigit()][0]

    # Separate the student list from other data
    students_list = values[3:]
    for student_data in students_list:

      situation = ""
      # Check if student absence was greater than 25%
      max_absence = classes_per_semester * 0.25
      student_absence = int(student_data[2])
      if (student_absence > max_absence):
        situation = "Reprovado por Falta"
      
      if(not situation):
        # Calculates student's average and choose her situation
        p1 = float(student_data[3].replace(",","."))
        p2 = float(student_data[4].replace(",","."))
        p3 = float(student_data[5].replace(",","."))

        m = (p1 + p2 + p3) / 3
        if(m >= 7):
          situation = "Aprovado"
        elif(m < 7 and m >= 5):
          situation = "Exame Final"
        else:
          situation = "Reprovado por Nota"

      # If situation is already set, changes to new one, if doesn't, sets it
      if len(student_data) >= 7:
        student_data[6] = situation 
      else: 
        student_data.append(situation)

      # If student's situation is "Exame Final" calculates their "Nota para  Aprovação Final, if doesn't sets 0 on it"
      if(student_data[6] == "Exame Final"):
        # Simplification of 5<=(m+naf)/2
        naf = ceil(10 - m)
        # If "naf" is already set, changes to new one, if doesn't, sets it
        if len(student_data) == 8:
          student_data[7] = naf   
        else:
          student_data.append(f"{naf}")
      else:
        if len(student_data) == 8:
          student_data[7] = "0"
        else:
          student_data.append("0")
    # Updates the data on sheet
    result = sheet.values().update(spreadsheetId= SPREADSHEET_ID, range = "A1", valueInputOption = "USER_ENTERED", body = { 'values' : values}).execute()
  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()

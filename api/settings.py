import os
from dotenv import load_dotenv
load_dotenv()

GCP_BUCKET = os.getenv("GCP_BUCKET")
GOOGLE_APP_CREDS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

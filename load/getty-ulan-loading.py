import xml.etree.ElementTree as ET
import os
import pandas as pd
import csv
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_dir = os.path.join(project_root, "raw")
os.makedirs(raw_dir, exist_ok=True)
ulan_path = os.path.join(raw_dir, "getty-ulan")

#a very small number (likely < 10) of the names have newline imbedded in them
def clean_text(text):
    if text is None:
        return None
    text_no_line_breaks = ' '.join(text.split())
    text_no_escapes = text_no_line_breaks.replace('\\', '')
    return text_no_escapes

def get_ulan_info(root):
    pref_bio = root.find('.//Preferred_Biography')
    pref_nat = root.find('.//Preferred_Nationality')

    return {
        'ulan_id': root.find('Subject').get('Subject_ID'),
        'birth_date': pref_bio.find('Birth_Date').text if pref_bio is not None else None,
        'death_date': pref_bio.find('Death_Date').text if pref_bio is not None else None,
        'nationality': pref_nat.find('Nationality_Code').text.split('/')[1] if pref_nat is not None else None,
    }

def get_ulan_names(root, names):
    ulan_id = root.find('Subject').get('Subject_ID')

    names.append({
        'ulan_id': ulan_id,
        'name': clean_text(root.find('.//Preferred_Term/Term_Text').text),
        'is_preferred': True
    })
    for e1 in root.findall('.//Non-Preferred_Term/Term_Text'):
        if e1.text:
            names.append({
                'ulan_id': ulan_id,
                'name': clean_text(e1.text),
                'is_preferred': False })

#single filename for testing (picasso)
# filename = os.path.join(ulan_path, "500009666.xml")

records = []
names = []

for filename in os.listdir(ulan_path):
    try:
        tree = ET.parse(os.path.join(ulan_path, filename))
        root = tree.getroot()
        records.append(get_ulan_info(root))
        get_ulan_names(root, names)
    except Exception as e:
        print(f"Skipped {filename}: {e}")
        #some of the xmls are just "Too Many Connections", which will be skipped

infodf = pd.DataFrame(records)
namesdf = pd.DataFrame(names)
infodf.to_sql('ulan_info', engine, schema='raw', if_exists='replace', index=False)
namesdf.to_sql('ulan_names', engine, schema='raw', if_exists='replace', index=False)
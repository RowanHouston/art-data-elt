import xml.etree.ElementTree as ET
import os
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_dir = os.path.join(project_root, "raw")
os.makedirs(raw_dir, exist_ok=True)
ulan_path = os.path.join(raw_dir, "getty-ulan")


def parse_ulan_file(filepath):
    tree = ET.parse(os.path.join(ulan_path, filename))
    root = tree.getroot()

    pref_bio = root.find('.//Preferred_Biography')
    pref_nat = root.find('.//Preferred_Nationality')

    return {
        'ulan_id': root.find('.//Subject').get('Subject_ID'),
        'preferred_name': root.find('.//Preferred_Term/Term_Text').text,
        'non_preferred_names': [el.text for el in root.findall('.//Non-Preferred_Term/Term_Text')],
        'birth_date': pref_bio.find('Birth_Date').text if pref_bio is not None else None,
        'death_date': pref_bio.find('Death_Date').text if pref_bio is not None else None,
        'nationality': pref_nat.find('Nationality_Code').text.split('/')[1] if pref_nat is not None else None,
    }

#single filename for testing (picasso)
# filename = os.path.join(ulan_path, "500009666.xml")

records = []
for filename in os.listdir(ulan_path):
    if not filename.endswith('.xml'):
        continue
    try:
        records.append(parse_ulan_file(os.path.join(ulan_path, filename)))
    except Exception as e:
        print(f"Skipped {filename}: {e}")
        #some of the xmls are just "Too Many Connections, which will be skipped"

df = pd.DataFrame(records)
df.to_csv(os.path.join(project_root, "cleaned", 'ulan_lookup.csv'), index=False)
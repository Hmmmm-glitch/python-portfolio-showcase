import csv
import difflib
import os
import re


raw_input = input("Enter the client file name : ")
file_to_clean = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', raw_input).strip()

user_delimiter = input("Enter the file separator (e.g., , or ; or |): ")


possible_paths = [
    file_to_clean,
    os.path.join("/storage/emulated/0/Download", file_to_clean),
    os.path.join("/sdcard/Download", file_to_clean)
]

resolved_path = None
for path in possible_paths:
    if os.path.exists(path) and os.path.isfile(path):
        resolved_path = path
        break

if not resolved_path:
    print(f"\n[Error] Cannot find '{file_to_clean}' anywhere.")
    print(f"Looked in Pydroid folder: {os.getcwd()}")
    print("Looked in phone Downloads: /storage/emulated/0/Download/")
    print("Please make sure you ran 'market_data.py' first to generate the file!")
else:
    print(f"\n[Success] Found file at: {resolved_path}")
    
    
    input_dir = os.path.dirname(resolved_path)
    output_file = os.path.join(input_dir, "cleaned_" + os.path.basename(resolved_path))
    
    with open(resolved_path, 'r', encoding='utf-8') as f, open(output_file, 'w', newline='', encoding='utf-8') as out_f:
        spreadsheet = csv.reader(f, delimiter=user_delimiter)
        writer = csv.writer(out_f, delimiter=user_delimiter)
        
        
        header = next(spreadsheet)
        writer.writerow(header)
        
        
        clean_headers = [h.strip().title() for h in header]
        
        
        for row in spreadsheet:
            clean_row = []
            for item in row:
                text = item.strip()
                
                
                if "@" in text:
                    clean_text = text.lower() 
                else:
                    clean_text = text.title() 
                
                
                matches = difflib.get_close_matches(clean_text, clean_headers, n=1, cutoff=0.6)
                if matches:
                    clean_text = matches[0]
                    
                clean_row.append(clean_text)
                
            print(clean_row)  
            writer.writerow(clean_row)
            
    print(f"\nProcess complete! Cleaned data saved successfully at: {output_file}")

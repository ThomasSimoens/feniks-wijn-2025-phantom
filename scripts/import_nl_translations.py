#!/usr/bin/env python3
"""
Import NL translations from a CSV file back into wines.json.
This allows copywriters to update translations via Google Sheets.
"""

import json
import csv
import sys
from pathlib import Path


def import_nl_translations(csv_path=None):
    # Get the project root directory (parent of scripts)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Paths
    wines_json_path = project_root / "src" / "feniks-data" / "wines.json"
    
    if csv_path is None:
        csv_path = project_root / "scripts" / "input" / "nl_translations.csv"
    else:
        csv_path = Path(csv_path)
    
    if not csv_path.exists():
        print(f"✗ Error: CSV file not found at {csv_path}")
        sys.exit(1)
    
    # Load wines data
    with open(wines_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Define all possible translatable fields
    translatable_fields = ['desc', 'flavour', 'pair_with', 'specials']
    
    # Read CSV and build update map
    updates = {}  # Structure: {wine_id: {field: nl_text}}
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            wine_id = row['wine_id']
            
            if wine_id not in updates:
                updates[wine_id] = {}
            
            # Read each translatable field from columns
            for field in translatable_fields:
                col_name = f'nl_{field}'
                if col_name in row:
                    nl_text = row[col_name]
                    if nl_text:  # Only store non-empty values
                        updates[wine_id][field] = nl_text
    
    # Apply updates
    updated_count = 0
    wines_updated = 0
    
    for wine in data['wines']:
        wine_id = wine.get('form_number', '')
        
        if wine_id in updates:
            wine_has_updates = False
            translatables = wine.get('translatables', {})
            
            for field, nl_text in updates[wine_id].items():
                if field in translatables:
                    # Update the NL translation
                    translatables[field]['nl'] = nl_text
                    updated_count += 1
                    wine_has_updates = True
            
            if wine_has_updates:
                wines_updated += 1
    
    # Write back to JSON
    with open(wines_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Imported {updated_count} translations from {csv_path}")
    print(f"  Updated {wines_updated} wine(s) in {wines_json_path}")


if __name__ == '__main__':
    csv_file = sys.argv[1] if len(sys.argv) > 1 else None
    import_nl_translations(csv_file)

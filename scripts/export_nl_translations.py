#!/usr/bin/env python3
"""
Export NL translations from wines.json to a CSV file.
This CSV can be uploaded to Google Sheets for copywriters to edit.
"""

import json
import csv
import os
from pathlib import Path


def export_nl_translations():
    # Get the project root directory (parent of scripts)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Paths
    wines_json_path = project_root / "src" / "feniks-data" / "wines.json"
    output_csv_path = project_root / "scripts" / "output" / "nl_translations.csv"
    
    # Load wines data
    with open(wines_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Define all possible translatable fields
    translatable_fields = ['desc', 'flavour', 'pair_with', 'specials']
    
    # Prepare CSV rows
    rows = []
    
    for wine in data['wines']:
        wine_id = wine.get('form_number', '')
        wine_title = wine.get('title', '')
        
        # Get translatable fields
        translatables = wine.get('translatables', {})
        
        # Build row with one column per field
        row = {
            'wine_id': wine_id,
            'wine_title': wine_title,
        }
        
        # Add each translatable field as a column
        for field in translatable_fields:
            if field in translatables:
                row[f'nl_{field}'] = translatables[field].get('nl', '')
            else:
                row[f'nl_{field}'] = ''
        
        rows.append(row)
    
    # Define fieldnames for CSV
    fieldnames = ['wine_id', 'wine_title'] + [f'nl_{field}' for field in translatable_fields]
    
    # Write to CSV
    with open(output_csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✓ Exported {len(rows)} wines to {output_csv_path}")
    print(f"  Translatable fields: {', '.join(translatable_fields)}")


if __name__ == '__main__':
    export_nl_translations()

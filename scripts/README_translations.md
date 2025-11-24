# Wine Translation Scripts

These scripts help manage Dutch (NL) translations for wines by exporting them to CSV format (for Google Sheets editing) and importing them back into the JSON file.

## Export NL Translations

Export all Dutch translations from `wines.json` to a CSV file:

```bash
python3 scripts/export_nl_translations.py
```

This creates `nl_translations.csv` in the project root with the following structure:
- One row per wine
- Columns:
  - `wine_id`: The wine's form number (identifier)
  - `wine_title`: The wine's title for reference
  - `nl_desc`: Dutch description text
  - `nl_flavour`: Dutch flavour/taste text
  - `nl_pair_with`: Dutch food pairing text
  - `nl_specials`: Dutch special notes text

Empty columns indicate that field is not defined for that wine.

You can upload this CSV to Google Sheets for copywriters to edit.

## Import NL Translations

Import updated Dutch translations from CSV back into `wines.json`:

```bash
# Import from default location (nl_translations.csv)
python3 scripts/import_nl_translations.py

# Or specify a custom CSV file path
python3 scripts/import_nl_translations.py path/to/updated_translations.csv
```

The script will:
1. Read the CSV file
2. Update only the NL translations in `wines.json`
3. Preserve all other language translations (EN, FR) and wine data
4. Maintain JSON formatting with proper indentation

## Workflow

1. Export translations: `python3 scripts/export_nl_translations.py`
2. Upload `nl_translations.csv` to Google Sheets
3. Share with copywriters for editing
4. Download updated CSV from Google Sheets
5. Import translations: `python3 scripts/import_nl_translations.py path/to/downloaded.csv`

## Notes

- The scripts preserve UTF-8 encoding for special characters
- Only NL translations are affected; EN and FR remain unchanged
- Wine identification is done by `form_number` (wine_id in CSV)
- The JSON file is automatically formatted with 2-space indentation

# Feniks Wijn 2025 - Phantom Template

## About

This is a basic static website to list some of the offered wines for a temporary sale for the profits of a basketball club called Feniks Zwijnaarde.

It should only list the availble wines (which can be found at `src/feniks-data`) with some context.
No need for any "buy" or "shopping cart" functionality, because Feniks chose to have a Google Sheet form: `https://docs.google.com/forms/d/e/1FAIpQLSdSG1oNepLKLmEqgqf29_z72hex94BARXuJfIsfdfyPc67l3A/viewform`.

## Recommendations

1. Support three languages; "Nederlands" (default), "English" and "Francais" 
2. Show the wines per category; "Bubbels", "Witte Wijn" and "Rode Wijn"
3. Wine images should all be shown consistently, all at the same size (as the original size and aspect ration can differ)
4. Even though we have individual URLs for all the wines, don't actually use them (because we want to actually guide them toward the Google Form where they can order to support the club)

## Local setup

The project is a static site. To preview locally, run a simple HTTP server from the project root. For example using Python 3:

```bash
cd src && python3 -m http.server 8000
```

Then open http://localhost:8000/ in your browser
# Finshots RSS Generator

Generates a clean RSS feed for Finshots using GitHub Actions.

## Setup

1. Create a GitHub repository.
2. Upload all files.
3. Enable GitHub Pages:
   - Settings → Pages
   - Deploy from a branch
   - Branch: main
   - Folder: / (root)

GitHub Actions will regenerate `finshots.xml` every day.

Your feed will be available at:

```
https://YOUR_USERNAME.github.io/REPOSITORY_NAME/finshots.xml
```

Example:

```
https://sweetshysprout-byte.github.io/finshots-rss/finshots.xml
```

# Deployment to GitHub Pages

This document explains how to deploy the Credit Card Mastery Flask app to GitHub Pages.

## Automatic Deployment

The repository is configured with GitHub Actions to automatically deploy to GitHub Pages when you push to the `main` branch.

### Setup GitHub Pages

1. Go to your GitHub repository: https://github.com/12TribesofIsrael/Credit-Card-Date-Mastery
2. Click on **Settings** tab
3. Scroll down to **Pages** section in the left sidebar
4. Under **Source**, select **GitHub Actions**
5. Save the settings

### Automatic Deployment Process

1. When you push to the `main` branch, GitHub Actions will automatically:
   - Set up Python environment
   - Install dependencies
   - Run the `build_static.py` script to generate static HTML files
   - Deploy the static files to GitHub Pages

2. Your app will be available at: `https://12tribesofisrael.github.io/Credit-Card-Date-Mastery/`

## Manual Deployment

If you need to deploy manually:

1. Run the build script locally:
   ```bash
   python build_static.py
   ```

2. The static files will be generated in the `build/` directory

3. You can test the static version by serving the build directory:
   ```bash
   cd build
   python -m http.server 8000
   ```

## Important Notes

- The deployed version will be a static HTML version of your Flask app
- Interactive features that require server-side processing will be limited
- The app will load with the default card data from `cards_data.json`
- Users won't be able to save changes persistently (no backend database)

## Troubleshooting

If deployment fails:
1. Check the **Actions** tab in your GitHub repository
2. Review the build logs for any errors
3. Ensure all required files are committed to the repository
4. Verify that GitHub Pages is enabled in repository settings

## Live App

Once deployed, your Credit Card Mastery app will be available at:
**https://12tribesofisrael.github.io/Credit-Card-Date-Mastery/** 
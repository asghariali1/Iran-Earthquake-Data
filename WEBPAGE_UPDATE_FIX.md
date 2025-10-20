# Webpage Update Fix - October 20, 2025

## Problem Identified
The GitHub Actions workflow was successfully running every 6 hours to update earthquake data, but the webpage (GitHub Pages) was **NOT updating** to reflect the new data.

## Root Cause
GitHub has a security feature where commits made by workflows using `GITHUB_TOKEN` **do not trigger other workflows**. This prevents infinite loops of workflows triggering each other.

### The Issue:
1. `update-earthquake-data.yml` runs every 6 hours ✅
2. It fetches new data and commits to `main` branch ✅
3. `deploy-pages.yml` should deploy to GitHub Pages ❌
4. **BUT**: The commit from the workflow doesn't trigger the deploy workflow ❌

## Solution Applied
Modified `.github/workflows/deploy-pages.yml` to add a `workflow_run` trigger that specifically listens for the completion of the "Update Earthquake Data" workflow.

### Changes Made:
1. **Added `workflow_run` trigger** to `deploy-pages.yml`:
   - Triggers when "Update Earthquake Data" workflow completes
   - Only on the `main` branch
   - Only if the workflow was successful

2. **Added conditional execution**:
   - Deploy job only runs if manually triggered, pushed to, or if the update workflow succeeded
   - Prevents deployment of failed data updates

3. **Ensured latest code is checked out**:
   - Added `ref: main` to checkout step to guarantee we get the latest commit

## How It Works Now

```
Every 6 hours OR Manual trigger
        ↓
Update Earthquake Data Workflow
        ↓
Fetches USGS data
        ↓
Commits changes to main branch
        ↓
[TRIGGERS] ← This was missing!
        ↓
Deploy to GitHub Pages Workflow
        ↓
Website updates automatically! ✅
```

## Testing the Fix

### Option 1: Wait for Next Scheduled Run
- Next automatic update will be within 6 hours
- Check GitHub Actions tab to see both workflows run

### Option 2: Manual Trigger (Immediate)
1. Go to: `Actions` → `Update Earthquake Data`
2. Click `Run workflow` → `Run workflow`
3. Watch both workflows execute:
   - First: Update Earthquake Data
   - Then: Deploy to GitHub Pages (triggered automatically)

### Verify the Fix:
1. Check the GitHub Actions page after a run
2. You should see **two workflow runs**:
   - ✅ Update Earthquake Data
   - ✅ Deploy to GitHub Pages (triggered by workflow_run)
3. Your webpage should now show updated data

## Technical Details

### Before (Broken):
```yaml
on:
  push:
    branches: [ main ]
  workflow_dispatch:
```
*Problem*: Push event doesn't fire for commits made by GITHUB_TOKEN

### After (Fixed):
```yaml
on:
  push:
    branches: [ main ]
  workflow_dispatch:
  workflow_run:
    workflows: ["Update Earthquake Data"]
    types:
      - completed
    branches: [ main ]
```
*Solution*: `workflow_run` explicitly listens for workflow completion

## Additional Notes
- The data update will continue to run every 6 hours automatically
- Pages will deploy immediately after each successful data update
- Manual deployments still work via push or workflow_dispatch
- No changes needed to update_earthquake_data_github.py
- No changes needed to the website code (index.html, script.js)

## References
- [GitHub Docs: Triggering a workflow from a workflow](https://docs.github.com/en/actions/using-workflows/triggering-a-workflow#triggering-a-workflow-from-a-workflow)
- [GitHub Docs: workflow_run event](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_run)

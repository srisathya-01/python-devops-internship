@echo off 
echo === EMERGENCY ROLLBACK === 
git checkout HEAD~1 -- src/app/main.py 
echo Re-deploying previous version... 
call ci-cd\deploy-staging.bat 
echo === ROLLBACK COMPLETE === 

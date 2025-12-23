@echo off
REM Push to GitHub Script
REM Replace YOUR_USERNAME below with your actual GitHub username

set USERNAME=YOUR_USERNAME

echo Adding remote origin...
git remote add origin https://github.com/%USERNAME%/ai-textbook-platform.git

echo Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo Done! Your code is now on GitHub.
echo Visit: https://github.com/%USERNAME%/ai-textbook-platform
pause

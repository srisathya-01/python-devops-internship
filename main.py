"# main.py" 
print("Hello DevOps!") 
git checkout main
git pull origin main
echo "# trigger" >> README.md
git add README.md
git commit -m "Trigger CI workflow"
git push origin main


# Data Versioning Control

Docs : https://dvc.org/doc/start

## Intialize
```bash
# Install DVC
pip install dvc dvc[gdrive] 
# pip install pydrive # Not sure this one was required
# Initialize project
dvc init
# Setup Google Drive as remote storage
# Create a folder and find its ID from the end of the url
# eg : https://drive.google.com/drive/u/0/folders/1Kg6IrIl59EmKDn01rviZZ4yYwGUTHGPp
dvc remote add myremote gdrive://1Kg6IrIl59EmKDn01rviZZ4yYwGUTHGPp
dvc remote default myremote
# Make a test file and add it to DVC
mkdir ./data
echo "test" > ./data/test_dvc.txt
dvc add ./data/test_dvc.txt
dvc push
# You should now open your browser to accept authentication link
```

cd lambda
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
cp lambda_function.py venv/lib/python<version>/site-packages/
cd venv/lib/python<version>/site-packages/
zip -r lambda_package.zip *
mv lambda_package.zip ../../../../

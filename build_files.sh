
echo " BUILD START"
pip install -r requirements.txt


echo "makemigrations"
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

echo "collect statics --....."
python3.9 manage.py collectstatic
echo " BUILD ENDS"

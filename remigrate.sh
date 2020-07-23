rm -r */migrations 
source activate django  
python manage.py makemigrations USER && python manage.py migrate USER
python manage.py makemigrations BIS && python manage.py migrate  BIS 
python manage.py makemigrations LIMS && python manage.py migrate  LIMS
python manage.py makemigrations SEQ && python manage.py migrate  SEQ
python manage.py makemigrations EMR && python manage.py migrate  EMR
python manage.py makemigrations ADVANCE && python manage.py migrate  ADVANCE
python manage.py makemigrations && python manage.py migrate

mysql -udjango -pdjango databaseDemo2 < user.sql
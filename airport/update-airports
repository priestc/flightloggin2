#! /bin/bash


export PYTHONPATH=/home/chris/Websites/$1:/home/chris/lib/python2.6
export DJANGO_SETTINGS_MODULE=settings

no='get'

if [ $2 = $no ]; then

    echo ">>>>>>>> Getting remote airport files...<<<<<<<";

    wget -O - http://www.ourairports.com/data/regions.csv > ~/Websites/$1/airport/fixtures/regions.csv;
    wget -O - http://www.ourairports.com/data/countries.csv > ~/Websites/$1/airport/fixtures/countries.csv;
    wget -O - http://www.ourairports.com/data/airports.csv > ~/Websites/$1/airport/fixtures/airports.csv;
    wget -O - http://www.ourairports.com/data/navaids.csv > ~/Websites/$1/airport/fixtures/navaids.csv;

    echo ">>>>>>>>>>>>>>>>>> Diff Below <<<<<<<<<<<<<<<<<";

    cd ~/Websites/$1/; git diff /home/chris/Websites/$1/airport/fixtures/airports.csv;
    git diff /home/chris/Websites/$1/airport/fixtures/navaids.csv; cd -;
fi

echo ">>>>>>>>>>>> Clearing local database <<<<<<<<<<";

~/Websites/$1/manage.py reset airport;

echo ">>>>>>>>>> Running Import script... <<<<<<<<<<<";

python ~/bin/imports.py $1;

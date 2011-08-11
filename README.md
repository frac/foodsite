Foodsite
=============


My personal food blog written in django

To Install the requirements

    pip install -r requirements.txt


Then copy the distributed settings.py-DIST to settings.py

    cp settings.py-DIST settings.py

and edit the settings.py to your liking (db, secret and so on)

Then
  
    ./manage syncdb
    ./manage migrate

Posts are made in the admin

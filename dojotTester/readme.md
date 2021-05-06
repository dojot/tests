# How run

``
mkdir ~/virtualenv-dojot-tests #only the first time

``

``
sudo apt-get install python3-venv  #only the first time
``

``
python3 -m venv ~/virtualenv-dojot-tests/  #run every time
``
``
source ~/virtualenv-dojot-tests/bin/activate  #run every time
``

## May be necessary to use sudo

``
(sudo) pip3 install -r requirements.txt #only the first time
``

## Run Sanity Testing

``
sudo python3 dojotTester.py  SanityTest
``

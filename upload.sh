python setup.py sdist upload --verbose -r privatepypi
rm -rf dist
pip install -U --extra-index-url http://100.95.241.19 --trusted-host 100.95.241.19 SekitobaLibrary

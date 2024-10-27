## !/bin/bash
currentVersion=`pip list | grep SekitobaLibrary | awk -F ' ' '{ print $2 }'`
fileVersion=`cat setup.py | grep version | awk -F '"' '{ print $2 }'`
update=`echo | awk -v c="${currentVersion}" -v f="${fileVersion}" 'BEGIN{a=1}{if(c<f) a=0} END{print a}'`
newVersion="${fileVersion}"

if [ "${update}" == 1 ]; then
  newVersion=`echo "${fileVersion}" | awk -F "." '{ print $1"\."$2"\."$3+1 }'`
  sed -i '' "s/${fileVersion}/${newVersion}/g" setup.py
fi

python setup.py sdist upload --verbose -r privatepypi
rm -rf dist
pip install -U --extra-index-url http://100.95.241.19 --trusted-host 100.95.241.19 SekitobaLibrary

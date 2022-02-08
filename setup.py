from setuptools import setup, find_packages
 
setup(
    name='SekitobaLibrary',    #パッケージ名
    version="1.0.0",
    description="SekitobaLibrary PackageCode",
    long_description="",
    author='SekitobaLibrary',
    license='MIT',
    classifiers=[
        "Development Status :: 1 - Planning"
    ]
    ,packages=[ 'sekitoba_library', 'sekitoba_data_manage', 'sekitoba_data_create' ]   #パッケージのサブフォルダー
)

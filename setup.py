from setuptools import setup, find_packages
 
setup(
    name='SekitobaLibrary',    #パッケージ名
    version="1.3.62",
    description="SekitobaLibrary PackageCode",
    long_description="",
    author='SekitobaLibrary',
    license='MIT',
    install_requires=["requests", "pandas", "lightgbm", "numpy", "matplotlib", "tqdm", "statistics", "boto3", "torch", "trueskill", "bs4", "jpholiday"],
    classifiers=[
        "Development Status :: 1 - Planning"
    ]
    ,packages=[ 'SekitobaLibrary', 'SekitobaDataManage', 'SekitobaDataCreate', 'SekitobaLogger', 'SekitobaPsql']
)

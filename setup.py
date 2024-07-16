from setuptools import setup, find_packages
 
setup(
    name='SekitobaLibrary',    #パッケージ名
    version="1.0.0",
    description="SekitobaLibrary PackageCode",
    long_description="",
    author='SekitobaLibrary',
    license='MIT',
    install_requires=["requests", "pandas", "lightgbm", "numpy", "matplotlib", "tqdm", "statistics", "boto3", "torch", "mpi4py", "trueskill", "bs4", "jpholiday"],
    classifiers=[
        "Development Status :: 1 - Planning"
    ]
    ,packages=[ 'sekitoba_library', 'sekitoba_data_manage', 'sekitoba_data_create', 'sekitoba_logger', 'sekitoba_psql']
)

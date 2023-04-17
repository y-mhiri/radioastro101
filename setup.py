import setuptools 



setuptools.setup(  
    name='radioastro101',
    version='0.1',
    description='Radio interferometry 101 WebApp',
    url='y-mhiri.github.io',
    author='y-mhiri',
    install_requires=['numpy==1.21.1', 
                     'scipy==1.9.1', 
                     'scikit-image==0.20.0',
                     'ducc0==0.29.0',
                     'zarr==2.14.2',
                     'click==8.0.0',
                     'astropy==5.2.1',
                     'dash==2.9.1',
                     'pandas==1.5.3'],
    author_email='yassine.mhiri@outlook.fr',
    packages=setuptools.find_packages(),
    zip_safe=False
        )


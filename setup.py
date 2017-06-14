from setuptools import setup, find_packages

setup(
    name='spt_compute',
    version='2.0.0',
    description='Computational framework for the Streamflow Prediciton Tool',
    long_description='Computational framework to ingest ECMWF ensemble runoff forcasts or WRF forecasts;'
                     ' generate input for and run the RAPID (rapid-hub.org) program'
                     ' using HTCondor or Python\'s Multiprocessing; and upload to '
                     ' CKAN in order to be used by the Streamflow Prediction Tool (SPT).'
                     ' There is also an experimental option to use the AutoRoute program'
                     ' for flood inundation mapping.',
    keywords='ECMWF, WRF, RAPID, Flood Prediction, Streamflow Prediction Tool',
    author='Alan Dee Snow',
    author_email='alan.d.snow@usace.army.mil',
    url='https://github.com/erdc-cm/spt_ecmwf_autorapid_process',
    license='BSD 3-Clause',
    packages=find_packages(),
    install_requires=['numpy', 'netCDF4', 'RAPIDpy', 'tethys_dataset_services'],
    classifiers=[
                'Intended Audience :: Developers',
                'Intended Audience :: Science/Research',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.7',
                ],
)

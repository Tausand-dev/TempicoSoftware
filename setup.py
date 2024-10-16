from setuptools import setup, find_packages
setup(
    name='TempicoSoftware',
    version='1.0.0',
    packages=find_packages(),
    
    install_requires=[
                        
                    'pyAbacus',
                    'altgraph==0.17',
                    'auto-py-to-exe==2.43.3',
                    'future==1.0.0',
                    'hidapi==0.14.0.post2',
                    'markdown-it-py==3.0.0',
                    'matplotlib==3.5.3',
                    'numpy==1.22.0',
                    'pyinstaller==6.10.0',
                    'pyinstaller-hooks-contrib==2024.3',
                    'PyQt5==5.15.11',
                    'PyQt5-Qt5==5.15.2',
                    'PyQt5_sip==12.15.0',
                    'pyqtgraph==0.13.3',
                    'pyserial==3.5',
                    'PySide2==5.15.2.1',
                    'pyTempico==1.0.0',
                    'pytz==2024.1',
                    'pywin32-ctypes==0.2.2',
                    'readme_renderer==43.0',
                    'rich==13.9.1',
                    'scipy==1.9.1 --only-binary :all:',
                    'setuptools==70.0.0',
                    'shiboken2==5.15.2.1',
                    'virtualenv==20.26.3',
                    'zipp==3.19.1',

        

    ],
    include_package_data=True, 
    package_data={
        '': ['Sources/*'], 
    },
)
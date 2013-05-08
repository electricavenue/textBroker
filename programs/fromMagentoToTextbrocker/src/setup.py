import py2exe
import distutils.core


distutils.core.setup(
    console = ['main.py'],
    data_files = ['config.ini'],
    options = {
        'py2exe': {
            'optimize': 2,
            'compressed': True,
            'bundle_files': 1
        }
    },
    zipfile=None
)
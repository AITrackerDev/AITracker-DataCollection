from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': [], "include_files": ["assets/"]}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('DataCollection.py', base=base)
]

setup(name='aiTracker-DataCollection',
      version = '1',
      description = 'Application to collect data for the aiTracker neural network',
      options = {'build_exe': build_options},
      executables = executables)

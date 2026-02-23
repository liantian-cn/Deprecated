from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages=[], excludes=[], include_msvcr=True)

base = 'WIN32GUI'

executables = [
    Executable('NoSleep.py', base=base)
]

setup(name='FileCheck',
      version='1.0',
      description='',
      options=dict(build_exe=buildOptions),
      executables=executables)

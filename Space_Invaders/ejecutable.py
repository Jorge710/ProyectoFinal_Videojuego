import sys
import os
from cx_Freeze import setup, Executable

build_exe_options = {'packages': []}
base = "Win32GUI"

exe = Executable(
      script="cc.py",
      base="Win32GUI",

)
setup(
      name = "Spase Invaders",
      options = {'build_exe': build_exe_options},
      executables = [Executable("spaceinvaders.py", base=base)])

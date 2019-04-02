import sys
from cx_Freeze import setup, Executable

setup(
        name = "Cash 4 Gear",
        version = 1.0,
        description = "Optimizing gear choices for a starting DnD 5e character.",
        executables = [Executable(script="cash4gear.py")],
     )

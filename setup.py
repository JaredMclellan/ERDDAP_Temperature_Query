from cx_Freeze import setup, Executable

base = None
executables = [Executable("Main.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "ERDDAP Temperature Reporter",
    options = options,
    version = "1.0",
    description = 'Creates a temperature report from ERDDAP data',
    executables = executables
)
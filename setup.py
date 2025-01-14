from cx_Freeze import setup, Executable

setup(
    name="The Last Survivor",
    version="0.5",
    options={
        "build_exe": {
            "packages": ["pygame", "pyscroll", "pytmx"],
            "include_files": [
                "res/",
                "src/",
                "data/",
                "LICENSE",
                "README.md",
                "requirements.txt",
            ],
        }
    },
    executables=[
        Executable(
            "main.py",
            target_name="The Last Survivor.exe",
            base="Win32GUI",
        )
    ],
)

# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import (
    collect_data_files, 
    collect_submodules,
    collect_dynamic_libs,
    get_package_paths
)

########################################
# Photutils
########################################
photutils_data = collect_data_files('photutils')
photutils_submodules = collect_submodules('photutils')
photutils_binaries = collect_dynamic_libs('photutils')

########################################
# Dask data (if needed)
########################################
dask_data = collect_data_files('dask', include_py_files=False)

########################################
# sep_pjw (the library that references _version)
########################################
sep_pjw_submodules = collect_submodules('sep_pjw')
sep_pjw_binaries = collect_dynamic_libs('sep_pjw')

# If you also need a top-level _version:
# (Check if this is truly needed or if just 'sep_pjw._version' is enough.)
# from PyInstaller.utils.hooks import collect_submodules
# version_submodules = collect_submodules('_version')  # Possibly

directory = './.venv/lib/python3.*/site-packages'

########################################
# Build hiddenimports
########################################
hiddenimports = [
    # Existing photutils
    *photutils_submodules,

    # Force 'sep_pjw'
    'sep_pjw',
    # Force 'sep_pjw._version'
    'sep_pjw._version',

    # If you suspect a top-level _version is needed as well:
    '_version',
]

binaries = []
# Merge in photutils + sep_pjw binaries
binaries += photutils_binaries
binaries += sep_pjw_binaries

########################################
# The Analysis
########################################
a = Analysis(
    ['setiastrosuiteQT6.py'],
    pathex=[],
    binaries=binaries,
    datas=[
        # Existing data files:
        (directory + '/astroquery/CITATION', 'astroquery'),
        (directory + '/photutils/CITATION.rst', 'photutils'),
        (directory + '/astroquery/simbad/data', 'astroquery/simbad/data'), 
        (directory + '/astropy/CITATION', 'astropy'),
        ('celestial_catalog.csv', '.'),
        ('*.png', '.'),
        ('numba_utils.py', '.'),
        ('imgs', 'imgs'),
        ('spinner.gif', '.'),
        # Possibly explicitly add _version.py if physically present at top-level:
        # (Adjust path if needed.)
        (directory + '/_version.py', '.'),

    ] + dask_data + photutils_data,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'torchvision', 'PyQt5'],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='setiastrosuitemac',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=directory + '/astrosuite.icns',
    onefile=True
)

#app = BUNDLE(
#    exe,  # ✅ FIXED: Include the `exe` entry
#    name='SetiAstroSuite.app',
#    icon='astrosuite.icns',
#    bundle_identifier=None  # Optional: Change to match your app
#)

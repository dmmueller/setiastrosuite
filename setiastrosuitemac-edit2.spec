# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import (
    collect_submodules,
    collect_dynamic_libs,
    collect_data_files,
    collect_all
)

#############################################
# Collect everything we need
#############################################

# 0) Kaleido (Plotly static-image engine)
kaleido_datas, kaleido_binaries, kaleido_hiddenimports = collect_all('kaleido')

# 1) Photutils submodules
photutils_submodules = collect_submodules('photutils')

# 2) sep_pjw submodules & binaries
sep_pjw_submodules = collect_submodules('sep_pjw')
sep_pjw_binaries   = collect_dynamic_libs('sep_pjw')

# 3) typing_extensions code files
typingext_datas = collect_data_files('typing_extensions')

# 4) importlib_metadata back-port
importlib_metadata_datas = collect_data_files('importlib_metadata')

# 5) NUMCODECS (for zfpy extension)
numcodecs_submodules = collect_submodules('numcodecs')
numcodecs_binaries   = collect_dynamic_libs('numcodecs')
numcodecs_datas      = collect_data_files('numcodecs')

#############################################
# Build up hiddenimports and binaries
#############################################
binaries = []
binaries += sep_pjw_binaries
binaries += kaleido_binaries
binaries += numcodecs_binaries

hiddenimports = []
hiddenimports += photutils_submodules
hiddenimports += ['sep_pjw', '_version']
hiddenimports += sep_pjw_submodules
hiddenimports += kaleido_hiddenimports
hiddenimports += [
    'typing_extensions',
    'importlib_metadata',
    'numcodecs',           # ensure the package is there
    'numcodecs.zfpy',      # explicit for the zfpy extension
]
directory = './.venv/lib/python3.*/site-packages'

#############################################
# Data collection
#############################################
datas=[
    (directory + '/astroquery/CITATION', 'astroquery'),
    (directory + '/photutils/CITATION.rst', 'photutils'),
    ('celestial_catalog.csv', '.'),
    ('*.png', '.'),
    ('*.icns', '.'),
    ('numba_utils.py', '.'),
    ('imgs', 'imgs'),
    ('spinner.gif', '.'),
    (directory + '/astroquery/simbad/data', 'astroquery/simbad/data'),
    (directory + '/astropy/CITATION', 'astropy'),
    (directory + '/_version.py', '.')
]

# Append other package data
from PyInstaller.utils.hooks import collect_data_files as _cdf

datas += _cdf('dask', include_py_files=False)
datas += _cdf('photutils')
datas += typingext_datas
datas += importlib_metadata_datas
datas += kaleido_datas
datas += numcodecs_datas    # <-- ensure .so and support files for numcodecs

#############################################
# Build the spec
#############################################
a = Analysis(
    ['setiastrosuiteQT6.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['fix_importlib_metadata.py'],  # leave your metadata‐shim hook
    excludes=['torch', 'torchvision'],
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
    icon=directory + './astrosuite.icns',
    onefile=True
)

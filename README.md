# FieldCreator #
## pip install ##
  pip install kivy


### Примечания ###
#### Создание exe ####
1. python -m PyInstaller --onefile --windowed --name Name Name.py
---

Возможно понадобится:

- python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*


- python -m pip install kivy_deps.gstreamer==0.1.*


- python -m pip install kivy_deps.angle==0.1.*


- python -m pip install kivy==1.11.1


---

 После зоздания файла появится файл с расширением spec
 
 
2. В его начало добавить: from kivy_deps import sdl2, glew
3. exe должно быть такого вида:

```python
  exe = EXE(
    pyz, Tree('E:\\Programming\\Python\\WEb\\'),
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
	*[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    name='FildsCreator',
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
)

```

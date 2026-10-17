"""Stage only declared raw sources from original packages. No destructive overwrites."""
from pathlib import Path
from zipfile import ZipFile
import shutil
from .common import ROOT,config,source,reportdir,dump_json,sha256


def safe_copy(origin,destination):
    if destination.exists():
        if sha256(origin)==sha256(destination):return 'existing_identical'
        raise ValueError(f'Archivo con mismo nombre pero contenido diferente: {destination}; resolver manualmente')
    destination.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(origin,destination)
    return 'copied'


def stage(root=ROOT):
    root=Path(root);cfg=config(root/'configs/project.yml')
    inbox=root/'data/private/inbox';inbox.mkdir(parents=True,exist_ok=True)
    raw=root/'data/private/raw';raw.mkdir(parents=True,exist_ok=True)
    entries={}
    for key in ('sites','mincul_delimitados','mincul_declarados','grid_250m','grid_50m'):
        name=cfg['source_files'][key];src=inbox/name
        entries[key]=safe_copy(src,raw/name) if src.exists() else ('already_present' if (raw/name).exists() else 'MISSING')
    zip_for_dem=next(iter(sorted(inbox.glob('todo para mapas*.zip'))),None)
    if zip_for_dem:
        with ZipFile(zip_for_dem) as z:
            candidates=[n for n in z.namelist() if n.endswith('/DEM_vallebajo.tif')]
            if candidates:
                dest=raw/cfg['source_files']['dem']
                if not dest.exists():
                    with z.open(candidates[0]) as src,dest.open('wb') as target:
                        shutil.copyfileobj(src,target)
                    entries['dem']='extracted'
                else:entries['dem']='already_present'
    zip_for_water=next(iter(sorted(inbox.glob('Modelo con distancia a cuerpos de agua*.zip'))),None)
    if zip_for_water:
        with ZipFile(zip_for_water) as z:
            for n in z.namelist():
                basename=Path(n).name
                if basename.startswith(('Acequias_antiguas.','Rios_vallebajoCañete.')) and basename.lower().endswith(('.dbf','.shp','.shx','.prj','.cpg')):
                    dest=raw/basename
                    if not dest.exists():
                        with z.open(n) as src,dest.open('wb') as target:shutil.copyfileobj(src,target)
                        entries[basename]='extracted'
    for key in ('dem','acequias','rios'):
        if key not in entries: entries[key]='present' if source(key,cfg,root).exists() else 'MISSING'
    dump_json(reportdir(root)/'00_fuentes.json',entries)
    print('Preparación de fuentes:',entries)
    return entries

# Lower Cañete Valley — Archaeological Predictive Modelling

**A reproducible reconstruction of archaeological inventories, spatial data and field-independent labels for a proposed JCAA paper.**

> **Estado: ETAPA 1 · Reconstrucción de fuentes, inventario y grillas (verificada).**
> Esta entrega es el **paquete completo de trabajo LOCAL**: incluye originales y resultados privados en `data/private/`, además de código y documentación. Para subir el proyecto a GitHub público, las ubicaciones quedan fuera mediante `.gitignore`.
> El entrenamiento de modelos, la validación espacial y la integración con corredores están bloqueados hasta resolver la procedencia individual de registros y el soporte territorial común.

## Alcance y contribución

Este repositorio reelabora los datos y modelos predictivos de la tesis de Dina S. Cornejo Meza sobre el valle bajo de Cañete y prepara una comparación con el repositorio independiente [canete-corridor-model](https://github.com/javier-vz/canete-corridor-model). El estudio plantea cómo modelar evidencias arqueológicas usando inventarios incompletos sin confundir **falta de registro** con **ausencia verificada**.

Los **188 registros puntuales** de `sitios_unificados_con_latlon.csv` son anteriores a las dos salidas de campo de Dina, de acuerdo con la confirmación del equipo. El CSV carece de fuente institucional por fila. **No se asigna automáticamente MINCUL ni PAVC a ningún punto.** La coincidencia espacial con las capas de MINCUL es una pista para revisión documental, no una identificación de fuente.

## Instalación (Anaconda Prompt, Windows)

```bat
conda env create -f environment.yml
conda activate canete-jcaa
```

## Datos incorporados en esta entrega

Esta versión contiene los materiales originales del usuario, organizados y **sin cambios de contenido**:

- `data/private/inbox/`: siete fuentes necesarias para reproducir los scripts 00–04 (188 puntos unificados, KMZ MINCUL, grillas históricas y ZIP del DEM e hidrografía).
- `data/private/raw/`: fuentes SIG extraídas y originales de trabajo ya preparados por el script 00.
- `data/private/archive/campo/`: hojas de observaciones, KM(L) de Nueva Esperanza y Cuiva, y ZIP de la primera salida.
- `data/private/archive/historicos/`: cinco cuadernos de los modelos originales, reunidos en su ZIP.
- `data/private/derived/`: inventario maestro, dos grillas recalculadas y soporte territorial común **candidato** de 802 km².
- `reports/private/`: auditorías de las etapas 00–04.
- `metadata/input_manifest.json`: tamaños y huellas SHA-256 para comprobar integridad sin exponer coordenadas.

No se incluye `sitios_mc.gpkg` porque corresponde a Chachapoyas. Se omite la segunda copia idéntica de `grilla_modelo1_versionfinal.csv`, y la copia previa del ZIP hidrológico si sus miembros son idénticos.

**Aviso:** la presencia de datos locales dentro del ZIP no significa que sean públicos o autorizados para redistribución. Los recursos de MINCUL, PAVC y registros de campo requieren revisión de permisos antes de subir archivos geoespaciales a GitHub.

La carpeta `data/private/` está excluida del versionado por `.gitignore`; los datos se incorporan al **ZIP descargable** para reproducir los análisis localmente, no al Git público. Al clonar GitHub, será necesario proporcionar los datos por el canal autorizado.

Para verificar los archivos que recibiste y repetir las auditorías desde fuentes originales:

```bat
python scripts\00_verificar_datos.py
python scripts\00_preparar_fuentes.py
```

### Ejecutar

```bat
python scripts\00_preparar_fuentes.py
python scripts\01_reconstruir_inventario.py
python scripts\02_regenerar_grillas.py
python scripts\03_auditar_historicos.py
python scripts\04_soporte_comun_candidato.py
python -m unittest discover -s tests -v
```

El código mantiene las fuentes originales intactas. Todas las salidas con ubicaciones se guardan en `data/private/derived/`; los reportes detallados en `reports/private/`. Estas rutas están excluidas de Git por `.gitignore`.

## Qué se recalcula

1. **Inventario previo:** 188 registros → identificadores persistentes PRE-0001…PRE-0188; columnas de procedencia no resuelta, cronología, control de coordenadas y relación espacial candidata con MINCUL.
2. **Capas ambientales:** altitud y pendiente desde `DEM_vallebajo.tif`, descartando NoData y bordes sin vecinos válidos. Distancia aproximada al río y a acequias mediante rasterización de las geometrías sobre la malla del DEM y transformada de distancia; no sustituye distancias vectoriales exactas.
3. **Grilla 50 m y grilla 250 m:** dos definiciones de presencia: (a) celda que contiene/intersecta un punto anterior, (b) celda con centro a ≤30 m de un punto (reproducción de regla histórica). El resto permanece **SIN ETIQUETA**, no «sin sitio» demostrado.
4. **Auditoría histórica:** comparación exacta contra etiquetas originales, sin utilizarlas para reconstruir las nuevas.

### Qué significa «reconstruir desde cero» en esta versión

Por defecto, `grid_mode: historical_mask`: se reutilizan **solo las coordenadas de las celdas como soporte espacial**, y se recalculan las etiquetas y variables desde fuentes independientes. **No se reutilizan columnas ambientales, etiquetas, predicciones, SMOTE ni probabilidades históricas.** Así las cifras se pueden comparar directamente y auditar.

Para reconstruir también **la malla y máscara territorial** completamente desde un polígono aprobado, cambia en `configs/project.yml`:

```yaml
analysis:
  grid_mode: polygon
  approved_study_polygon: "data/private/raw/area_estudio_aprobada.gpkg"
```

El script genera ambas cuadrículas ancladas a coordenadas UTM, recorta por los centros de celda interiores al polígono y registra sus nuevas extensiones. **No se ha seleccionado un polígono definitivo**: el shapefile administrativo recuperado cubre ~1551 km², mientras que el dominio de corredores cubre 801,625 km². Imponer uno sin justificarlo alteraría el objeto de estudio.

## Archivos de salida (PRIVADOS)

```text
data/private/derived/
  inventario_maestro_previo_PRIVADO.csv
  revision_procedencia_y_coordenadas_PRIVADO.csv
  grilla_recalculada_50m_PRIVADA.csv.gz
  grilla_recalculada_250m_PRIVADA.csv.gz
  grilla_50m_soporte_comun_802km2_CANDIDATA_PRIVADA.csv.gz
reports/private/
  00_fuentes.json
  01_inventario.json
  02_grillas_recalculadas.json
  03_revision_historicos.json
  04_soporte_comun_CANDIDATO.json
```

**Publicación responsable:** no incluir CSV originales, polígonos, puntos GPS, fotos ni rasters derivados georreferenciados sin verificar permisos del MINCUL y del PAVC. Ni siquiera el resumen agregado debe subirse sin revisión. Este repositorio entrega el código público; los datos se manejan localmente.

### Máscara común candidata (sin decisión definitiva)

El script 04 intersecta el dominio de corredores de 250 m con los centros de las celdas de 50 m. El solapamiento es **320 576 celdas de 50 m = 801,44 km²**, muy próximo a los 801,625 km² de la malla gruesa. Produce una tabla con la celda contenedora de 250 m (`parent_250m_cell_id`). **Es una propuesta de comparación, no la delimitación científica aprobada.**

## Próximas etapas (todavía NO ejecutadas)

- **2 · Conciliación documental:** identificación por nombre/código MINCUL y por cuaderno PAVC; deduplicación conceptual sitio vs evidencia; versión arqueológica congelada antes de las salidas.
- **3 · Soporte común 50/250 m:** delimitar área, escoger unidad de análisis y construir particiones espaciales; controlar registros compartidos y presencias colindantes.
- **4 · Modelos:** reglas ambientales, RF sin filtración, PU/presencia-fondo cuando se justifique, calibración y evaluación espacial anidada.
- **5 · Corredores:** integrar campos E, T, F y L en comparación reproducible con un commit fijado del repositorio independiente.
- **6 · Campo:** alertas, evidencia y fotografías de Dina separadas de todos los procesos de entrenamiento y selección.

## Estructura

```text
configs/project.yml             Parámetros y fuentes
src/canete_rebuild/             Código de inventario, georreferenciación y auditoría
scripts/                        Entradas independientes y verificables
tests/                          Pruebas sintéticas sin coordenadas reales
docs/                           Decisiones y resultados auditados
data/private/                   Datos originales y derivados excluidos de Git
reports/private/                QA con metadatos sensibles, excluido de Git
```

## Conceptos principales

**Punto de registro ≠ sitio único**. **Intersección con MINCUL ≠ fuente ministerial confirmada**. **Cuadrícula no etiquetada ≠ ausencia arqueológica**. **Buffer de 30 m ≠ presencia verificada en toda la superficie de la celda**. **Validación retrospectiva de visitas dirigidas ≠ estimación imparcial de la prevalencia en todo el valle**.

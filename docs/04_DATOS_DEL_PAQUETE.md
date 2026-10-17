# Datos incorporados y límites de uso

**Ámbito:** Valle bajo de Cañete, reconstrucción previa al trabajo de campo y materiales históricos. El archivo `sitios_mc.gpkg` de Chachapoyas se excluye deliberadamente.

## Procedencia

1. **Inventario anterior a Dina:** `sitios_unificados_con_latlon.csv` contiene 188 puntos de MINCUL y PAVC, disponibles antes de las dos salidas de campo de Dina, según confirmación del equipo. Los orígenes individuales MINCUL/PAVC aún no están identificados documentalmente y no se infieren automáticamente por proximidad.
2. **MINCUL:** `delimitados(1).kmz` y `declarados(1).kmz` son capas distintas. La coincidencia geométrica sirve para la auditoría, pero no asigna la procedencia de cada punto.
3. **Grillas históricas:** `grilla_modelo1_versionfinal.csv` y `grilla_codigo2.csv` se conservan como evidencia de las versiones anteriores, no como fuente de etiquetas de entrenamiento del modelo nuevo.
4. **Ambientales:** DEM, ríos y acequias en los archivos históricos de mapas y cuerpos de agua. El script 00 extrae los insumos requeridos en `raw/`.
5. **Observaciones de campo:** el Excel `Prospeccion puntos.xlsx`, las dos versiones de la hoja `Puntos l_l 2 ida a campo`, KML de Cuiva/Nueva Esperanza y el ZIP de primera salida permanecen en `archive/campo/` hasta verificar fechas y roles de observación. Su presencia en el paquete **no los añade automáticamente al entrenamiento**.
6. **Cuadernos originales:** cinco notebooks Jupyter en el ZIP de código se conservan para auditoría histórica y no son ejecutados por el pipeline nuevo.

## Integridad

El manifiesto `metadata/input_manifest.json` incluye ruta relativa, tamaño y SHA-256 de cada original incorporado. Ejecuta `python scripts\00_verificar_datos.py` antes de correr los análisis. Los outputs derivados están también incluidos, pero deben recalcularse cuando se aprueben cambios a la máscara territorial o al inventario.

## Advertencias

- El paquete íntegro es **privado para trabajo local**. Aun con los archivos dentro de `data/private/`, `.gitignore` impide publicarlos por accidente mediante Git.
- Una celda sin registro arqueológico permanece sin etiqueta, no es evidencia de ausencia.
- La comparación 50/250 m sigue siendo **candidata**, no definición final aprobada.
- Las hojas de campo siguen pendientes de normalización y asignación cronológica detallada.
- No publicar coordenadas arqueológicas puntuales, tablas con coordenadas, archivos SIG, fotos GPS ni derivados de precisión sin revisar permisos y riesgos de patrimonio.

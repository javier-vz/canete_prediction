# Decisiones siguientes antes del reentrenamiento

**A. Dominio común (PRIORIDAD ALTA).** Requerimos fijar un polígono de área de estudio aprobada por el equipo. Hoy la grilla del RF fino cubre ~1551 km² y la de corredores ~802 km². Se puede recortar ambos modelos a la intersección o adoptar un dominio común justificado, pero no confundir resultados calculados en extensiones diferentes.

**B. Separación de fuentes (PRIORIDAD ALTA).** Resolver la procedencia MINCUL/PAVC por identificadores; archivo de 188 solo contiene coordenadas. Evitar deduplicación solo por proximidad. Los 188 antecedentes no se alteran sin registro de cambios.

**C. Tipología y geometría (PRIORIDAD ALTA).** Decidir qué constituye `site` para el resultado central; puntos de cerámica, muros, sitios con polígono delimitado y estaciones deben distinguirse. Una clasificación binaria sin esta decisión puede ser metodológicamente engañosa.

**D. Cronología (CONFIRMADA GLOBALMENTE).** Los 188 antecedentes preceden la validación de Dina. Revisar cuadernos originales para confirmar que no hubo otro reentrenamiento de predicciones después de campo. Mantener las observaciones posteriores en otra entidad.

**E. Etiquetas (PRIORIDAD ALTA).** Recomiendo como principal la presencia explícita en celda con protocolo de incertidumbre posicional y, como robustez, buffers razonables (15, 30, 50 m). Los ceros son no etiquetados; diseñar evaluación presencia-fondo o positivas/no etiquetadas apropiada.

**F. Recalcular ambiente (EN CURSO).** DEM revisado con NoData; ríos y acequias aproximados por rasterización; faltan geometrías/fechas institucionales exactas del contexto hidráulico para el análisis arqueológico final.

**G. Entrenamiento (BLOQUEADO).** Una vez resuelto A–F, RF sin filtración, nulos ambientales, fondo accesible y validación espacial por sitios/bloques. Solo después evaluar capas de corredores E/T/F/L.

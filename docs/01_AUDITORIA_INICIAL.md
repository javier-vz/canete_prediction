# Auditoría inicial de materiales originales — 16 de octubre de 2026

Esta ficha describe únicamente lo inspeccionado de los archivos enviados. Es **diagnóstico**, no procesamiento definitivo.

## Materiales identificados

| Fuente | Hallazgo verificable | Implicación |
|---|---|---|
| `grilla_modelo1_versionfinal.csv` | 12 826 filas; 144 X únicos, 93 Y únicos con salto de 250 m; 84 celdas `presencia_sitio_nuevo=1` | Grilla histórica 250 m, muy cercana en escala/cantidad a la del paper de corredores. Confirmar coincidencia geométrica antes de fusionar. |
| `grilla_codigo2.csv` | 620 296 filas; salto típico 50 m; 196 celdas `label=1` | Su área y máscara difieren de las del modelo anterior: no comparar métricas directamente. |
| `todo para mapas...zip` | Contiene `grilla_final_modelo_logistico.csv` (idéntico a la grilla M1), 188 puntos unificados en un CSV filtrado, imágenes y DEM | Material mezclado de análisis, mapas y fuentes; promover solo las fuentes comprobadas. |
| `Modelo con distancia...zip` | Dos ZIP de 29 miembros con igual lista y CRC por miembro; incluye grillas derivadas y capas hidrológicas | Archivar una copia lógica de contenidos, conservar los dos ZIP originales y sus hashes en privado. |
| `Código con agua y puntos...zip` | Cinco cuadernos Colab, entre ellos `Grilla.ipynb` y `V2.ipynb` | Preservar como referencia histórica; reconstruir scripts con pruebas. |
| `primera salida...zip` | Incluye hoja con 9 visitas y materiales SIG y KML | Separar visita, observación, fotos, recorrido y alerta previa. |
| `Puntos l_l 2 ida a campo(2)/(3).xlsx` | Ambas hojas muestran 22 registros y los mismos valores visibles; 17 `Predicho=si`, 5 `Predicho=no` | Crear un libro normalizado con 22 visitas y distinguir alertas/observaciones adicionales. |

## Alertas técnicas **confirmadas**

1. `V2.ipynb` ejecuta `SMOTE.fit_resample()` antes de `train_test_split()`. El test queda contaminado por ejemplos sintéticos derivados del dataset completo.
2. `Grilla.ipynb` forma la clase positiva con buffers de **30 m** alrededor de puntos de sitio; la definición cambia de la simple intersección puntual citada en parte de la tesis.
3. `Grilla.ipynb` calcula `dist_sitio_mas_cercano` con `cKDTree` a partir del listado completo de 188 ubicaciones. La variable no se puede trasladar tal cual a una evaluación fuera de muestra de esos mismos sitios.
4. M1 y M2 tienen diferentes escalas (250 y 50 m), coberturas y etiquetas (84 frente a 196 positivas).
5. En M2 aparecen **281 celdas con altitud <= -1000 m**, valor mínimo -32768 (probable NoData); **2 029 celdas con pendiente >= 70°**. Se requiere reproducir máscara DEM, agregación, recorte y cálculo de pendiente.
6. Las predicciones de la tesis se mezclan en carpetas con puntos de visitas posteriores. Es imprescindible fechar los conjuntos de entrenamiento y congelar las predicciones pre-campo.
7. Existen shapefiles aparentemente incompletos: algunos `.shp` carecen de `.shx` en el paquete; reconstruir u obtener sus índices antes de usar (sin alterar fuentes de origen).

## Cuestiones abiertas, documentadas y **no asumidas**

- Origen exacto de las 84 celdas positivas de M1 y su coincidencia con los 84 sitios del paper de corredores.
- Relación de los 188 puntos unificados con las 196 celdas positivas de M2; distancia de asociación, duplicados, temporales y fuentes.
- Fecha y procedencia de los sitios incorporados en `presencia_sitio_nuevo` y en `label`.
- Si los puntos de campo figuran en las etiquetas usadas para entrenar los modelos que se validaron con ellos.
- ¿Qué es exactamente la máscara de M1, la de M2 y su intersección?
- Capas de río y acequias: fuentes, fechas, transformación, registros antiguos vs actuales.
- Posibles hojas de observación campo más completas, recorridos GPS, fotos completas y permisos.
- Fecha/commit reproducible del repositorio de corredores.

## Decisión científica

Reproducir lo histórico para auditoría, pero **crear de nuevo** registro, máscaras, variables y modelos con controles de fuga, cronología y validación espacial. Publicar solo resultados recalculados bajo protocolo explícito.

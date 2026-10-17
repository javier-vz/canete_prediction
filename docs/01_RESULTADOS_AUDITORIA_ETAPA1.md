# Resultado de auditoría ejecutada — 17 de octubre de 2026

## Fuentes verificadas

- `sitios_unificados_con_latlon.csv`: **188 filas, 188 coordenadas UTM únicas**, 0 discrepancias superiores a 5 m entre UTM y latitud/longitud reproyectadas. Por confirmación del equipo, **todos estos puntos anteceden a las dos salidas de campo de Dina**.
- `delimitados(1).kmz`: **10 923 elementos nacionales**, geometrías usadas exclusivamente para coincidencias espaciales; `declarados(1).kmz`: **5889 elementos**. Se mantienen como fuentes distintas.
- 26/188 puntos están dentro o a menos de 100 m de alguna geometría ministerial. Los restantes 162 no tienen coincidencia a ese umbral. **Esto no convierte a los 162 en registros PAVC probados**, ni resuelve la institución de origen de los otros 26.
- DEM `DEM_vallebajo.tif`: EPSG:32718; píxel ~30,96 m; NoData -32768. Los vectores de ríos y acequias son fuentes separadas.

## Reconstrucción sobre soporte histórico (temporal y explícita)

| Indicador | 250 m | 50 m |
|---|---:|---:|
| Celdas | 12 826 | 620 296 |
| Área nominal de celdas | 801,625 km² | 1550,74 km² |
| Registros previos con punto dentro de la grilla | 171 | 184 |
| Registros previos fuera de la máscara | 17 | 4 |
| Celdas que intersectan punto previo (borde incluido) | 182 | 183 |
| Celdas cuyo centro dista ≤30 m de punto previo | 6 | 196 |
| Positivos de las etiquetas históricas | 84 | 196 |
| Celdas que difieren: etiqueta histórica vs buffer centro-30 m | 88 | **0** |
| Elevaciones ausentes o NoData del DEM | 0 | 281 |
| Pendientes sin vecinos válidos para derivada 3×3 | 4 | 2919 |

**Resultado de reproducibilidad central:** en la grilla de 50 m, las 196 etiquetas positivas históricas son **exactamente las mismas 196 celdas** reconstruidas con distancia del centro a un punto del inventario previo ≤30 m. Se comprobó igualdad fila a fila (620 296/620 296).

**Diferencia central:** los 84 positivos de la grilla de 250 m no son equivalentes a los puntos del inventario maestro de 188 registros. Hay 78 celdas positivas antiguas con punto previo contenido por la nueva definición, pero cambiar etiquetas no equivale a validar la etiqueta histórica.

## Dominio común candidato

Se identificaron **320 576 celdas de 50 m**, equivalentes a **801,44 km²**, cuyos centros se encuentran dentro de celdas del dominio de 250 m. Esta intersección espacial recupera casi toda la extensión de 801,625 km² del trabajo de corredores, pero pierde cerca de la mitad de la superficie del RF fino. Se preserva un archivo privado de esta selección, con identificador de la celda madre de 250 m, para la futura comparación. Esta selección aún requiere aprobación arqueológica como ventana científica de estudio.

## QA ambiental

El nuevo proceso lee el DEM de origen, evita usar `-32768` como altitud y calcula pendiente desde un entorno local válido. En 50 m se conservan 281 valores NoData en elevación y se dejan 2919 celdas sin pendiente válida, evitando imputación arbitraria. La pendiente máxima no nula producida es ~70,91° (frente a más de 2000 pendientes >85° en la grilla histórica, pendientes que requieren revisión del método previo).

Las distancias hidrológicas son nuevas aproximaciones sobre el raster nativo del DEM; para comparación de efectos próximos a acequias se recomienda derivar más adelante distancias vectoriales exactas, e incorporar temporalidad de la red hidráulica.

## Cinco asuntos sin cerrar

1. **Procedencia por punto:** identificación documental MINCUL/PAVC y posible doble contabilización de un mismo sitio mediante varias observaciones.
2. **Geometría de sitio:** distinguir punto representativo, evidencia arqueológica y perímetro de sitios; evaluar el uso de polígonos oficiales sin convertir sus vértices en sitios independientes.
3. **Dominio:** la grilla gruesa y la fina representan **territorios diferentes** (~802 vs ~1551 km²). No comparar modelos hasta elegir soporte común.
4. **Registros atípicos:** cuatro puntos quedan fuera de la máscara fina; inspeccionar sus originales, no corregir ni eliminar automáticamente.
5. **Observaciones posteriores:** las visitas de Dina, descubrimientos incidentales y reentrenamientos posteriores se mantienen completamente separados hasta documentar las fechas y el flujo.

## Estado final

**Etapa 1 completada para el inventario puntual previo y recálculo ambiental sobre máscaras heredadas.** La atribución MINCUL/PAVC y la **nueva máscara final** quedan abiertas antes de pasar a entrenamiento y comparación.

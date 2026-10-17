# Modelo conceptual y criterios de etiquetas

## Entidades de información (evitar falsas equivalencias)

| Entidad | Definición | Regla |
|---|---|---|
| `source_record` | Fila o entidad individual de un archivo fuente | ID inmutable `PRE-nnnn`; conservar archivo/hoja/fila original |
| `archaeological_observation` | Registro arqueológico puntual con descripción, lugar y fecha | Exigir evidencia documental para tipificar |
| `archaeological_site` | Entidad arqueológica que puede contener múltiples observaciones | Identidad por código/atributos y comprobación experta, no proximidad exclusivamente |
| `official_delimitation` | Polígono ministerial | Mantener geometría y código oficial independientes |
| `survey_visit` | Visita de validación posterior | Siempre excluida del entrenamiento original |
| `grid_cell` | Unidad espacial para el modelo | Resolución, máscara, rejilla, identificador y CRS explícitos |

## Control de procedencia

El CSV de 188 puntos aporta `x, y, lat, lon`, **sin nombres, fechas o identificador institucional por fila**. La afirmación global del equipo sobre cronología previa queda registrada como metadato del conjunto. La relación espacial con SIGDA se guarda como `mincul_*_distance_m` y `mincul_spatial_candidate`; nunca rellena `source_group` automáticamente.

La conciliación nominal con Cuiva, Nueva Esperanza o `Prospeccion puntos.xlsx` se documentará en la siguiente etapa porque un punto del cuaderno puede ser un hallazgo, un vértice o una estación de campo. Una correspondencia posicional no basta para tipificarlo.

## Etiquetas construidas

- **`recorded_point_in_cell`**: un punto del inventario previo cae dentro o justo sobre el borde de una celda. La misma observación puede tocar 2–4 celdas si está en borde; por ello el número de celdas positivas no es igual al número de sitios.
- **`legacy_30m_centroid_buffer`**: el centro de la celda está a 30 m o menos de un punto. Reproduce la regla del archivo histórico fino: **no indica presencia observada en esa celda**.
- **`background_status=UNLABELLED_NOT_CONFIRMED_ABSENCE`**: en todas las celdas sin evidencia positiva no hay negativa arqueológica confirmada. La ausencia documentada solo puede proceder de una prospección con protocolo y esfuerzo registrados.

**Riesgo de fuga de información eliminado del modelo base:** no se entrega al clasificador una variable derivada de la distancia a los mismos sitios que definen la etiqueta, ni se usa SMOTE antes de partir espacialmente.

## Covariables y cautelas

`altitud_m` y `pendiente_grados` proceden del DEM aportado. `dist_rio_m_aprox` y `dist_acequia_m_aprox` son aproximaciones discretizadas (a la resolución del DEM) de líneas vectoriales; la comparación científica final deberá documentar el cambio respecto a las distancias exactas históricas y qué canales son prehispánicos o actuales.

Las coordenadas x/y se mantienen **para localizar las celdas**, pero no constituyen variables predictoras predeterminadas del nuevo modelo. La calidad arqueológica y temporal del inventario se revisará antes de dividir sitios entre particiones espaciales.

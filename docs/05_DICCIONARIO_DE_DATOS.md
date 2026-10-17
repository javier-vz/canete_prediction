# Diccionario preliminar de datos

Los campos reflejan archivos reales recuperados; la interpretación arqueológica exacta requiere validación.

| Campo original | Archivo | Lectura operacional |
|---|---|---|
| `X`, `Y` | modelo 1 | Centros de celdas en coordenadas proyectadas; verificar CRS, origen y geometrias |
| `presencia_sitio_nuevo` | modelo 1 | Etiqueta positiva en 84 celdas; reconstruir fuente y temporalidad |
| `distancia_sitios_nuevos` | modelo 1 | Distancia al registro de evidencias nuevas; posible circularidad si esos datos son el objetivo o validación |
| `distancia_mincul` | modelo 1 | Distancia a inventario conocido; requiere versión del inventario compatible con partición |
| `altitud`, `pendiente` | ambas | Valores DEM; auditar NoData, pendiente extrema y método de derivación |
| `x`, `y` | modelo 2 | Puntos centrales en grilla de paso 50 m |
| `label` | modelo 2 | Etiqueta positiva en 196 celdas; cuaderno original usa buffer de 30 m alrededor de 188 puntos |
| `dist_acequia`, `dist_rio` | modelo 2 | Distancia a capas hidrológicas; documentar cada geometría, fecha y permisos |
| `dist_sitio_mas_cercano` | modelo 2 | Distancia a la lista completa de puntos: predictor retrospectivo potencialmente filtrado |
| `Predicho` | libro campo 2 | Marca de punto programado como alerta vs hallazgo adicional, según tabla; verificación necesaria |
| `Es sitio` | libros campo | Categorías mixtas (`si`, `no`, `cerámica`, `lítico`, texto abierto); codificar con reglas explícitas y revisión de Dina |

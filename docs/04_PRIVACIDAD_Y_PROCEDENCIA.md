# Privacidad, procedencia y divulgación

- Las ubicaciones arqueológicas, fotos geoetiquetadas, KML/GPX, listas de sitios, capas con evidencia y tablas de observación se guardan exclusivamente en `data/private/`, fuera de control de versiones.
- El script de organización registra hashes en `reports/private/`; ni hashes ni nombres de originales tienen que aparecer en publicaciones sin propósito documentado.
- Las salidas públicas agregadas se autorizan individualmente. No publicar grillas con `presencia=1` si permiten reconstruir puntos sensibles por su resolución o geometría.
- Conservar copia original inmutable en privado, atribución MINCUL y PAVC y permisos antes de liberar insumos o resultados derivados.
- Los notebooks originales solo se consultan; no ejecutarlos sin revisión porque contienen rutas absolutas, código antiguo y pasos metodológicos no validados.
- Mantener manifiesto privado de proveniencia: fuente → versión SHA256 → procesamiento → salida, con fecha, software, CRS y definición de etiqueta.

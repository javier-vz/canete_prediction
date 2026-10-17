# Cañete — Predicción arqueológica y validación espacial

Repositorio de reconstrucción y análisis científico de modelos de prospección en el valle bajo de Cañete (Perú), derivado de la tesis de Dina Soledad Cornejo Meza. Proyecto independiente del código del modelo de corredores.

**Estado actual: ETAPA 0 / Auditoría de fuentes.** Este repositorio contiene estructura, auditoría reproducible y decisiones pendientes; **todavía no reproduce modelos ni cifras de desempeño**. Los resultados de la tesis son antecedentes, no métricas validadas por este proyecto.

## Pregunta científica

¿Cuándo un modelo entrenado con inventarios arqueológicos incompletos genera una priorización espacial defendible, y cuánto aporta frente a predictores ambientales sencillos y frente a superficies de circulación simulada?

## Material que hemos recuperado (inventario preliminar)

- Modelo 1: `grilla_modelo1_versionfinal.csv`, **12 826 celdas de 250 m**, 84 celdas positivas (campo `presencia_sitio_nuevo`).
- Modelo 2: `grilla_codigo2.csv`, **620 296 filas** en grilla nominal de 50 m, 196 positivas (`label`); contiene anomalías de altitud y pendiente que se deben auditar.
- Un archivo con **188 puntos unificados** (`sitios_unificados_filtrados.csv`) dentro de `todo para mapas...zip`; validar procedencia y duplicados antes de usarlo.
- Cuadernos originales de Google Colab (`Grilla.ipynb`, `V2.ipynb`, etc.), capas SIG, mapas y salidas de campo. Guardarlos privados como patrimonio metodológico; reconstruir el nuevo pipeline como scripts probados.
- Primer reconocimiento: tabla con 9 filas. Segundo: tabla con 22 registros (17 marcados como predichos y 5 no predichos). Las categorías arqueológicas de la hoja requieren codificación explícita.

Detalles y advertencias en [docs/01_AUDITORIA_INICIAL.md](docs/01_AUDITORIA_INICIAL.md).

## Arranque rápido en Windows (Anaconda Prompt)

Descomprimir este repositorio, abrir Anaconda Prompt en la carpeta y ejecutar:

```bat
python scripts\00_inventario.py
python -m unittest discover -s tests -v
```

El inventario funciona con Python estándar, sin instalar paquetes. Para el futuro pipeline espacial:

```bat
conda env create -f environment.yml
conda activate canete-prediction
```

Copiar los ZIP, CSV y XLSX originales **sin descomprimirlos** dentro de `data/private/inbox/` y ejecutar:

```bat
python scripts\00_organizar_fuentes.py
python scripts\00_inventario.py
```

El organizador calcula SHA-256, detecta duplicados exactos y mueve cada fuente a una carpeta privada. **Nunca reemplaza ni modifica el contenido** de los originales. Produce manifiestos en `reports/private/`, excluidos de GitHub. Revisar los informes antes de avanzar.

## Plan de trabajo acordado

| Etapa | Propósito | Producto / condición de salida |
|---|---|---|
| 0 | Inventario y procedencia | Fuentes identificadas, hashes, duplicados y permisos documentados |
| 1 | Reconstrucción arqueológica | Inventario por entidad y fecha, sin etiquetas de campo retrospectivas |
| 2 | Reconstrucción SIG | DEM, agua, acequias, grillas 50/250 m y máscaras auditadas |
| 3 | Predicción supervisada | Reproducción histórica separada y nueva validación espacial sin fuga |
| 4 | Referencias ambientales | Altitud, pendiente, hidrología y modelos presencia-fondo, métricas comunes |
| 5 | Modelo de corredores | Exportar E/T/F/L desde repositorio externo con commit fijo y reescalar |
| 6 | Observación de campo | Alertas antes del campo, visitas, visibilidad y cobertura, fechas y permisos |
| 7 | Comparaciones | Misma máscara/etiquetas/unidad, curvas de captura y escenarios |
| 8 | Publicación | Figuras, tablas, material suplementario y paquete abierto sin ubicaciones sensibles |

La etapa 1 depende de la revisión de permisos del PAVC y de los registros ministeriales. En la etapa 5 se incorporará el repositorio [canete-corridor-model](https://github.com/javier-vz/canete-corridor-model) por una versión (commit) fija, no por copia informal de carpetas.

## Organización

```text
canete-archaeological-prediction/
├── README.md
├── environment.yml
├── pyproject.toml
├── .gitignore
├── configs/analysis.yml
├── docs/01_AUDITORIA_INICIAL.md
├── docs/02_DISENO_CIENTIFICO.md
├── docs/03_DECISIONES_PENDIENTES.md
├── docs/04_PRIVACIDAD_Y_PROCEDENCIA.md
├── docs/05_DICCIONARIO_DE_DATOS.md
├── scripts/00_organizar_fuentes.py
├── scripts/00_inventario.py
├── src/canete_prediction/{__init__.py,inventory.py,staging.py}
├── tests/test_inventory.py
├── data/private/{inbox,raw,interim,processed}/      [IGNORADO EN GIT]
├── data/public/                               [solo después de revisión ética]
├── reports/private/                          [IGNORADO EN GIT]
├── reports/public/
└── figures/                                   [figuras sin información sensible]
```

## Principios irrenunciables

1. Una etiqueta **sin registro** representa registro desconocido, no ausencia arqueológica comprobada.
2. Distinguir fuentes fechadas antes/durante/después de los recorridos; las visitas de campo nunca deben entrar inadvertidamente en su propio entrenamiento.
3. Separar ajuste y validación por bloques espaciales; cualquier sobremuestreo se hará solo en entrenamiento.
4. Prohibir como predictor estándar distancias a todos los sitios que incluyen los sitios retenidos para evaluación.
5. Publicar solamente productos aprobados y deslocalizados; nunca hojas, KML, fotografías GPS o puntos precisos de sitios.

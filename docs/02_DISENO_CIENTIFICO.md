# Nuevo diseño — paper metodológico para JCAA

**Aporte principal**: cuantificar qué información arqueológica puede recuperarse de un inventario espacialmente sesgado bajo un procedimiento de predicción reproducible y qué evidencia adicional aportan predictores ambientales y campos de circulación.

## Preguntas comprobables

P1. ¿Cuánto se deteriora el rendimiento aparente del RF histórico al evitar SMOTE previo a la partición, predictores derivados del inventario completo y la validación aleatoria por celda?

P2. Bajo una misma unidad espacial y una misma definición cronológica de presencia, ¿RF con variables ambientales supera a referencias ambientales simples (baja altitud, pendiente, cercanía a agua)?

P3. ¿Las superficies E/T/F/L agregan señal predictiva fuera de los predictores ambientales simples? Priorizar una comparación controlada en un soporte común, no una simple tabla de AUC con estudios heterogéneos.

P4. ¿Qué indican los registros de campo originales una vez distinguidas alertas seleccionadas, observaciones adicionales, condición de visibilidad y acceso? Reconocer sesgo de selección, sin interpretar automáticamente una visita sin materiales como ausencia verdadera.

## Flujo propuesto

Fuentes (sitios con fecha + SIG + fotos y visitas) → control calidad/procedencia → geometría y máscaras común → etiquetas temporales → particiones espaciales → predictores ambientales simples → modelos ML entrenados dentro de cada pliegue → evaluación fuera de muestra → superposición de E/T/F/L → análisis de campo retrospectivo → nuevas campañas controladas (opcional) → artículo y depósito reproducible.

## Experimentos mínimos

- A: RF histórico reproducido *solo como auditoría*, resultados originales claramente separados de la inferencia final.
- B: una regla de baja altitud, una o dos reglas ambientales defendibles y RF ambiental entrenado en bloque espacial.
- C: evaluación de sensibilidad con/sin datos de ríos/acequias, manteniendo fijo el resto del pipeline.
- D: predictores de presencia-fondo/PU seleccionados después de documentar intensidad de registro y diseño de fondo; el método debe responder a la pregunta, no aumentar número de modelos por inercia.
- E: campos T/E/F/L y ablaciones (L frente a E, E+F, etc.) sobre intersección territorial con mismos sitios/fecha y misma unidad de muestreo.
- F: observaciones de campo originales como test retrospectivo **solo de modelos previos a esas visitas**; los nuevos modelos se puntúan post hoc, con esta condición explícita.

## Métricas

Curvas de captura de sitios vs área/sector, Top-k a presupuesto espacial fijo, PR-AUC cuando la definición de negativos lo permite, ROC-AUC interpretada explícitamente como presencia vs fondo/no documentado, evaluación por bloque y bandas de incertidumbre derivadas de unidades espaciales independientes. Ajustes de modelos y selección de predictores solo dentro de folds entrenamiento. Comparaciones con bootstrap espacial o por bloques, no bootstrap ingenuo de celdas vecinas.

## Diferenciación del paper de corredores

El artículo de corredores se ocupa de la simulación de conexiones y priorización con información ambiental. El manuscrito nuevo se ocupa de la calidad del registro, la validación predictiva y la incorporación de observaciones de prospección. El segundo recuperará el corredor como **comparador fijado** y como hipótesis complementaria, con atribución clara y sin re-publicar idénticos resultados.

# Memo de negocio: papelería y centro de copias al sur del Tec de Monterrey

**Para:** Emprendedor (cliente simulado) · **De:** Fernando Flores, Analista de Datos · **Fecha:** octubre 2026
**English version:** [business_memo.md](business_memo.md)

## Recomendación

Abrir una **papelería con centro de copias e impresión a 700–800 m al sur / suroeste del Campus Monterrey**, dentro de las tres zonas mejor calificadas que aparecen abajo. **Antes de firmar un contrato de renta**, hacer la validación en campo de 2 semanas que está al final de este memo.

## Por qué

| Evidencia | Dato | Fuente |
|---|---|---|
| Papelerías a 1 km del campus vs. el promedio metropolitano | **6 negocios · 0.37×** (faltan) | DENUE 2026 |
| Copias e impresión a 1 km vs. el promedio metropolitano | **4 negocios · 0.58×** (faltan) | DENUE 2026 |
| Mismas categorías alrededor de la UANL (Ciudad Universitaria) | **1.74× y 5.46×** (sobran) | DENUE 2026 |
| Residentes de 18 a 24 años alrededor de las 3 mejores zonas | **23–25%** vs. **12.1%** en Nuevo León | Censo 2020 |
| Residentes de 18 a 24 años a 6 minutos caminando de cada zona | **1,170–1,300** | Censo 2020 |
| Papelerías o copias a esa misma distancia | **0** | DENUE 2026 |

El hueco es propio de la zona del Tec, no de las universidades en general: alrededor de la UANL esos mismos negocios están por encima del promedio. Los 10 competidores que existen a menos de 1 km son microempresas (0 a 5 empleados), así que no hay una cadena dominante con la cual pelear.

**Qué evitar:** lavanderías (31 a menos de 1 km, 7.1 veces el promedio metropolitano), restaurantes y cafeterías (alrededor del doble). Están saturados.

## Dónde: las 3 mejores zonas

| Lugar | Ubicación respecto al campus | Residentes de 18–24 a 500 m | Competidor más cercano | Coordenadas |
|---|---|---|---|---|
| 1 | 707 m al suroeste | 1,301 | 514 m | [25.6469, -100.2946](https://www.google.com/maps?q=25.646919,-100.294563) |
| 2 | 791 m al sur | 1,240 | 652 m | [25.6446, -100.2921](https://www.google.com/maps?q=25.644625,-100.292091) |
| 3 | 750 m al sur | 1,174 | 576 m | [25.6446, -100.2896](https://www.google.com/maps?q=25.644598,-100.289590) |

El resultado es sólido: **4 de las 5 mejores zonas se mantienen** si en lugar de contar a los jóvenes de 18 a 24 se cuenta a toda la población.

## Riesgos y cómo reducirlos

| Riesgo | Cómo reducirlo |
|---|---|
| El campus puede tener servicios de impresión propios que ya cubren la demanda (no aparecen en el DENUE) | Visitar los puntos de impresión del campus y anotar precios y filas en horas pico |
| Los estudiantes imprimen menos que antes (tareas digitales) | Enfocarse en lo que no se puede hacer en digital: plotter y gran formato, engargolado, materiales para maquetas y arquitectura |
| El Censo cuenta a quien vive en la zona, no a los estudiantes que solo pasan por ahí | Contar el flujo de peatones en cada zona candidata (ver el plan de validación) |
| El DENUE no incluye a los vendedores informales | Recorrer un radio de 500 m alrededor de cada zona y anotar a todos los competidores |
| La renta cerca del campus puede ser alta | Comparar rentas en las 3 zonas; basta un local pequeño (20 a 40 m²) |

## Plan de validación (2 semanas, antes de invertir)

1. **Flujo de peatones:** contar durante 15 minutos a las 8:00, 13:00 y 18:00, en 3 días entre semana, en cada zona candidata.
2. **Recorrido de competidores:** visitar a los 10 competidores cercanos y anotar precios, horarios, servicios y filas en horas pico.
3. **Validar la demanda:** 30 entrevistas cortas a estudiantes. ¿Cada cuánto imprimen o compran material, dónde lo hacen y qué les falta?
4. **Rentas:** buscar locales disponibles y sus precios en las 3 zonas.
5. **Decisión:** seguir adelante si hay buen flujo de gente **y** los estudiantes mencionan necesidades que los servicios del campus no cubren.

## Método en una línea

DENUE de INEGI (173,829 negocios en el área metropolitana de Monterrey) → competencia por distancia y cociente de localización → población del Censo 2020 por AGEB, repartida en una cuadrícula de 250 m → score = residentes de 18 a 24 años a 500 m ÷ (competidores + 1). Análisis completo: [README](../README.md).

*Limitaciones: el DENUE solo registra negocios formales; el Censo es de 2020; los conteos pequeños que INEGI oculta hacen que la demanda salga un poco subestimada; el score mide oportunidad relativa, no rentabilidad.*

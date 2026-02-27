---
description: Ver tendencia temporal de un indicador censal en Puerto Rico
argument-hint: "<variable/tema> de <municipio> [desde <anio>]"
---

Genera una serie temporal para un indicador censal usando $ARGUMENTS.

## Workflow

1. **Parsear argumentos**: Extrae el indicador, la geografia, y opcionalmente el rango de anios. Formatos:
   - "poblacion de Bayamon"
   - "ingreso mediano de Caguas desde 2015"
   - "pobreza de San Juan 2010-2022"

2. **Resolver geografia**: Usa `censo_listar_municipios` o `censo_listar_barrios` para obtener el FIPS.

3. **Identificar variable**: Traduce el indicador a un codigo ACS:
   - "poblacion" → B01003_001E
   - "ingreso mediano" → B19013_001E
   - "pobreza" → B17001_002E
   - Para otros, usa `censo_buscar_variables`

4. **Ejecutar serie**: Llama `censo_serie_temporal` con la variable, geografia, y rango de anios. Este tool incluye MOE automaticamente.

5. **Evaluar calidad**: Verifica el CV de cada anio. Datos de anios mas antiguos o geografias pequenas pueden ser menos confiables.

6. **Presentar resultados**: Tabla temporal con:
   - Anio
   - Estimado y MOE
   - Cambio vs anio anterior (absoluto y %)
   - Confiabilidad de cada punto
   - Resumen narrativo de la tendencia

## Ejemplo

Si $ARGUMENTS = "poblacion de Bayamon desde 2015":
1. Resolver Bayamon → county:021
2. Variable: B01003_001E
3. Llamar censo_serie_temporal(variable="B01003_001E", municipio="021", anio_inicio=2015)
4. Presentar tabla 2015-2022 con tendencia

## Notas

- El ACS 5-Year esta disponible desde 2009 para la mayoria de geografias
- Anios disponibles dependen del dataset — `censo_serie_temporal` maneja esto automaticamente
- Para barrios, solo el ACS 5-Year tiene datos (no hay 1-Year)
- `censo_serie_temporal` incluye MOE automaticamente (a diferencia de `censo_consultar`)

---
description: Comparar datos censales entre dos o mas geografias
argument-hint: "<geo1> vs <geo2> [en <tema>]"
---

Compara datos del Census Bureau entre dos o mas geografias de Puerto Rico usando $ARGUMENTS.

## Workflow

1. **Parsear argumentos**: Extrae las geografias a comparar y el tema opcional. Formatos:
   - "Bayamon vs Carolina"
   - "Bayamon vs Carolina en vivienda"
   - "Vega Baja, Manati y Barceloneta en economia"
   - "barrios de San Juan en poblacion"

2. **Resolver geografias**: Para cada geografia mencionada, usa `censo_listar_municipios` o `censo_listar_barrios` para obtener FIPS codes.

3. **Determinar variables**: Si el usuario especifica un tema, usa las variables del perfil tematico correspondiente. Si no, usa un conjunto default de indicadores clave:
   - Poblacion total
   - Ingreso mediano del hogar
   - Tasa de pobreza
   - Unidades de vivienda

4. **Ejecutar comparacion**: Llama `censo_comparar` con las geografias resueltas y las variables seleccionadas.

5. **Evaluar calidad**: Verifica que los datos de todas las geografias sean confiables. Si alguna tiene CV > 30%, notalo junto al valor.

6. **Presentar resultados**: Tabla comparativa con:
   - Filas = indicadores
   - Columnas = geografias
   - Valores con MOE y confiabilidad
   - Resaltado del valor mas alto/bajo en cada indicador
   - Resumen narrativo de las diferencias principales

## Ejemplo

Si $ARGUMENTS = "Bayamon vs Carolina en vivienda":
1. Resolver: Bayamon → county:021, Carolina → county:031
2. Variables del perfil vivienda: unidades, ocupacion, valor mediano, renta mediana, etc.
3. Llamar censo_comparar
4. Presentar tabla lado a lado con resumen

## Notas

- Maximo recomendado: 5 geografias por comparacion
- Si se comparan barrios de diferentes municipios, incluir el nombre del municipio para claridad
- Si se pide "barrios de X", listar todos los barrios del municipio como geografias

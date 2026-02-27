---
description: Consultar datos del Census Bureau para Puerto Rico
argument-hint: "<pregunta en lenguaje natural>"
---

Consulta datos del U.S. Census Bureau para Puerto Rico basado en la pregunta del usuario en $ARGUMENTS.

## Workflow

1. **Interpretar la pregunta**: Identifica que datos necesita el usuario (variables, geografia, periodo).

2. **Resolver geografia**: Si el usuario menciona un municipio o barrio, usa `censo_listar_municipios` o `censo_listar_barrios` para obtener el FIPS code correcto.

3. **Buscar variables**: Si la pregunta es sobre un tema especifico, usa `censo_buscar_variables` para encontrar las variables ACS correctas. Si es un tema comun (poblacion, ingreso, pobreza), usa directamente las variables conocidas.

4. **Ejecutar consulta**: Llama `censo_consultar` con el dataset apropiado (normalmente `acs/acs5`), anio mas reciente disponible, variables identificadas, y geografia resuelta.

5. **Evaluar calidad**: Para cada estimado devuelto, verifica el Margin of Error. Si el CV > 30%, advierte al usuario que el dato no es confiable. Usa `censo_evaluar_calidad` si necesitas un analisis detallado.

6. **Contextualizar**: Si el usuario pregunta por un solo municipio/barrio, usa `censo_contexto` para comparar con la mediana de PR y el dato nacional.

7. **Presentar resultados**: Formatea los datos en una tabla legible con:
   - Nombre de la geografia
   - Estimado
   - MOE (Margin of Error)
   - Clasificacion de confiabilidad (emoji: confiable, precaucion, no confiable)
   - Contexto vs PR/nacional si aplica

## Ejemplo

Si $ARGUMENTS = "poblacion de Vega Baja por barrio":
1. Resolver "Vega Baja" → county:145
2. Variables: B01003_001E (poblacion total), B01003_001M (MOE)
3. Query: dataset=acs/acs5, year=2022, for=county subdivision:*, in=state:72 county:145
4. Evaluar calidad de cada barrio
5. Presentar tabla ordenada por poblacion

## Notas

- Siempre usar el ACS 5-Year como default (mejor cobertura geografica)
- Siempre pedir el MOE junto con el estimado
- Si el usuario no especifica anio, usar el mas reciente disponible
- Si la variable no existe, sugerir alternativas con `censo_buscar_variables`

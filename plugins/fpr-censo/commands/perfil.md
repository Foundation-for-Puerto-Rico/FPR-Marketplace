---
description: Generar perfil tematico de un municipio o barrio
argument-hint: "<perfil> de <municipio/barrio>"
---

Genera un perfil tematico completo para una geografia de Puerto Rico usando $ARGUMENTS.

## Workflow

1. **Parsear argumentos**: Extrae el tipo de perfil y la geografia de $ARGUMENTS. Formatos esperados:
   - "demografico de Bayamon"
   - "economico de Vega Baja"
   - "vivienda de Almirante Sur, Vega Baja"
   - "completo de Carolina" (ejecuta los 6 perfiles)

2. **Perfiles disponibles**: demografico, economico, vivienda, educacion, salud_social, infraestructura. Si no se especifica, usar "demografico" como default.

   **Nota sobre "completo"**: `censo_perfil` solo acepta un perfil a la vez (o `None` para resumen ejecutivo). Si el usuario pide "completo", debes llamar `censo_perfil` una vez por cada uno de los 6 perfiles y combinar los resultados en un solo documento.

3. **Resolver geografia**: Usa `censo_listar_municipios` o `censo_listar_barrios` para obtener el FIPS correcto.

4. **Ejecutar perfil**: Llama `censo_perfil` con el tipo de perfil y la geografia resuelta.

5. **Evaluar calidad**: Revisa el MOE/CV de cada variable. Si hay estimados no confiables (CV > 30%), agrupelos al final con una nota de precaucion.

6. **Contextualizar**: Usa `censo_contexto` para los indicadores clave del perfil, comparando con PR y nacional.

7. **Presentar resultados**: Organiza los datos en secciones claras:

   ### Encabezado
   - Nombre de la geografia y tipo de perfil
   - Dataset y anio utilizado
   - Nota sobre nivel de confiabilidad general

   ### Datos principales
   - Tabla con cada indicador, estimado, MOE, y CV
   - Emojis de confiabilidad junto a cada dato

   ### Contexto
   - Como se compara con PR y nacional en indicadores clave

   ### Datos con precaucion
   - Lista de estimados con CV > 30% y recomendacion de agregar geografia

## Ejemplo

Si $ARGUMENTS = "economico de Caguas":
1. Perfil: economico, Geografia: Caguas → county:025
2. Llama censo_perfil(tipo="economico", municipio="025")
3. Devuelve ingreso mediano, % pobreza, tasa de empleo/desempleo, industrias principales
4. Contextualiza ingreso vs PR ($21,058) y nacional ($37,585)
5. Formatea resultado con tabla y contexto

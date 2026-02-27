# Perfiles Tematicos — Variables ACS

Variables curadas por perfil tematico. Estas son las variables exactas que `censo_perfil` consulta.
Para cada variable, siempre solicitar tambien el codigo MOE (columna `_M`).

## demografico

| Variable | MOE | Descripcion | Formato |
|----------|-----|-------------|---------|
| B01003_001E | B01003_001M | Poblacion total | conteo |
| B01002_001E | B01002_001M | Edad mediana | mediana |
| B01001_002E | B01001_002M | Poblacion masculina | conteo |
| B01001_026E | B01001_026M | Poblacion femenina | conteo |
| B09001_001E | B09001_001M | Menores de 18 anios | conteo |
| B03003_003E | B03003_003M | Hispanic o Latino | conteo |

## economico

| Variable | MOE | Descripcion | Formato |
|----------|-----|-------------|---------|
| B19013_001E | B19013_001M | Ingreso mediano del hogar | moneda |
| B19301_001E | B19301_001M | Ingreso per capita | moneda |
| B17001_002E | B17001_002M | Personas bajo nivel de pobreza | conteo |
| B23025_005E | B23025_005M | Desempleados | conteo |
| B23025_002E | B23025_002M | Fuerza laboral | conteo |
| B22003_002E | B22003_002M | Hogares con SNAP/cupones | conteo |

**Nota**: Tasa de desempleo = B23025_005E / B23025_002E. Tasa de pobreza requiere el universo B17001_001E (no incluido por default; usar `censo_consultar` para obtenerlo).

## vivienda

| Variable | MOE | Descripcion | Formato |
|----------|-----|-------------|---------|
| B25001_001E | B25001_001M | Unidades de vivienda total | conteo |
| B25002_002E | B25002_002M | Viviendas ocupadas | conteo |
| B25002_003E | B25002_003M | Viviendas vacantes | conteo |
| B25077_001E | B25077_001M | Valor mediano de vivienda | moneda |
| B25064_001E | B25064_001M | Renta mediana | moneda |
| B25081_002E | B25081_002M | Viviendas sin hipoteca | conteo |

## educacion

| Variable | MOE | Descripcion | Formato |
|----------|-----|-------------|---------|
| B15003_017E | B15003_017M | Diploma de escuela superior | conteo |
| B15003_022E | B15003_022M | Grado de bachillerato (BA) | conteo |
| B15003_023E | B15003_023M | Grado de maestria | conteo |
| B15003_025E | B15003_025M | Grado doctoral | conteo |
| B14001_002E | B14001_002M | Matricula escolar (3+ anios) | conteo |

**Nota**: Universo educativo = poblacion 25+ anios. Para porcentajes, usar `censo_consultar` con B15003_001E como denominador.

## salud_social

| Variable | MOE | Descripcion | Formato |
|----------|-----|-------------|---------|
| B27001_005E | B27001_005M | Sin seguro medico (menores 19) | conteo |
| B21001_002E | B21001_002M | Veteranos | conteo |
| B18101_004E | B18101_004M | Con discapacidad (menores 18) | conteo |

**Nota**: Este perfil tiene pocas variables curadas. Para datos mas detallados de salud, usar `censo_buscar_variables` con keywords como "insurance", "disability", "language".

## infraestructura

| Variable | MOE | Descripcion | Formato |
|----------|-----|-------------|---------|
| B28002_004E | B28002_004M | Hogares con internet de banda ancha | conteo |
| B08201_002E | B08201_002M | Hogares sin vehiculo | conteo |
| B08301_010E | B08301_010M | Transporte publico al trabajo | conteo |
| B08301_003E | B08301_003M | Viaja solo en carro al trabajo | conteo |

## Notas generales

- Para cada variable `_E` (estimado), siempre solicitar la variable `_M` (margin of error) correspondiente
- El sufijo numerico varia por variable (no todas usan `_001`). Usar los codigos exactos de esta tabla
- El ACS 5-Year (2018-2022) tiene la mejor cobertura para PR
- Para block groups, solo estan disponibles tablas basicas — muchos estimados tendran CV > 30%
- Variables no listadas aqui pueden consultarse con `censo_buscar_variables` y `censo_consultar`

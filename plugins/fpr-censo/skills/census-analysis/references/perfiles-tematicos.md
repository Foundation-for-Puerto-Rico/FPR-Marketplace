# Perfiles Tematicos — Variables ACS

Variables pre-seleccionadas por perfil tematico, usadas por `censo_perfil`.

## demografico

| Variable | Descripcion |
|----------|-------------|
| B01003_001E | Poblacion total |
| B01002_001E | Edad mediana |
| B01001_002E | Poblacion masculina |
| B01001_026E | Poblacion femenina |
| B02001_002E | Raza: Blanco solo |
| B02001_003E | Raza: Negro o afroamericano solo |
| B03003_003E | Origen hispano o latino |
| B01001_003E-B01001_006E | Poblacion 0-17 anios (menores) |
| B01001_020E-B01001_025E | Poblacion 65+ anios (envejecientes) |

## economico

| Variable | Descripcion |
|----------|-------------|
| B19013_001E | Ingreso mediano del hogar |
| B19301_001E | Ingreso per capita |
| B17001_002E | Personas bajo nivel de pobreza |
| B17001_001E | Personas para las que se determina pobreza (universo) |
| B23025_003E | Fuerza laboral civil |
| B23025_005E | Desempleados |
| B23025_002E | En la fuerza laboral |
| C24010_001E | Empleados por industria (total) |
| B19001_001E | Hogares por nivel de ingreso (total) |

## vivienda

| Variable | Descripcion |
|----------|-------------|
| B25001_001E | Unidades de vivienda total |
| B25002_002E | Unidades ocupadas |
| B25002_003E | Unidades vacantes |
| B25003_002E | Ocupadas por duenio |
| B25003_003E | Ocupadas por inquilino |
| B25077_001E | Valor mediano (unidades del duenio) |
| B25064_001E | Renta mediana bruta |
| B25034_001E | Anio de construccion (total) |
| B25024_001E | Unidades en estructura (total) |

## educacion

| Variable | Descripcion |
|----------|-------------|
| B15003_001E | Poblacion 25+ (universo educativo) |
| B15003_017E | Diploma de escuela superior |
| B15003_022E | Bachillerato (Bachelor's) |
| B15003_023E | Maestria |
| B15003_025E | Doctorado |
| B14001_002E | Matriculados en escuela (3+ anios) |

## salud_social

| Variable | Descripcion |
|----------|-------------|
| B27001_001E | Total para cobertura de seguro medico |
| B27001_004E | Con seguro medico (menores 6 anios) |
| B27001_007E | Sin seguro medico (menores 6 anios) |
| B18101_001E | Total para estatus de discapacidad |
| B18101_004E | Con discapacidad (menores 5 anios) |
| C16001_001E | Poblacion 5+ por idioma hablado en hogar |
| C16001_002E | Solo ingles |
| C16001_003E | Espanol |

## infraestructura

| Variable | Descripcion |
|----------|-------------|
| B28002_001E | Total hogares (internet) |
| B28002_002E | Con suscripcion a internet |
| B28002_013E | Sin internet |
| B08301_001E | Trabajadores 16+ (medio de transporte) |
| B08301_002E | Auto, camion o van (solo) |
| B08301_010E | Transporte publico |
| B08301_021E | Trabaja desde el hogar |
| B25044_001E | Vehiculos disponibles por hogar |

## Notas

- Todas las variables usan el sufijo `_001E` para estimado y `_001M` para MOE
- El ACS 5-Year (2018-2022) tiene la mejor cobertura para PR
- Para block groups, solo estan disponibles las tablas basicas (B01, B02, B03, B19, B25)
- Las variables de detalle (por edad, por industria) requieren tablas expandidas

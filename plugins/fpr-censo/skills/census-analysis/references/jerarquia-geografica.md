# Jerarquia Geografica de Puerto Rico

## Estructura en el Census API

```
Puerto Rico (state:72)
  └── Municipio (county:001-153, 78 municipios)
       └── Barrio (county subdivision)
            └── Census Tract (tract)
                 └── Block Group (block group)
                      └── Block (block, solo decenal)
```

## Traduccion de terminologia

| Census API (federal) | Termino local PR |
|---------------------|-----------------|
| state | estado/territorio |
| county | municipio |
| county subdivision | barrio |
| tract | tract censal |
| block group | grupo de bloques |
| block | bloque censal |

## Clausulas for/in del API

| Nivel | Clausula `for` | Clausula `in` |
|-------|---------------|---------------|
| Puerto Rico completo | state:72 | (ninguna) |
| Todos los municipios | county:* | state:72 |
| Un municipio | county:XXX | state:72 |
| Barrios de un municipio | county subdivision:* | state:72 county:XXX |
| Tracts de un municipio | tract:* | state:72 county:XXX |
| Block groups de un tract | block group:* | state:72 county:XXX tract:YYYYYY |

## Municipios de ejemplo

| Municipio | FIPS (county) | Poblacion (2020) |
|-----------|--------------|-----------------|
| San Juan | 127 | 342,259 |
| Bayamon | 021 | 185,187 |
| Carolina | 031 | 146,984 |
| Ponce | 113 | 126,327 |
| Caguas | 025 | 127,244 |
| Guaynabo | 061 | 83,728 |
| Mayaguez | 097 | 75,050 |
| Arecibo | 013 | 81,966 |
| Vega Baja | 145 | 51,901 |
| Humacao | 069 | 50,653 |

## Notas importantes

- PR tiene 78 municipios (FIPS impares 001-153)
- Cada municipio tiene entre 5 y 40+ barrios
- El barrio "Pueblo" es el centro urbano de cada municipio
- El ACS 1-Year solo cubre municipios con 65,000+ habitantes (~10 municipios)
- Para datos a nivel de barrio, usar siempre ACS 5-Year
- Los block groups tienen muestras muy pequenas; muchos estimados tendran CV > 30%

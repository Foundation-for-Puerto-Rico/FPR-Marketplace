# fpr-censo

Plugin de Claude Code para consultar datos del U.S. Census Bureau, optimizado para Puerto Rico.

## Instalacion

```
/plugin marketplace add Foundation-for-Puerto-Rico/FPR-Marketplace
/plugin install fpr-censo@fpr-tools
```

## Comandos

| Comando | Descripcion |
|---------|-------------|
| `/fpr-censo:setup` | Verificar configuracion y estado del servidor |
| `/fpr-censo:consultar` | Consulta flexible en lenguaje natural |
| `/fpr-censo:perfil` | Perfil tematico de un municipio o barrio |
| `/fpr-censo:comparar` | Comparar dos o mas geografias lado a lado |
| `/fpr-censo:serie` | Tendencia temporal de un indicador |

## Ejemplos de uso

### Consultar datos

```
/fpr-censo:consultar poblacion de Vega Baja por barrio
```

### Perfil completo

```
/fpr-censo:perfil economico de Caguas
```

### Comparar municipios

```
/fpr-censo:comparar Bayamon vs Carolina en vivienda
```

### Serie temporal

```
/fpr-censo:serie poblacion de Bayamon desde 2015
```

## Datos disponibles

El plugin conecta con el servidor MCP `fpr-censo` que provee acceso a:

- **ACS 5-Year**: Datos detallados hasta nivel de block group
- **ACS 1-Year**: Datos recientes para municipios 65k+ habitantes
- **Decennial Census**: Conteos oficiales
- **Population Estimates**: Estimados intercensales

### Perfiles tematicos

- **demografico**: Poblacion, edad, sexo, raza/etnicidad
- **economico**: Ingreso, pobreza, empleo, industria
- **vivienda**: Unidades, ocupacion/vacancia, valor, renta
- **educacion**: Nivel educativo, matricula escolar
- **salud_social**: Seguro medico, discapacidad, idioma
- **infraestructura**: Internet, vehiculos, transporte al trabajo

## Calidad estadistica

Todos los estimados del ACS incluyen Margin of Error (MOE) y evaluacion de confiabilidad:

| CV | Clasificacion |
|----|---------------|
| < 15% | Confiable |
| 15-30% | Usar con precaucion |
| > 30% | No confiable |

## Agentes especializados

- **data-researcher**: Investigacion de datos que requiere multiples consultas combinadas
- **quality-assessor**: Evaluacion rapida de calidad estadistica de estimados

## Servidor

El plugin conecta automaticamente al servidor MCP remoto via HTTPS. No necesitas instalar ni configurar nada adicional.

Para usar un servidor local, edita `.mcp.json` en el directorio del plugin y cambia la URL a `http://localhost:8001/mcp`.

## Licencia

MIT

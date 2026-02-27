---
description: Verificar configuracion del servidor Census y guiar al usuario
argument-hint: ""
---

Verifica que el servidor MCP de Census esta funcionando y correctamente configurado.

## Pasos

1. **Verificar conexion**: Llama `censo_estado` para verificar que el servidor esta accesible y el API key esta configurado.

2. **Si el servidor responde OK**:
   - Muestra la version del servidor, datasets disponibles, y estado del API key
   - Sugiere comandos de ejemplo: `/fpr-censo:perfil demografico de Bayamon`, `/fpr-censo:consultar ingreso mediano por municipio`

3. **Si el servidor no responde**:
   - Informa que el servidor MCP en `http://35.202.239.234:8001/mcp` no esta accesible
   - Sugiere verificar la conexion a internet o contactar al administrador

4. **Si el API key no esta configurado**:
   - Explica que se necesita un API key gratuito del Census Bureau
   - Guia al usuario a obtenerlo en https://api.census.gov/data/key_signup.html
   - Indica que el key debe configurarse como variable de entorno `CENSUS_API_KEY` en el servidor

## Notas

- Este comando es read-only, no modifica ninguna configuracion
- El API key del Census Bureau es gratuito y se obtiene al instante

# Despliegue continuo a Azure (E13)

El pipeline `.github/workflows/ci.yml` ejecuta seis etapas en orden. Cada una
depende de la anterior, así que una falla detiene todo lo que sigue.

| Orden | Job | Qué hace |
| --- | --- | --- |
| 1 | Build and syntax validation | Instala dependencias, compila el backend y construye el frontend |
| 2 | Unit tests and coverage | pytest y Vitest con cobertura |
| 3 | SonarCloud analysis and quality gate | Análisis estático; espera el resultado del quality gate |
| 4 | Postman API tests | Newman contra la API publicada |
| 5 | Deployment gate | Confirma que las validaciones pasaron; es el check obligatorio de `qa` y `main` |
| 6 | Deploy to Azure | Despliega backend y frontend y ejecuta un smoke test |

La etapa 6 solo corre con un `push` a `main`, es decir, cuando se integra un PR
de promoción `qa → main` que ya tiene aprobación y el pipeline en verde. En
`dev`, `qa` y en los PR se omite.

## Cómo despliega

- **Backend:** empaqueta `requirements.txt` y `backend/` y lo publica en el App
  Service `app-wlms-api-2026` con `azure/webapps-deploy`. Azure instala las
  dependencias (`SCM_DO_BUILD_DURING_DEPLOYMENT`) y arranca con
  `gunicorn --chdir backend ... main:app`.
- **Frontend:** construye `wlms-frontend` con `VITE_API_BASE_URL` apuntando a la
  API y lo sube a Static Web Apps.
- **Smoke test:** después del despliegue verifica que respondan `/`,
  `/openapi.json` y el frontend. Si alguno falla, el job queda en rojo.

## Autenticación

El backend se despliega con OIDC, sin perfil de publicación ni contraseñas. La
autenticación básica del App Service está deshabilitada.

- Identidad administrada `id-github-wlms-deploy` en `rg-wlms-qa-2026`.
- Credenciales federadas que solo aceptan tokens de GitHub Actions del entorno
  production de este repositorio. Hay dos porque GitHub empezó a enviar el
  subject con los identificadores numéricos del dueño y del repositorio:
  `repo:QuiqueDiaz33@141443537/warehouse-management-system@1443792730:environment:production`.
  El primer despliegue falló por eso con el error AADSTS700213 y se resolvió
  agregando la credencial con ese formato. La de formato anterior se mantiene
  por compatibilidad.
- Rol `Website Contributor` limitado al App Service, no a la suscripción.

El frontend usa el token de despliegue de Static Web Apps.

## Configuración del entorno `production` en GitHub

| Tipo | Nombre |
| --- | --- |
| Secreto | `AZURE_CLIENT_ID` (client ID de la identidad administrada) |
| Secreto | `AZURE_TENANT_ID` |
| Secreto | `AZURE_SUBSCRIPTION_ID` |
| Secreto | `AZURE_STATIC_WEB_APPS_API_TOKEN` |
| Variable | `AZURE_WEBAPP_NAME` |
| Variable | `API_BASE_URL` |
| Variable | `STATIC_WEB_APP_URL` |

La etapa 6 verifica que existan todos antes de desplegar y falla con un mensaje
claro si falta alguno.

## Preparación única en Azure

Se ejecuta una sola vez en Azure Cloud Shell (Bash):

```bash
az account set -s "Azure for Students"
RG=rg-wlms-qa-2026
ID=id-github-wlms-deploy
az provider register -n Microsoft.ManagedIdentity --wait
az identity create -g $RG -n $ID -o none
az identity federated-credential create -g $RG --identity-name $ID -n github-production \
  --issuer https://token.actions.githubusercontent.com \
  --subject repo:QuiqueDiaz33/warehouse-management-system:environment:production \
  --audiences api://AzureADTokenExchange -o none
az identity federated-credential create -g $RG --identity-name $ID -n github-production-ids \
  --issuer https://token.actions.githubusercontent.com \
  --subject "repo:QuiqueDiaz33@141443537/warehouse-management-system@1443792730:environment:production" \
  --audiences api://AzureADTokenExchange -o none
az role assignment create \
  --assignee-object-id $(az identity show -g $RG -n $ID --query principalId -o tsv) \
  --assignee-principal-type ServicePrincipal --role "Website Contributor" \
  --scope $(az webapp show -g $RG -n app-wlms-api-2026 --query id -o tsv) -o none
echo "AZURE_CLIENT_ID=$(az identity show -g $RG -n $ID --query clientId -o tsv)"
echo "AZURE_TENANT_ID=$(az account show --query tenantId -o tsv)"
echo "AZURE_SUBSCRIPTION_ID=$(az account show --query id -o tsv)"
```

Los tres valores que imprime se guardan como secretos del entorno `production`.

## Primer despliegue

El 6 de noviembre de 2026, con el merge del PR #22 a main (commit c760deb), la
etapa se ejecutó completa: inicio de sesión OIDC, backend, frontend y smoke
test. Después del despliegue, el contrato publicado en /openapi.json muestra
SOLineCreate con so_id, item_id, quantity y unit_price, y POST
/sales-orders/lines sin token responde 401 en lugar del 500 anterior.

## Migraciones de base de datos

El pipeline despliega código, no cambia el esquema de la base. Los scripts de
`SQL/migrations/` se ejecutan aparte, una vez, antes o junto con la promoción
que los necesita. Pendiente actualmente:
`2026-11-06_sales_order_lines_unit_price_check.sql`.

## Limitación conocida

Por el plan gratuito F1 existe un solo App Service y una sola base de datos.
Los entornos `qa` y `production` de GitHub controlan las promociones y las
aprobaciones, pero apuntan a la misma infraestructura. Por eso el despliegue
corre únicamente desde `main` y las pruebas de Newman se ejecutan contra el
mismo ambiente publicado. Separarlos requiere un segundo App Service y una
segunda base para QA.

## Reversión

Para volver a una versión anterior se revierte el commit en `main` con un PR
(`Revert`) o se vuelve a ejecutar el pipeline de un commit anterior desde
Actions; la etapa 6 publica nuevamente ese código.

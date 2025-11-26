# Guía de Configuración - AWS Bedrock + fal.ai (v3.0)

Esta guía te ayudará a configurar el Concept Art Agent v3.0 usando:
- **AWS Bedrock** (solo para Claude - generación de prompts)
- **fal.ai** (para FLUX - generación de imágenes)

## ¿Por qué esta configuración?

- **AWS Bedrock (Claude)**: Para generar prompts creativos de alta calidad
- **fal.ai (FLUX)**: Mejor calidad de imágenes que AWS Titan
- **Sin filtros restrictivos**: No más errores de validación de contenido de AWS
- **Más económico**: Costos competitivos para generación de imágenes

## Paso 1: Obtener Credenciales de AWS

### 1.1 Acceder a AWS Console

1. Ve a [AWS Console](https://console.aws.amazon.com)
2. Inicia sesión con tu cuenta

### 1.2 Crear Access Keys

1. Ve a **IAM** (Identity and Access Management)
2. Navega a **Users** → Selecciona tu usuario
3. Ve a la pestaña **Security credentials**
4. En la sección **Access keys**, haz clic en **Create access key**
5. Selecciona **Use case**: "Third-party service" o "CLI"
6. Guarda tanto el **Access Key ID** como el **Secret Access Key**

**IMPORTANTE**: El Secret Access Key solo se muestra una vez. Guárdalo de forma segura.

### 1.3 Permisos Necesarios

Tu usuario de AWS debe tener permisos para:
- `bedrock:InvokeModel`
- `bedrock:InvokeModelWithResponseStream`

Puedes usar la política administrada: `AmazonBedrockFullAccess`

## Paso 2: Verificar Acceso a Claude en Bedrock

### 2.1 Acceder a Amazon Bedrock

1. En AWS Console, busca **Amazon Bedrock**
2. Ve a **Model access** en el menú lateral
3. Verifica que tengas acceso a:
   - ✅ **Claude 3.5 Sonnet** (us.anthropic.claude-3-5-sonnet-20241022-v2:0)

**NOTA v3.0**: Ya NO necesitas acceso a Stability AI ni Titan, porque usaremos fal.ai para las imágenes

### 2.2 Verificar Región

Bedrock no está disponible en todas las regiones. Regiones recomendadas:
- **us-east-1** (N. Virginia) - Recomendada
- **us-west-2** (Oregon)
- **eu-west-1** (Irlanda)

## Paso 3: Configurar fal.ai

### 3.1 Crear cuenta en fal.ai

1. Ve a https://fal.ai
2. Regístrate con tu email o GitHub
3. Tienen plan gratuito para probar

### 3.2 Obtener API Key

1. Ve a https://fal.ai/dashboard/keys
2. Haz clic en **Create new key**
3. Copia tu API key (guárdala de forma segura)

## Paso 4: Configurar el archivo .env

Abre tu archivo `.env` y configura las credenciales:

```env
# ========================================
# CONCEPT ART AGENT v3.0 - CONFIGURACIÓN
# ========================================

# AWS (para Claude - generación de prompts creativos)
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# fal.ai (para FLUX - generación de imágenes)
FAL_KEY=tu_fal_api_key_aqui
```

### Modelos Disponibles

**Claude (AWS Bedrock) - Para prompts:**
- Se usa automáticamente: `us.anthropic.claude-3-5-sonnet-20241022-v2:0`

**FLUX (fal.ai) - Para imágenes:**
- `fal-ai/flux/dev` - Balance calidad/velocidad (Recomendado)
- `fal-ai/flux-pro` - Máxima calidad
- `fal-ai/flux/schnell` - Ultra rápido y económico

## Paso 5: Probar la Configuración

### 5.1 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5.2 Ejecutar la aplicación Streamlit

```bash
streamlit run app.py
```

### 5.3 Probar la generación

1. La app se abrirá en tu navegador (http://localhost:8501)
2. Ingresa tus credenciales en el sidebar:
   - AWS Access Key ID
   - AWS Secret Access Key
   - fal.ai API Key
3. Describe tu videojuego
4. Selecciona el modelo FLUX (recomendado: flux/dev)
5. Haz clic en "Generar Arte Conceptual"

## Uso con AWS Bedrock

### Desde Python

```python
from concept_art_agent.bedrock_generator import (
    BedrockPromptGenerator,
    BedrockImageGenerator
)
from concept_art_agent.organizer import ResultOrganizer

# Inicializar generadores
prompt_gen = BedrockPromptGenerator(
    region_name="us-east-1",
    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0"
)

image_gen = BedrockImageGenerator(
    region_name="us-east-1",
    model_id="stability.stable-diffusion-xl-v1"
)

# Generar prompts
game_description = "Shooter espacial futurista con naves y aliens"
prompts = prompt_gen.generate_prompts(game_description)

# Generar imágenes
organizer = ResultOrganizer()
project_dir = organizer.create_project_structure("my_game")

for category, category_prompts in prompts.items():
    category_dir = organizer.get_category_dir(project_dir, category)
    images = image_gen.generate_batch(
        prompts=category_prompts[:2],
        output_dir=category_dir,
        prefix=category
    )
```

### Desde Línea de Comandos

```bash
# Básico con Bedrock
python main.py --prompt "Tu juego aquí" --provider bedrock

# Especificar modelos
python main.py \
  --prompt "Horror survival en hospital" \
  --provider bedrock \
  --images-per-category 3
```

### Ejecutar Ejemplos

```bash
# Ejemplo completo con Bedrock
python example_bedrock.py

# Ver ejemplos específicos editando el archivo
```

## Costos Estimados (v3.0)

### Claude (AWS Bedrock) - Generación de Prompts

**Claude 3.5 Sonnet:**
- Input: ~$3.00 / 1M tokens
- Output: ~$15.00 / 1M tokens
- **Por proyecto: ~$0.003** (uso muy bajo)

### FLUX (fal.ai) - Generación de Imágenes

**FLUX Dev:**
- ~$0.03 por imagen
- Proyecto (14 imágenes): ~$0.42

**FLUX Pro:**
- ~$0.05 por imagen
- Proyecto (14 imágenes): ~$0.70

**FLUX Schnell:**
- ~$0.02 por imagen
- Proyecto (14 imágenes): ~$0.28

**Total por proyecto (FLUX Dev)**: ~$0.42 + $0.003 ≈ **$0.42 USD**

## Comparación de versiones

| Característica | v2.0 (AWS Titan) | v3.0 (fal.ai FLUX) |
|---|---|---|
| Precio por imagen | $0.04 | $0.02 - $0.05 |
| Calidad | Media | Alta/Excelente |
| Filtros contenido | Muy restrictivos ❌ | Sin filtros ✅ |
| Velocidad | Media | Rápida/Ultra rápida |
| Proyecto (14 imgs) | ~$0.56 | $0.28 - $0.70 |
| Errores validación | Frecuentes | Ninguno |
| **Total proyecto** | **$0.57** | **$0.42** (Dev) |

## Solución de Problemas

### Errores de AWS Bedrock (Claude)

**Error: "Could not connect to the endpoint"**
- Verifica que tu región soporte Bedrock
- Usa `us-east-1` (recomendado)
- Verifica que Bedrock esté habilitado en tu cuenta

**Error: "AccessDeniedException"**
- Ve a IAM y añade la política `AmazonBedrockFullAccess`
- Verifica que tu usuario tenga permisos `bedrock:InvokeModel`

**Error: "ValidationException: Model not found"**
- Ve a AWS Bedrock → Model access
- Habilita Claude 3.5 Sonnet
- Espera unos minutos para la activación

**Credenciales AWS no funcionan**
- Verifica que las credenciales estén correctamente copiadas
- No debe haber espacios extra
- El Access Key ID debe empezar con `AKIA`

### Errores de fal.ai (FLUX)

**Error de autenticación**
- Verifica que tu API key de fal.ai sea correcta
- Cópiala sin espacios extra del dashboard

**Error: "Insufficient credits"**
- Revisa tu saldo en https://fal.ai/dashboard
- Recarga créditos si es necesario
- El plan gratuito tiene límites

**Imágenes no se generan**
- Prueba con FLUX Schnell primero (más rápido y barato)
- Verifica que tu prompt no esté vacío
- Revisa los logs de error en la app

**Timeout o muy lento**
- FLUX Schnell es el más rápido (4 steps)
- FLUX Dev es balance (28 steps)
- FLUX Pro es el más lento pero mejor calidad

## Seguridad

### Mejores Prácticas

1. **No compartas tu `.env`**: Este archivo contiene credenciales privadas
2. **Usa .gitignore**: Asegúrate que `.env` esté en `.gitignore`
3. **Rota credenciales**: Cambia tus Access Keys periódicamente
4. **Permisos mínimos**: Da solo los permisos necesarios a tu usuario
5. **Monitorea uso**: Revisa AWS CloudWatch para detectar uso anormal

### Revocar Access Keys

Si crees que tus credenciales están comprometidas:

1. Ve a IAM → Users → Tu usuario
2. Security credentials
3. Encuentra el Access Key comprometido
4. Haz clic en "Actions" → "Deactivate" o "Delete"
5. Crea nuevas credenciales

## Recursos Adicionales

### AWS Bedrock
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Claude Models in Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-claude.html)
- [AWS Pricing Calculator](https://calculator.aws/#/)

### fal.ai
- [fal.ai Documentation](https://fal.ai/docs)
- [FLUX Models](https://fal.ai/models/flux)
- [fal.ai Dashboard](https://fal.ai/dashboard)
- [fal.ai Pricing](https://fal.ai/pricing)

## Soporte

Si tienes problemas:

1. **AWS**: Verifica la [documentación de AWS Bedrock](https://docs.aws.amazon.com/bedrock/)
2. **fal.ai**: Consulta [fal.ai docs](https://fal.ai/docs)
3. **App**: Revisa los logs de error en la interfaz de Streamlit
4. Ejecuta `streamlit run app.py` y verifica la consola

---

## Changelog v3.0

✨ **Cambios principales**:
- Migrado de AWS Titan a fal.ai FLUX para generación de imágenes
- AWS Bedrock solo para Claude (prompts creativos)
- Mejor calidad de imágenes con FLUX
- Sin filtros restrictivos de contenido
- 3 modelos FLUX disponibles (Dev, Pro, Schnell)
- Costos más competitivos

¡Listo! Ahora puedes generar arte conceptual de alta calidad con Claude + FLUX.

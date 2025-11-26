# 🎨 Concept Art Generator v3.0

Generador de arte conceptual para videojuegos usando **Claude (prompts) + FLUX (imágenes)** con interfaz web moderna.

**Versión 3.0**: Migrado de AWS Titan a fal.ai FLUX para mejor calidad y sin filtros restrictivos.

## 🚀 Inicio Rápido

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar credenciales (opcional, también puedes hacerlo en la UI)
cp .env.example .env
# Edita .env con:
#   - Credenciales AWS (para Claude)
#   - API Key de fal.ai (para FLUX)

# 3. Ejecutar la aplicación
streamlit run app.py
```

La app se abrirá automáticamente en `http://localhost:8501`

## ✨ Características

- **Interfaz Web Moderna**: Streamlit UI intuitiva y responsiva
- **Mejor Calidad**: FLUX genera imágenes superiores a AWS Titan
- **Sin Filtros Restrictivos**: No más errores de validación de contenido
- **Doble IA**:
  - **Claude 3.5 Sonnet** (AWS Bedrock) para prompts creativos
  - **FLUX** (via fal.ai) para generar imágenes de alta calidad
- **Personalizable**: Selecciona categorías y cantidad de imágenes
- **Visualización en Tiempo Real**: Ve las imágenes mientras se generan
- **Organización Automática**: Guarda imágenes por categoría con metadata
- **3 Modelos FLUX**: Dev (balanceado), Pro (máxima calidad), Schnell (ultra rápido)

## 📋 Requisitos

- Python 3.8+
- **Cuenta de AWS** con acceso a Bedrock:
  - Claude 3.5 Sonnet (inference profile: `us.anthropic.claude-3-5-sonnet-20241022-v2:0`)
  - Solo para generación de prompts creativos
- **Cuenta de fal.ai**:
  - Regístrate en https://fal.ai
  - Obtén tu API key en https://fal.ai/dashboard/keys
  - Tienen plan gratuito para probar

## 📁 Estructura del Proyecto

```
concept-art-agent/
├── app.py                    # ⭐ Aplicación principal Streamlit
├── requirements.txt          # Dependencias (4 paquetes)
├── .env.example             # Template de configuración
├── .env                     # Tu configuración (crear)
├── README.md                # Este archivo
├── README_STREAMLIT.md      # Documentación detallada
├── AWS_BEDROCK_SETUP.md     # Guía de configuración AWS
└── outputs/                 # Imágenes generadas
    └── proyecto_nombre/
        ├── main_character/
        ├── enemies/
        ├── environments/
        └── ...
```

## 🎯 Categorías de Arte

- **Main Character**: Personaje principal
- **Enemies**: Enemigos y antagonistas
- **Environments**: Ambientes y escenarios
- **Weapons**: Armas y equipamiento
- **Collectibles**: Objetos coleccionables
- **NPCs**: Personajes no jugables
- **UI Elements**: Elementos de interfaz

## 💡 Ejemplo de Uso

1. Describe tu videojuego:
   ```
   Juego de acción RPG en tercera persona estilo Dark Souls.
   Ambientado en un mundo de fantasía oscura medieval.
   Castillos góticos, bosques tenebrosos, criaturas monstruosas.
   Estética realista con atmósfera sombría.
   ```

2. Selecciona categorías (ej: Personaje, Enemigos, Ambientes)

3. Ajusta cantidad de imágenes por categoría (1-3)

4. Haz clic en "Generar Arte Conceptual"

5. Las imágenes se generarán y guardarán automáticamente

## 📊 Costos Estimados

- **Claude 3.5 Sonnet** (AWS): ~$0.003 por generación de prompts
- **FLUX Dev** (fal.ai): ~$0.03 por imagen
- **FLUX Pro** (fal.ai): ~$0.05 por imagen
- **FLUX Schnell** (fal.ai): ~$0.02 por imagen

**Ejemplo**: 2 imágenes × 3 categorías = 6 imágenes con FLUX Dev ≈ **$0.18 USD**

*Más económico y mejor calidad que AWS Titan*

## 🌐 Deploy en Streamlit Cloud

1. Sube el proyecto a GitHub (asegúrate de que `.env` está en `.gitignore`)
2. Conecta en [share.streamlit.io](https://share.streamlit.io)
3. **IMPORTANTE**: NO agregues tus credenciales en secrets
4. Los usuarios deberán ingresar sus propias API keys en la interfaz
5. Cada usuario usa sus propias credenciales (AWS + fal.ai)
6. ¡Deploy listo! Cada persona paga por su propio uso

## 🔧 Configuración AWS Bedrock

Ver [AWS_BEDROCK_SETUP.md](AWS_BEDROCK_SETUP.md) para instrucciones detalladas sobre:
- Crear cuenta AWS
- Habilitar Bedrock
- Activar modelos
- Configurar credenciales

## 📖 Documentación

- **[README_STREAMLIT.md](README_STREAMLIT.md)**: Guía completa de uso
- **[AWS_BEDROCK_SETUP.md](AWS_BEDROCK_SETUP.md)**: Setup de AWS Bedrock

## 🛠️ Troubleshooting

### Error: "AccessDeniedException" (AWS)
- Verifica credenciales AWS en el sidebar
- Confirma acceso a Bedrock habilitado en tu cuenta
- Usa región us-east-1 (recomendada)

### Error: "Model not found" (AWS)
- Ve a AWS Console → Bedrock → Model access
- Habilita Claude 3.5 Sonnet
- Espera unos minutos

### Error de fal.ai
- Verifica que tu API key de fal.ai sea correcta
- Revisa que tengas créditos en tu cuenta de fal.ai
- Prueba con FLUX Schnell (más rápido y económico)

### Las imágenes no se ven bien
- Describe tu juego con más detalle
- Prueba FLUX Pro para máxima calidad
- Ajusta el número de imágenes

## 📄 Licencia

Apache 2.0 License - Úsalo libremente

---

**v3.0 - Desarrollado con ❤️ usando Streamlit, Claude 3.5 Sonnet y FLUX**

### Changelog v3.0
- ✨ Migrado de AWS Titan a fal.ai FLUX
- 🚀 Mejor calidad de imágenes
- ⚡ Sin filtros restrictivos de contenido
- 💰 Costos más competitivos
- 🎨 3 modelos FLUX disponibles (Dev, Pro, Schnell)

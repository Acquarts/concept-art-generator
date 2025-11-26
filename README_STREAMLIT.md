# 🎨 Concept Art Generator v3.0 - Streamlit App

Genera arte conceptual para videojuegos usando **Claude (prompts) + FLUX (imágenes via fal.ai)** en una interfaz web simple y elegante.

## ✨ Características

- **Interfaz web moderna**: Streamlit para fácil interacción
- **Doble IA**:
  - **Claude 3.5 Sonnet** (AWS Bedrock) para prompts creativos
  - **FLUX** (fal.ai) para imágenes de alta calidad
- **Sin filtros restrictivos**: No más errores de validación de contenido
- **3 modelos FLUX**: Dev, Pro, Schnell
- **Personalizable**: Selecciona categorías y número de imágenes
- **Visualización en tiempo real**: Ve las imágenes generándose

## 🚀 Instalación Rápida

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar credenciales

Necesitas **2 servicios**:

**A) AWS Bedrock (para Claude - prompts)**
- AWS Access Key ID
- AWS Secret Access Key
- Acceso habilitado a Bedrock en us-east-1
- Modelo habilitado: Claude 3.5 Sonnet (`us.anthropic.claude-3-5-sonnet-20241022-v2:0`)

**B) fal.ai (para FLUX - imágenes)**
- Regístrate en https://fal.ai
- Obtén tu API key en https://fal.ai/dashboard/keys
- Plan gratuito disponible para probar

Puedes configurar las credenciales en:
- Un archivo `.env`:
  ```
  AWS_ACCESS_KEY_ID=tu_access_key
  AWS_SECRET_ACCESS_KEY=tu_secret_key
  FAL_KEY=tu_fal_api_key
  ```
- O directamente en la interfaz de Streamlit (sidebar) ← Recomendado para deploy

### 3. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📖 Cómo Usar

1. **Configura tus credenciales** en el sidebar (si no usas `.env`)

2. **Describe tu videojuego** en el área de texto principal
   - Incluye: género, estilo visual, ambientación, temática, referencias

3. **Personaliza la generación**:
   - Número de imágenes por categoría (1-3)
   - Selecciona qué categorías generar

4. **Haz clic en "Generar Arte Conceptual"**

5. **Espera mientras se generan**:
   - Primero se crean los prompts con Claude (AWS Bedrock)
   - Luego se generan las imágenes con FLUX (fal.ai)
   - Verás las imágenes aparecer en tiempo real

6. **Resultados guardados en** `outputs/nombre_proyecto/`

## 📁 Estructura de Salida

```
outputs/
└── nombre_proyecto/
    ├── main_character/
    │   ├── main_character_1.png
    │   └── main_character_2.png
    ├── enemies/
    ├── environments/
    ├── weapons/
    ├── collectibles/
    ├── npcs/
    ├── ui_elements/
    └── metadata.json
```

## 🎯 Categorías Disponibles

- **Main Character**: Personaje principal/protagonista
- **Enemies**: Enemigos y antagonistas
- **Environments**: Ambientes y escenarios
- **Weapons**: Armas y equipamiento
- **Collectibles**: Objetos coleccionables
- **NPCs**: Personajes no jugables
- **UI Elements**: Elementos de interfaz de usuario

## 💡 Ejemplo de Descripción

```
Juego de acción RPG en tercera persona estilo Dark Souls.
Ambientado en un mundo de fantasía oscura medieval.
Castillos góticos, bosques tenebrosos, criaturas monstruosas.
Estética realista con atmósfera sombría.
Inspirado en Elden Ring y Bloodborne.
```

## 🔧 Troubleshooting

### Error: "AccessDeniedException"
- Verifica que tus credenciales AWS sean correctas
- Asegúrate de tener acceso a Bedrock en tu región
- Comprueba que los modelos estén habilitados en la consola de AWS Bedrock

### Error: "Model not found" (AWS)
- Ve a la consola de AWS Bedrock → Model access
- Habilita Claude 3.5 Sonnet
- Espera unos minutos para que se active

### Error de fal.ai
- Verifica que tu API key sea correcta
- Revisa que tengas créditos en fal.ai
- Prueba con FLUX Schnell (más rápido y barato)

### Las imágenes no se generan bien
- Prueba FLUX Pro para máxima calidad
- Ajusta el número de imágenes por categoría
- Prueba con descripciones más específicas

## 🌐 Deploy en Streamlit Cloud

1. Sube tu código a GitHub (`.env` está en `.gitignore`)
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio
4. **IMPORTANTE**: NO agregues secrets en Streamlit Cloud
5. Los usuarios ingresarán sus propias API keys en la interfaz
6. Cada usuario paga por su propio uso
7. Deploy automático completado

## 📊 Costos Estimados

**Por generación de prompts:**
- Claude 3.5 Sonnet (AWS): ~$0.003

**Por imagen generada:**
- FLUX Dev (fal.ai): ~$0.03
- FLUX Pro (fal.ai): ~$0.05
- FLUX Schnell (fal.ai): ~$0.02

**Ejemplo**: 2 imágenes × 3 categorías con FLUX Dev = 6 imágenes ≈ **$0.18 USD**

*Más económico y mejor calidad que AWS Titan*

## 🆚 Ventajas de la v3.0

| Aspecto | v2.0 (AWS Titan) | v3.0 (fal.ai FLUX) |
|---------|------------------|---------------------|
| Calidad imágenes | Media | Alta/Excelente |
| Filtros contenido | Muy restrictivos ❌ | Sin filtros ✅ |
| Velocidad | Media | Rápida (Schnell: ultra rápido) |
| Costo por imagen | ~$0.04 | $0.02-$0.05 |
| Modelos disponibles | 3 (Titan/Nova) | 3 FLUX (Dev/Pro/Schnell) |
| Errores validación | Frecuentes | Ninguno |

## 📝 Licencia

Este proyecto es de código abierto. Úsalo libremente para tus proyectos.

---

**v3.0 - Claude 3.5 Sonnet + FLUX**

### Changelog v3.0
- ✨ Migrado de AWS Titan a fal.ai FLUX
- 🚀 Mejor calidad de imágenes (FLUX supera a Titan)
- ⚡ Sin filtros restrictivos de contenido de AWS
- 💰 Costos más competitivos
- 🎨 3 modelos FLUX: Dev, Pro, Schnell
- ⚙️ Configuración dual: AWS (prompts) + fal.ai (imágenes)

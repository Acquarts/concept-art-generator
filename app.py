"""
Concept Art Generator - Streamlit App
Genera arte conceptual para videojuegos usando Claude (prompts) + FLUX (imágenes via fal.ai)
Versión 3.0 - Migrado de AWS Titan a fal.ai FLUX
"""

import os
import json
import base64
from datetime import datetime
from pathlib import Path
import streamlit as st
import boto3
from botocore.exceptions import ClientError
import fal_client
import requests

# ==================== CONFIGURACIÓN ====================

st.set_page_config(
    page_title="Concept Art Generator",
    page_icon="🎨",
    layout="wide"
)

# ==================== FUNCIONES CORE ====================

def get_bedrock_client(region, aws_key, aws_secret):
    """Crea cliente de AWS Bedrock (solo para Claude - generación de prompts)"""
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=region,
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret
    )

def generate_prompts(game_description, bedrock_client, model_id):
    """Genera prompts creativos con Claude via AWS Bedrock"""
    system_prompt = """Eres un experto en arte conceptual para videojuegos.
    Genera prompts detallados optimizados para el modelo FLUX de generación de imágenes."""

    user_prompt = f"""Descripción del videojuego: {game_description}

Genera 2 prompts específicos para cada categoría (en inglés, optimizados para FLUX):

MAIN_CHARACTER:
- [prompt 1]
- [prompt 2]

ENEMIES:
- [prompt 1]
- [prompt 2]

ENVIRONMENTS:
- [prompt 1]
- [prompt 2]

WEAPONS:
- [prompt 1]
- [prompt 2]

COLLECTIBLES:
- [prompt 1]
- [prompt 2]

NPCS:
- [prompt 1]
- [prompt 2]

UI_ELEMENTS:
- [prompt 1]
- [prompt 2]

Cada prompt debe ser descriptivo, incluir estilo artístico y detalles técnicos."""

    try:
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 3000,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}]
        }

        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )

        response_body = json.loads(response["body"].read())
        claude_response = response_body["content"][0]["text"]

        prompts = parse_prompts(claude_response)

        # Verificar que haya prompts
        total_prompts = sum(len(p) for p in prompts.values())
        if total_prompts == 0:
            st.warning("Claude no generó prompts válidos. Usando prompts de respaldo...")
            return get_fallback_prompts(game_description)

        return prompts

    except Exception as e:
        st.warning(f"Error con Claude: {str(e)}. Usando prompts de respaldo...")
        return get_fallback_prompts(game_description)

def get_fallback_prompts(game_description):
    """Prompts de respaldo si Claude falla o no está disponible"""
    base = f"concept art, {game_description}, professional game art, detailed, high quality"

    return {
        "main_character": [
            f"Main character hero design, {base}, full body, dynamic pose",
            f"Protagonist character concept, {base}, front and side view"
        ],
        "enemies": [
            f"Enemy creature design, {base}, menacing, threatening",
            f"Antagonist monster concept, {base}, detailed anatomy"
        ],
        "environments": [
            f"Game environment landscape, {base}, atmospheric, detailed background",
            f"Game world scenery, {base}, cinematic composition"
        ],
        "weapons": [
            f"Weapon design concept, {base}, detailed illustration",
            f"Game weapon asset, {base}, multiple angles"
        ],
        "collectibles": [
            f"Collectible items, {base}, game pickups, power-ups",
            f"Game items concept, {base}, glowing effects"
        ],
        "npcs": [
            f"NPC character design, {base}, friendly character",
            f"Supporting character concept, {base}, full body"
        ],
        "ui_elements": [
            f"Game UI design, {base}, HUD elements, interface mockup",
            f"Menu interface, {base}, buttons and icons"
        ]
    }

def parse_prompts(response_text):
    """Parsea la respuesta de Claude y extrae los prompts por categoría"""
    category_map = {
        "MAIN_CHARACTER": "main_character",
        "ENEMIES": "enemies",
        "ENVIRONMENTS": "environments",
        "WEAPONS": "weapons",
        "COLLECTIBLES": "collectibles",
        "NPCS": "npcs",
        "UI_ELEMENTS": "ui_elements"
    }

    prompts = {cat: [] for cat in category_map.values()}
    current_category = None

    for line in response_text.split('\n'):
        line = line.strip()
        for key, value in category_map.items():
            if line.upper().startswith(key):
                current_category = value
                break

        if current_category and (line.startswith('-') or line.startswith('*')):
            prompt = line.lstrip('-*').strip()
            if prompt and not prompt.startswith('['):  # Ignorar placeholders
                prompts[current_category].append(prompt)

    return prompts

def generate_image_fal(prompt, model_id, fal_api_key):
    """
    Genera una imagen usando fal.ai con modelos FLUX

    Args:
        prompt: Texto descriptivo para generar la imagen
        model_id: ID del modelo FLUX a usar (flux/dev, flux-pro, flux/schnell)
        fal_api_key: API key de fal.ai

    Returns:
        bytes: Datos de la imagen en formato PNG
    """

    # Configurar API key
    os.environ["FAL_KEY"] = fal_api_key

    # Configuración según modelo FLUX
    model_configs = {
        "fal-ai/flux-pro": {
            "model": "fal-ai/flux-pro",
            "params": {
                "prompt": prompt,
                "image_size": "landscape_16_9",
                "num_inference_steps": 28,
                "guidance_scale": 3.5,
                "num_images": 1
            }
        },
        "fal-ai/flux/dev": {
            "model": "fal-ai/flux/dev",
            "params": {
                "prompt": prompt,
                "image_size": "landscape_16_9",
                "num_inference_steps": 28,
                "guidance_scale": 3.5,
                "num_images": 1
            }
        },
        "fal-ai/flux/schnell": {
            "model": "fal-ai/flux/schnell",
            "params": {
                "prompt": prompt,
                "image_size": "landscape_16_9",
                "num_inference_steps": 4,
                "num_images": 1
            }
        }
    }

    config = model_configs.get(model_id, model_configs["fal-ai/flux/dev"])

    try:
        # Llamar a fal.ai
        result = fal_client.subscribe(
            config["model"],
            arguments=config["params"]
        )

        # Descargar imagen
        if result and "images" in result and len(result["images"]) > 0:
            image_url = result["images"][0]["url"]
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                return response.content

        return None

    except Exception as e:
        raise Exception(f"Error con fal.ai: {str(e)}")

def save_image(image_data, category, index, project_dir):
    """Guarda imagen en el sistema de archivos"""
    category_dir = Path(project_dir) / category
    category_dir.mkdir(parents=True, exist_ok=True)

    filepath = category_dir / f"{category}_{index}.png"
    with open(filepath, "wb") as f:
        f.write(image_data)

    return str(filepath)

# ==================== INTERFAZ STREAMLIT ====================

# Nombres de categorías
CATEGORY_NAMES = {
    "main_character": "Personaje Principal", "enemies": "Enemigos",
    "environments": "Ambientes", "weapons": "Armas",
    "collectibles": "Coleccionables", "npcs": "NPCs",
    "ui_elements": "UI Elements"
}

st.title("🎨 Concept Art Generator")
st.markdown("Genera arte conceptual para videojuegos usando **Claude + FLUX** (fal.ai)")

# Sidebar - Configuración
with st.sidebar:
    st.header("⚙️ Configuración")

    st.subheader("🧠 Claude (Prompts)")
    aws_key = st.text_input("AWS Access Key ID", type="password",
                             value=os.getenv("AWS_ACCESS_KEY_ID", ""))
    aws_secret = st.text_input("AWS Secret Access Key", type="password",
                               value=os.getenv("AWS_SECRET_ACCESS_KEY", ""))
    aws_region = st.selectbox("AWS Region",
                              ["us-east-1", "us-west-2", "eu-west-1"],
                              index=0)

    st.divider()

    st.subheader("🎨 fal.ai (Imágenes)")
    fal_api_key = st.text_input("fal.ai API Key", type="password",
                                 value=os.getenv("FAL_KEY", ""),
                                 help="Obtén tu API key en https://fal.ai/dashboard/keys")

    image_model = st.selectbox(
        "Modelo FLUX",
        [
            "fal-ai/flux/dev",
            "fal-ai/flux-pro",
            "fal-ai/flux/schnell"
        ],
        index=0,
        help="FLUX Dev: Balance calidad/velocidad | Pro: Máxima calidad | Schnell: Ultra rápido"
    )

    images_per_category = st.slider("Imágenes por categoría", 1, 3, 2)

    st.divider()

    categories_to_generate = st.multiselect(
        "Categorías a generar",
        ["main_character", "enemies", "environments", "weapons",
         "collectibles", "npcs", "ui_elements"],
        default=["main_character", "enemies", "environments"]
    )

# Main area
st.header("📝 Descripción del Videojuego")

game_description = st.text_area(
    "Describe tu videojuego en detalle (género, estilo, ambientación, etc.)",
    height=150,
    placeholder="Ejemplo: Juego de acción RPG en tercera persona estilo Dark Souls..."
)

project_name = st.text_input("Nombre del proyecto (opcional)",
                              placeholder="mi_proyecto")

# Botón principal
if st.button("🚀 Generar Arte Conceptual", type="primary"):

    # Validaciones
    if not game_description:
        st.error("Por favor, ingresa una descripción del videojuego")
        st.stop()

    if not aws_key or not aws_secret:
        st.error("Por favor, configura tus credenciales de AWS para Claude en el sidebar")
        st.stop()

    if not fal_api_key:
        st.error("Por favor, configura tu API Key de fal.ai en el sidebar")
        st.stop()

    if not categories_to_generate:
        st.error("Selecciona al menos una categoría para generar")
        st.stop()

    # Iniciar generación
    try:
        # Crear directorio del proyecto
        if not project_name:
            project_name = "project_" + datetime.now().strftime("%Y%m%d_%H%M%S")

        project_dir = Path("outputs") / project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        # Cliente Bedrock
        bedrock_client = get_bedrock_client(aws_region, aws_key, aws_secret)

        # PASO 1: Generar prompts con Claude
        with st.spinner("🧠 Generando prompts creativos con Claude..."):
            prompts = generate_prompts(
                game_description,
                bedrock_client,
                "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
            )
            st.success("✅ Prompts generados exitosamente")

            # Mostrar prompts generados
            with st.expander("🔍 Ver prompts generados"):
                for cat, cat_prompts in prompts.items():
                    if cat in categories_to_generate and cat_prompts:
                        st.markdown(f"**{CATEGORY_NAMES.get(cat, cat)}:**")
                        for i, p in enumerate(cat_prompts[:images_per_category], 1):
                            st.text(f"{i}. {p[:100]}...")

        # PASO 2: Generar imágenes
        st.header("🖼️ Generando Imágenes")

        all_generated_images = {}
        total_generated = 0

        for category in categories_to_generate:
            st.subheader(f"📂 {CATEGORY_NAMES.get(category, category)}")

            category_prompts = prompts.get(category, [])[:images_per_category]

            if not category_prompts:
                st.warning(f"No hay prompts para {category}")
                continue

            cols = st.columns(len(category_prompts))
            generated_paths = []

            for idx, (col, prompt) in enumerate(zip(cols, category_prompts), 1):
                with col:
                    with st.spinner(f"Generando {idx}/{len(category_prompts)}..."):
                        try:
                            image_data = generate_image_fal(
                                prompt,
                                image_model,
                                fal_api_key
                            )

                            if image_data:
                                filepath = save_image(image_data, category, idx, project_dir)
                                generated_paths.append(filepath)
                                st.image(image_data, caption=f"Imagen {idx}", use_column_width=True)
                                st.caption(f"💬 {prompt[:80]}...")
                                total_generated += 1
                            else:
                                st.error(f"Error generando imagen {idx}")

                        except Exception as e:
                            st.error(f"Error: {str(e)}")

            all_generated_images[category] = generated_paths

        # Resumen final
        st.divider()
        st.success(f"🎉 Generación completada: {total_generated} imágenes creadas")
        st.info(f"📁 Proyecto guardado en: `{project_dir}`")

        # Guardar metadata
        metadata = {
            "generated_at": datetime.now().isoformat(),
            "game_description": game_description,
            "prompts": prompts,
            "images": all_generated_images,
            "total_images": total_generated
        }

        with open(project_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    except ClientError as e:
        st.error(f"❌ Error de AWS: {str(e)}")
        st.info("Verifica tus credenciales y permisos de Bedrock")

    except Exception as e:
        st.error(f"❌ Error inesperado: {str(e)}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p>Concept Art Generator v3.0 | Powered by Claude + FLUX</p>
    <p>Claude 3.5 Sonnet (prompts) + FLUX via fal.ai (images)</p>
</div>
""", unsafe_allow_html=True)

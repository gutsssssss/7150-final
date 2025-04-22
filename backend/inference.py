import torch
from diffusers import StableDiffusionPipeline, UNet2DConditionModel
from transformers import CLIPTokenizer, CLIPTextModel
from safetensors.torch import load_file

# Use SD 2.1 base components
clip_model_id = "laion/CLIP-ViT-H-14-laion2B-s32B-b79K"
tokenizer = CLIPTokenizer.from_pretrained(clip_model_id)
text_encoder = CLIPTextModel.from_pretrained(clip_model_id)

# Load pipeline with matching text encoder and tokenizer
pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1-base",
    tokenizer=tokenizer,
    text_encoder=text_encoder,
    safety_checker=None,
    torch_dtype=torch.float32,
).to("cpu")

# Load fine-tuned UNet manually
unet_config_path = "C:/YZW_SDE/NEU/Academic/INFO7610/FP/model/config.json"
unet_weights_path = "C:/YZW_SDE/NEU/Academic/INFO7610/FP/model/diffusion_pytorch_model.safetensors"

unet = UNet2DConditionModel.from_config(unet_config_path)
unet.load_state_dict(load_file(unet_weights_path))
pipe.unet = unet.to("cpu")

# Image generation function
def generate_image(prompt: str, steps: int, scale: float) -> str:
    result = pipe(prompt, num_inference_steps=steps, guidance_scale=scale)
    image = result.images[0]
    safe_prompt = prompt.replace(" ", "_").replace(",", "").replace(".", "")[:50]
    filename = f"generated/{safe_prompt}_{steps}_{scale}.png"
    image.save(filename)
    return filename

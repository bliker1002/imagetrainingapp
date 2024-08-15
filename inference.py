import torch
from diffusers import StableDiffusionPipeline
import base64
from io import BytesIO

def model_fn(model_dir):
    model = StableDiffusionPipeline.from_pretrained(model_dir, torch_dtype=torch.float16)
    model = model.to("cuda")
    return model

def predict_fn(data, model):
    prompt = data.pop("prompt", data)
    image = model(prompt).images[0]

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return {'image_base64': image_base64}

def input_fn(request_body, request_content_type):
    if request_content_type == 'application/json':
        return json.loads(request_body)
    else:
        raise ValueError("Unsupported content type: " + request_content_type)

def output_fn(prediction, accept):
    if accept == 'application/json':
        return json.dumps(prediction), accept
    raise ValueError("Unsupported accept type: " + accept)
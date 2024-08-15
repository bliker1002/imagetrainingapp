import torch
from diffusers import StableDiffusionPipeline
from datasets import load_dataset
from transformers import TrainingArguments, Trainer
from aws_manager import AWSManager
from sendgrid_manager import SendGridManager
from finetuning import optimize_finetuning_params

aws_manager = AWSManager()
sendgrid_manager = SendGridManager()

def train_model(user_id):
    # Load dataset
    dataset = load_dataset("imagefolder", data_dir=f"/tmp/{user_id}")

    # Load model
    model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)

    # Optimize finetuning parameters
    labels_path = f"/tmp/{user_id}/labels.json"
    optimized_params = optimize_finetuning_params(labels_path)

    # Training configuration
    training_args = TrainingArguments(
        output_dir=f"/tmp/results/{user_id}",
        num_train_epochs=optimized_params['num_epochs'],
        per_device_train_batch_size=optimized_params['batch_size'],
        learning_rate=optimized_params['learning_rate'],
        max_grad_norm=1.0,
    )

    # Train
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        data_collator=lambda data: {"pixel_values": torch.stack([d["pixel_values"] for d in data])},
    )
    trainer.train()

    # Save model
    model_path = f"/tmp/models/{user_id}"
    model.save_pretrained(model_path)

    # Upload model to S3
    aws_manager.upload_model(user_id, model_path)

    # Send completion email
    sendgrid_manager.send_model_ready_email(user_id)

    # Stop EC2 instance
    aws_manager.stop_ec2_instance()

if __name__ == "__main__":
    import sys
    user_id = sys.argv[1]
    train_model(user_id)
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from aws_manager import AWSManager
from stripe_manager import StripeManager
from sendgrid_manager import SendGridManager
from claude_manager import ClaudeManager
from finetuning import optimize_finetuning_params

app = Flask(__name__)
CORS(app)

aws_manager = AWSManager()
stripe_manager = StripeManager()
sendgrid_manager = SendGridManager()
claude_manager = ClaudeManager()

@app.route('/api/upload', methods=['POST'])
def upload_files():
    if 'images' not in request.files or 'labels' not in request.files:
        return jsonify({'error': 'Missing files'}), 400

    images = request.files['images']
    labels = request.files['labels']

    # Save files temporarily
    images.save('temp_images.zip')
    labels.save('temp_labels.json')

    # Upload to S3
    user_id = request.form.get('user_id')
    aws_manager.upload_file(f'{user_id}/images.zip', 'temp_images.zip')
    aws_manager.upload_file(f'{user_id}/labels.json', 'temp_labels.json')

    # Calculate cost estimate
    image_size = os.path.getsize('temp_images.zip')
    with open('temp_labels.json', 'r') as f:
        labels_data = json.load(f)

    cost = calculate_cost(image_size, len(labels_data))

    # Clean up temp files
    os.remove('temp_images.zip')
    os.remove('temp_labels.json')

    return jsonify({'cost': cost}), 200

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    user_id = f"{data['firstName']}_{data['lastName']}_{data['modelName']}"

    # Create Stripe checkout session
    session_id = stripe_manager.create_checkout_session(data['cost'])

    if session_id:
        # Trigger training job
        aws_manager.start_training_job(user_id)

        # Send welcome email
        sendgrid_manager.send_welcome_email(data['email'], f"{data['firstName']} {data['lastName']}")

        return jsonify({'message': 'Signup successful', 'session_id': session_id, 'user_id': user_id}), 200
    else:
        return jsonify({'error': 'Failed to create payment session'}), 400

@app.route('/api/generate', methods=['POST'])
def generate_image():
    data = request.json
    user_id = data['user_id']
    prompt = data['prompt']

    # Call inference
    image_url = aws_manager.run_inference(user_id, prompt)

    return jsonify({'image_url': image_url}), 200

def calculate_cost(image_size, num_labels):
    # Calculate based on AWS pricing, storage, and processing estimates
    training_cost = (image_size / 1e9) * 0.1  # $0.1 per GB
    storage_cost = (image_size / 1e9) * 0.023 * 30  # $0.023 per GB-month
    inference_cost = num_labels * 0.01  # $0.01 per inference

    total_cost = (training_cost + storage_cost + inference_cost) * 1.4  # Add 40%
    return round(total_cost, 2)

if __name__ == '__main__':
    app.run(debug=True)
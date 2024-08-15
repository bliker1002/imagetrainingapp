import json
from claude_manager import ClaudeManager

def optimize_finetuning_params(labels_path):
    with open(labels_path, 'r') as f:
        labels_data = json.load(f)

    claude_manager = ClaudeManager()
    analysis_result = claude_manager.analyze_labels(json.dumps(labels_data))

    try:
        optimized_params = json.loads(analysis_result)
    except json.JSONDecodeError:
        # Fallback to default values if Claude's output is not valid JSON
        optimized_params = {
            "num_epochs": 100,
            "batch_size": 4,
            "learning_rate": 1e-5
        }

    return optimized_params
#!/usr/bin/env python3
import os
import json
import subprocess

# Call AWS CLI to get the deployed VisualizationBaseUrl
cmd = [
    "aws", "cloudformation", "describe-stacks",
    "--stack-name", "WguCapstoneStack",
    "--query", "Stacks[0].Outputs[?OutputKey=='VisualizationBaseUrl'].OutputValue",
    "--output", "text"
]
result = subprocess.run(cmd, stdout=subprocess.PIPE, check=True)
visualization_base_url = result.stdout.decode().strip()[:-1]

print("\nVisualization Base URL:", visualization_base_url)

# Write to config.json
config_path = "src/server/config.json"
os.makedirs(os.path.dirname(config_path), exist_ok=True)

with open(config_path, "w") as f:
    json.dump({"VISUALIZATION_BASE_URL": visualization_base_url}, f, indent=2)

print(f"✅ Wrote config to {config_path}")

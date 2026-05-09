import json
import os
import re
import sys
import jsonschema
from typing import Optional, Dict, Any

# Ensure we import from the local open-interpreter repo
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "open-interpreter"))

try:
    from interpreter import interpreter
except ImportError:
    print("Error: Could not import Open Interpreter. Make sure it's located at d:/autonomous_driving/open-interpreter")
    sys.exit(1)

from adapters.base import Law

class Translator:
    def __init__(self, model: str):
        self.model = model
        
        # Load the base prompt
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.base_prompt = f.read().strip()
            
        # Load the JSON schema
        schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "schemas", "law_translation.json")
        with open(schema_path, "r", encoding="utf-8") as f:
            self.schema = json.load(f)
            
        # Configure Open Interpreter
        interpreter.llm.model = self.model
        interpreter.auto_run = True
        interpreter.disable_telemetry = True
        interpreter.conversation_history = False
        
        # Override the system message for pure text-to-JSON
        interpreter.system_message = """You are a legal-to-vision translation engine.
You receive traffic law text and output ONLY valid JSON.
Do not write or execute any code. Do not use markdown fences.
Output the JSON object directly."""

    def translate_law(self, law: Law, max_retries=2) -> Dict[str, Any]:
        """Send one law to OI, return the parsed JSON dict."""
        full_prompt = f"{self.base_prompt}\n\nLaw ID: {law.id}\n{law.body}"
        
        for attempt in range(max_retries + 1):
            # Reset conversation so each law is independent
            interpreter.messages = []
            
            new_messages = interpreter.chat(full_prompt, display=False)
            
            # Extract assistant text
            assistant_text = ""
            for msg in new_messages:
                if msg.get("role") == "assistant" and msg.get("type") == "message":
                    assistant_text += msg.get("content", "")
            
            assistant_text = assistant_text.strip()
            
            # Clean markdown fences if the LLM ignored the instruction
            json_str = self._extract_json(assistant_text)
            
            try:
                data = json.loads(json_str)
                # Validate against schema
                jsonschema.validate(instance=data, schema=self.schema)
                return {
                    "law_id": law.id,
                    "status": "ok",
                    "translation": data,
                    "raw_text": law.body,
                    "source_url": law.source_url
                }
            except json.JSONDecodeError as e:
                error_msg = f"Failed to parse JSON. Error: {e}"
            except jsonschema.exceptions.ValidationError as e:
                error_msg = f"JSON did not match schema. Error: {e.message}"
            
            print(f"  [Attempt {attempt+1}] {error_msg}")
            
            if attempt < max_retries:
                full_prompt = f"Your previous output had an error: {error_msg}\n\nPlease fix the JSON and return ONLY valid JSON."
                
        return {
            "law_id": law.id,
            "status": "needs_review",
            "error": error_msg,
            "raw_output": assistant_text,
            "raw_text": law.body,
            "source_url": law.source_url
        }

    def _extract_json(self, text: str) -> str:
        """Extract JSON block from markdown fences if present."""
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            return match.group(1)
        
        # Sometimes it just puts the `{` and `}` without fences, but with surrounding text.
        match = re.search(r"(\{.*\})", text, re.DOTALL)
        if match:
            return match.group(1)
            
        return text

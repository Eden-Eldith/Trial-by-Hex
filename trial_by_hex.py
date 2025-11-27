#!/usr/bin/env python3
"""
trial_by_hex.py
Submit document to 6 different AI models for blind review.
Uses OpenRouter API for access to diverse models (Claude, GPT, Gemini, Llama, etc.)

Set OPENROUTER_API_KEY environment variable or use a .env file.

Author: Eden Eldith & Claude Opus 4.5
"""
import os
import sys
import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime

# Load .env file if it exists (for API key)
try:
    from dotenv import load_dotenv
    # Look for .env in script directory and current working directory
    script_dir = Path(__file__).parent.resolve()
    env_paths = [
        script_dir / '.env',
        Path.cwd() / '.env',
    ]
    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            break
except ImportError:
    pass  # python-dotenv not installed, rely on environment variable

try:
    import requests
except ImportError:
    print("=" * 60)
    print("ERROR: requests package not installed.")
    print("=" * 60)
    print("\nInstall with:")
    print("  pip install requests")
    print("\nOr install all dependencies:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

# OpenRouter API configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')

# Configure 6 diverse reviewer models/personas
# Using different model families for true diversity of perspective
# Mix of premium and cost-effective models
REVIEWERS = [
    {
        "model": "anthropic/claude-sonnet-4.5",
        "persona": "technical specialist focused on methodology and rigor"
    },
    {
        "model": "openai/gpt-5.1",
        "persona": "skeptical critic looking for weaknesses and logical gaps"
    },
    {
        "model": "google/gemini-3-pro-preview",
        "persona": "constructive reviewer focused on practical improvement"
    },
    {
        "model": "x-ai/grok-4.1-fast:free",
        "persona": "accessibility reviewer checking clarity for general audience"
    },
    {
        "model": "deepseek/deepseek-chat-v3.1",
        "persona": "literature reviewer checking connections to existing work"
    },
    {
        "model": "openai/gpt-5-mini",
        "persona": "experimental design and reproducibility reviewer"
    },
]

# Fallback models if primary ones fail (cheap/free options)
FALLBACK_MODELS = [
    "x-ai/grok-4.1-fast:free",
    "anthropic/claude-haiku-4.5",
    "openai/gpt-5-nano",
]


def openrouter_request(model: str, messages: List[Dict], max_tokens: int = 1500) -> str:
    """Make a request to OpenRouter API."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/Eden-Eldith/Trial-by-Hex",
        "X-Title": "Trial by Hex - Multi-Model Peer Review",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens
    }

    response = requests.post(
        OPENROUTER_BASE_URL,
        headers=headers,
        json=payload,
        timeout=120
    )
    response.raise_for_status()

    data = response.json()
    return data['choices'][0]['message']['content']


def get_review(content: str, persona: str, model: str) -> str:
    """Get a single blind review from a specific model."""
    messages = [
        {
            "role": "system",
            "content": f"""You are a {persona} conducting a blind peer review.

Evaluate this work on:
1. Technical accuracy
2. Clarity of argument
3. Evidence quality
4. Novel contribution
5. Weaknesses and gaps

Be specific. Cite sections. Provide actionable feedback.
Do NOT reference author credentials or affiliations - this is blind review.
Focus purely on the quality of the work itself."""
        },
        {
            "role": "user",
            "content": content
        }
    ]

    try:
        return openrouter_request(model, messages, max_tokens=1500)
    except Exception as e:
        # Try fallback models
        for fallback in FALLBACK_MODELS:
            try:
                print(f"    Falling back to {fallback}...")
                return openrouter_request(fallback, messages, max_tokens=1500)
            except:
                continue
        raise e


def synthesize_reviews(reviews: List[str], synthesis_model: str = "anthropic/claude-opus-4.5") -> str:
    """Synthesize 6 reviews into actionable summary using Opus 4.5."""
    combined = "\n\n---REVIEW---\n\n".join(reviews)

    messages = [
        {
            "role": "system",
            "content": """Synthesize these 6 blind reviews into a single actionable summary.

OUTPUT FORMAT:
## High Consensus (4+ reviewers agree)
[Issues most reviewers flagged]

## Moderate Consensus (2-3 reviewers)
[Issues some reviewers noted]

## Minority Concerns (1 reviewer, but substantive)
[Individual concerns worth considering]

## Strengths (what reviewers praised)
[Positive feedback]

## VERDICT
PASS: Ready for publication with minor edits
REVISE: Needs significant revision, re-review recommended
REJECT: Fundamental issues need addressing

Remove any credentialism-based dismissals. Focus on substance."""
        },
        {
            "role": "user",
            "content": combined
        }
    ]

    return openrouter_request(synthesis_model, messages, max_tokens=2000)


def trial_by_hex(input_file: str, output_file: str) -> Dict:
    """Run full trial by hex on a document."""
    if not OPENROUTER_API_KEY:
        print("=" * 60)
        print("ERROR: OPENROUTER_API_KEY not set!")
        print("=" * 60)
        print("\nOption 1 - Environment variable:")
        print("  Linux/Mac:       export OPENROUTER_API_KEY='your-key-here'")
        print("  Windows (PS):    $env:OPENROUTER_API_KEY = 'your-key-here'")
        print("  Windows (CMD):   set OPENROUTER_API_KEY=your-key-here")
        print("\nOption 2 - Create a .env file:")
        print("  Copy .env.example to .env and add your key")
        print("\nTo get an API key:")
        print("  1. Go to https://openrouter.ai")
        print("  2. Sign in or create account")
        print("  3. Navigate to Keys section")
        print("  4. Create new API key")
        return {"passed": False, "synthesis": "API key not set"}

    # Resolve input path (support both relative and absolute paths)
    input_path = Path(input_file).resolve()
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        return {"passed": False, "synthesis": "Input file not found"}

    content = input_path.read_text(encoding='utf-8')

    print("=" * 60)
    print("  TRIAL BY HEX - Multi-Model Blind Peer Review")
    print("  Powered by OpenRouter (Claude, GPT, Gemini, Llama)")
    print("=" * 60)
    print(f"\nDocument: {input_path}")
    print(f"Collecting 6 diverse blind reviews...\n")

    reviews = []
    for i, reviewer in enumerate(REVIEWERS):
        model_short = reviewer['model'].split('/')[-1]
        print(f"  [{i+1}/6] {model_short}: {reviewer['persona'][:40]}...")
        try:
            review = get_review(content, reviewer['persona'], reviewer['model'])
            reviews.append(review)
            print(f"        ✓ Complete")
        except Exception as e:
            print(f"        ✗ Error: {e}")
            reviews.append(f"Review failed: {e}")

    print("\nSynthesizing reviews with Claude Opus 4.5...")
    synthesis = synthesize_reviews(reviews)

    # Determine verdict
    passed = "PASS" in synthesis.upper()

    # Resolve output path
    output_path = Path(output_file).resolve()

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(f"""# Trial by Hex Review

**Document:** {input_path.name}
**Date:** {datetime.now().isoformat()}
**Verdict:** {"✓ PASSED" if passed else "⚠ NEEDS REVISION"}
**Reviewers:** 6 diverse AI models via OpenRouter

---

## Synthesized Review

{synthesis}

---

## Individual Reviews

""" + "".join(f"""### Reviewer {i+1}: {REVIEWERS[i]['model'].split('/')[-1]}
**Persona:** {REVIEWERS[i]['persona']}

{r}

---

""" for i, r in enumerate(reviews)), encoding='utf-8')

    print(f"\n{'=' * 60}")
    print(f"  Review saved to: {output_path}")
    print(f"  Verdict: {'✓ PASSED' if passed else '⚠ NEEDS REVISION'}")
    print(f"{'=' * 60}")

    return {"passed": passed, "synthesis": synthesis}


def print_usage():
    """Print usage information."""
    print("=" * 60)
    print("  TRIAL BY HEX - Multi-Model Blind Peer Review")
    print("=" * 60)
    print("\nUsage: python trial_by_hex.py <input_file> <output_file>")
    print("\nExamples:")
    print('  python trial_by_hex.py ./thesis.md ./thesis_review.md')
    print('  python trial_by_hex.py "path/to/document.txt" "path/to/review.md"')
    print("\nReviewers (6 diverse models):")
    for r in REVIEWERS:
        print(f"  • {r['model']}: {r['persona']}")
    print("\nSetup:")
    print("  1. pip install -r requirements.txt")
    print("  2. Set OPENROUTER_API_KEY (env var or .env file)")
    print("\nGet your API key at: https://openrouter.ai")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    trial_by_hex(sys.argv[1], sys.argv[2])

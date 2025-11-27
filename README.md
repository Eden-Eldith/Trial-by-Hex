**Fork it - Mess with it - Change the models - Change the prompts c: - Create your own council!**

![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![OpenRouter](https://img.shields.io/badge/API-OpenRouter-purple.svg)

# Trial by Hex

**Multi-Model Blind Peer Review System**

Submit your documents to multiple AI models for comprehensive, unbiased peer review. Each reviewer brings a unique perspective, ensuring thorough analysis from technical rigor to ethical considerations. Then Claude Opus 4.5 synthesizes each response into a meta-review.

## Features

- **Blind Review**: Removes author identity to prevent bias
- **Diverse Perspectives**: Uses different AI models with distinct personas
- **Multi-dimensional Analysis**: Covers methodology, logic, ethics, feasibility, and more
- **Automated Synthesis**: Consolidates feedback into actionable summaries with verdicts
- **Fallback Handling**: Automatically uses backup models if primary ones fail

## Two Versions

### Trial by Hex (Standard)
6 diverse reviewers covering traditional peer review perspectives:

| # | Model | Role |
|---|-------|------|
| 1 | Claude Sonnet 4.5 | Technical specialist (methodology & rigor) |
| 2 | GPT-5.1 | Skeptical critic (weaknesses & logical gaps) |
| 3 | Gemini 3 Pro | Constructive reviewer (practical improvement) |
| 4 | Grok 4.1 | Accessibility reviewer (clarity for general audience) |
| 5 | DeepSeek Chat v3.1 | Literature reviewer (connections to existing work) |
| 6 | GPT-5 Mini | Reproducibility reviewer (experimental design) |

### Trial by Hex+ (Enhanced)
12 specialized reviewers (original 6 + 6 philosophical/systems reviewers):

| # | Reviewer | Focus |
|---|----------|-------|
| 7 | The Logical Consistency Reviewer | Laws of Logic, Godel's Theorems, category errors |
| 8 | The Semantic Analyst | Wittgensteinian language debugging, definitions |
| 9 | The Ethical Alignment Sentinel | Bias detection, societal impact, safety |
| 10 | The Systems Architect | Feasibility, scalability, implementation |
| 11 | The Interdisciplinary Catalyst | Cross-domain connections, missed literature |
| 12 | The Steel Man Advocate | Charitable interpretation, strongest version |

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install requests python-dotenv
```

### 2. Set Up Your API Key

Get your API key from [OpenRouter](https://openrouter.ai):
1. Sign in or create an account
2. Navigate to the Keys section
3. Create a new API key

Then set it up using one of these methods:

**Option A: Environment Variable (Recommended for one-time use)**

```bash
# Linux/Mac
export OPENROUTER_API_KEY='your-key-here'

# Windows (PowerShell)
$env:OPENROUTER_API_KEY = 'your-key-here'

# Windows (CMD)
set OPENROUTER_API_KEY=your-key-here
```

**Option B: .env File (Recommended for persistent use)**

Create a `.env` file in the project directory:
```
OPENROUTER_API_KEY=your-key-here
```

### 3. Run a Review

**Standard (6 reviewers):**
```bash
python trial_by_hex.py ./your_document.md ./review_output.md
```

**Enhanced (12 reviewers):**
```bash
python trial_by_hex_plus.py ./your_document.md ./review_output.md
```

## Output Format

The review output includes:

1. **Synthesized Review** - Consensus-based summary with:
   - Critical issues (4+ reviewers agree)
   - Significant concerns (2-3 reviewers)
   - Individual considerations
   - Strengths
   - Overall verdict (PASS / REVISE / REJECT)

2. **Individual Reviews** - Full feedback from each reviewer

### Example Output Structure (Standard version)

```markdown
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
```

### Example Output Structure (Plus version)

```markdown
## CRITICAL ISSUES (Consensus across multiple reviewers)
[Issues flagged by 4+ reviewers - these are blockers]

## SIGNIFICANT CONCERNS (2-3 reviewers)
[Important issues worth addressing]

## CONSIDERATIONS (Single reviewer, but substantive)
[Individual concerns that deserve thought]

## STRENGTHS (What reviewers praised)
[Positive consensus]

## LOGICAL/FORMAL ISSUES
[From the Logical Consistency Reviewer - Godelian concerns, self-reference issues]

## LINGUISTIC CLARITY
[From the Semantic Analyst - language bewitchments, definition problems]

## ETHICAL CONSIDERATIONS
[From the Ethical Alignment Sentinel - bias, impact, safety]

## IMPLEMENTATION FEASIBILITY
[From the Systems Architect - can it be built?]

## INTERDISCIPLINARY CONNECTIONS
[From the Interdisciplinary Catalyst - missed connections, synthesis opportunities]

## STEEL MANNED VERSION
[From the Steel Man Advocate - the strongest form of the argument]

## VERDICT
**Technical Quality:** ⭐⭐⭐⭐☆
**Logical Coherence:** ⭐⭐⭐⭐☆
**Ethical Alignment:** ⭐⭐⭐⭐⭐
**Feasibility:** ⭐⭐⭐☆☆
**Novelty:** ⭐⭐⭐⭐☆

**Overall:** REVISE

**Priority Actions:**
1. [Most important fix]
2. [Second priority]
3. [Third priority]
```

## Requirements

- Python 3.7+
- `requests` library
- `python-dotenv` library (optional, for .env file support)
- OpenRouter API key

## Cost Considerations

Trial by Hex uses multiple AI models via OpenRouter. Costs vary by model:

- **Standard (6 reviewers)**: ~$0.10-0.50 per review (varies by document length)
- **Plus (12 reviewers)**: ~$0.20-1.00 per review (uses more premium models)

The scripts include fallback to cheaper/free models if primary models fail.

## Supported Input Formats

Any text-based document:
- Markdown (.md)
- Plain text (.txt)
- Academic papers
- Research proposals
- Technical documentation
- Essays and articles

## Project Structure

```
Trial-by-Hex/
├── trial_by_hex.py      # Standard 6-reviewer version
├── trial_by_hex_plus.py # Enhanced 12-reviewer version
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment file
├── README.md            # This file
└── LICENSE              # MIT License
```

## Troubleshooting

### "OPENROUTER_API_KEY environment variable not set"
Make sure you've set your API key using one of the methods above. If using a .env file, ensure it's in the same directory where you run the script.

### "requests package not installed"
Run: `pip install requests`

### Model errors or timeouts
The scripts automatically fall back to cheaper models. If issues persist, check your OpenRouter account for rate limits or credit balance.

### Encoding errors
The scripts use UTF-8 encoding. Ensure your input documents are saved with UTF-8 encoding.

## License

MIT License - Copyright 2025 Eden_Eldith

See [LICENSE](LICENSE) for details.

## Authors

- Eden Eldith
- Claude Opus 4.5

## Contributing

Contributions welcome! Feel free to:
- Add new reviewer personas
- Improve synthesis prompts
- Add support for additional output formats
- Enhance error handling

---

*"Six reviewers stand in judgment. None know whose work they judge. Let the ideas speak for themselves."*

<p align="center">Made with 🧠 by humans and AIs in collaboration</p>

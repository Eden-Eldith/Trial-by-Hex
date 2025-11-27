#!/usr/bin/env python3
"""
trial_by_hex_plus.py
Enhanced multi-model blind review with 12 specialized agents.
Original 6 + 6 new philosophical/systems reviewers.

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
    print("=" * 70)
    print("ERROR: requests package not installed.")
    print("=" * 70)
    print("\nInstall with:")
    print("  pip install requests")
    print("\nOr install all dependencies:")
    print("  pip install -r requirements.txt")
    sys.exit(1)

# OpenRouter API configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')

# Original 6 reviewers
ORIGINAL_REVIEWERS = [
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

# New specialized agents for trial_by_hex+
PLUS_REVIEWERS = [
    {
        "model": "anthropic/claude-opus-4.5",
        "name": "The Logical Consistency Reviewer",
        "persona": """logician and meta-theorist enforcing the Laws of Logic.

Your mandate:
1. Enforce the Laws of Logic:
   - Law of Identity (A = A)
   - Law of Non-Contradiction (¬(A ∧ ¬A))
   - Law of Excluded Middle (A ∨ ¬A)

2. Apply Godel's Incompleteness Theorems as meta-constraints:
   - Identify claims the system cannot self-validate
   - Flag statements requiring axioms outside the work's framework
   - Note where the work attempts to prove its own consistency

3. Detect:
   - Category errors (treating unlike things as equivalent)
   - Hidden assumptions masquerading as conclusions
   - Self-referential loops and paradoxes
   - Statements unprovable within the stated system
   - Claims requiring unstated extra axioms
   - Places where the work transcends its own formal definitions

Output format:
## Logical Violations
[Specific violations of identity, non-contradiction, excluded middle]

## Godelian Concerns
[Self-validation attempts, incompleteness issues]

## Category Errors
[Misapplied categories, type mismatches]

## Hidden Assumptions
[Unstated premises, smuggled axioms]

## Self-Referential Issues
[Loops, paradoxes, bootstrap problems]

## Formal Boundary Transgressions
[Where work exceeds its stated scope]"""
    },
    {
        "model": "anthropic/claude-sonnet-4.5",
        "name": "The Semantic Analyst (The Wittgensteinian)",
        "persona": """Wittgensteinian language analyst focused on linguistic precision and meaning-as-use.

Your mandate is to DEBUG THE LANGUAGE ITSELF:

1. Catch where the author is "bewitched by language":
   - Words used to hide lack of understanding
   - Technical jargon creating illusion of precision
   - Metaphors mistaken for explanations
   - Language games misapplied across contexts

2. Examine definitions:
   - Are key terms defined operationally or circularly?
   - Do definitions shift mid-argument (equivocation)?
   - Are there ostensive definitions that actually point to nothing?

3. Check "meaning as use":
   - Would this language mean anything in practice?
   - Is the author using private language impossible to verify?
   - Are there language games that have no clear rules?

4. Identify:
   - Meaningless sentences disguised as profound
   - Category mistakes from linguistic confusion
   - Pseudo-problems created by grammatical illusions
   - Where "whereof one cannot speak, thereof one must be silent" applies

Output format:
## Linguistic Bewitchments
[Where language creates illusions]

## Definition Problems
[Circular, shifting, or empty definitions]

## Meaning-as-Use Failures
[Language without practical grounding]

## Pseudo-Problems
[Issues created by language confusion, not reality]

## Recommended Clarifications
[Specific rewrites for clarity]"""
    },
    {
        "model": "openai/gpt-5.1",
        "name": "The Ethical Alignment Sentinel",
        "persona": """ethical analyst focused on bias, societal impact, and safety.

Your mandate is to check SECOND-ORDER EFFECTS:

1. Who gets hurt?
   - Direct harm from proposed ideas
   - Indirect harm from implementation
   - Harm to marginalized groups
   - Power asymmetries created or reinforced

2. Is the language exclusionary?
   - Gatekeeping terminology
   - Cultural assumptions presented as universal
   - Accessibility barriers (cognitive, educational, linguistic)
   - Who is implicitly addressed vs. excluded?

3. What are the unintended consequences?
   - Dual-use concerns
   - Weaponization potential
   - Surveillance/control implications
   - Environmental/resource costs
   - Labor displacement effects

4. Bias detection:
   - Dataset biases (if empirical)
   - Selection biases in evidence
   - Confirmation bias in argumentation
   - WEIRD (Western, Educated, Industrialized, Rich, Democratic) assumptions

5. Safety considerations:
   - Infohazards
   - Misuse pathways
   - Reversibility of proposed changes
   - Precautionary principle violations

Output format:
## Direct Harm Vectors
[Who could be harmed and how]

## Exclusionary Elements
[Language, framing, or assumptions that exclude]

## Unintended Consequences
[Second and third-order effects]

## Detected Biases
[Systematic blind spots]

## Safety Concerns
[Risks, misuse potential, irreversibility]

## Recommendations
[How to mitigate identified issues]"""
    },
    {
        "model": "google/gemini-3-pro-preview",
        "name": "The Systems Architect",
        "persona": """systems engineer focused on feasibility, scalability, and implementation.

IGNORE whether the idea is TRUE. Focus on whether it can be BUILT and SUSTAINED.

Your mandate:

1. Feasibility analysis:
   - Technical prerequisites
   - Resource requirements (compute, data, personnel)
   - Dependency chains
   - Current state of enabling technologies

2. Scalability assessment:
   - Does it work at 10x? 100x? 1000x?
   - What breaks first under load?
   - Bottlenecks and chokepoints
   - Coordination costs at scale

3. Implementation roadmap:
   - Critical path to MVP
   - Irreducible complexity
   - Integration points with existing systems
   - Migration pathways

4. Technical debt detection:
   - Shortcuts that will compound
   - Abstractions that leak
   - Maintenance burden over time
   - Documentation debt

5. Resource constraints:
   - Capital requirements
   - Human expertise availability
   - Time-to-implementation
   - Opportunity costs

6. Failure modes:
   - Single points of failure
   - Cascade failure risks
   - Recovery pathways
   - Graceful degradation options

Output format:
## Feasibility Assessment
[Can this be built? What's missing?]

## Scalability Analysis
[Where does it break at scale?]

## Implementation Critical Path
[Key milestones and dependencies]

## Technical Debt
[Hidden costs and shortcuts]

## Resource Requirements
[What's actually needed?]

## Failure Modes
[How will this break?]

## VERDICT: Build / Prototype First / Redesign / Infeasible"""
    },
    {
        "model": "deepseek/deepseek-chat-v3.1",
        "name": "The Interdisciplinary Catalyst",
        "persona": """interdisciplinary synthesist focused on lateral thinking and cross-domain connections.

Your mandate is to BREAK SILOED THINKING:

1. Cross-domain connections the author missed:
   - Biology: evolutionary parallels, ecological dynamics, homeostasis
   - Physics: thermodynamics, information theory, symmetry/conservation
   - Mathematics: topology, category theory, dynamical systems
   - History: precedents, cycles, analogous transformations
   - Art: aesthetic principles, creative processes, perception
   - Anthropology: cultural variations, ritual structures
   - Economics: incentive structures, market dynamics
   - Psychology: cognitive biases, behavioral patterns

2. Structural isomorphisms:
   - What other systems exhibit the same pattern?
   - What metaphors from other fields illuminate this?
   - Where has this problem been solved under a different name?

3. Missed literature:
   - Obscure but relevant fields
   - Historical work predating modern framing
   - Non-Western intellectual traditions
   - Practitioner knowledge not in academic literature

4. Synthesis opportunities:
   - How could insights from other fields strengthen the argument?
   - What would a physicist/biologist/historian notice immediately?
   - Where is the author reinventing an existing wheel?

5. Anti-siloing prompts:
   - "This is isomorphic to [X] in [field]"
   - "The [field] literature calls this [term]"
   - "This was solved by [person] in [year] via [method]"

Output format:
## Missed Connections
[Relevant work from other fields]

## Structural Isomorphisms
[Same pattern under different names]

## Cross-Domain Insights
[What other fields would notice]

## Synthesis Opportunities
[How to strengthen via interdisciplinary bridging]

## Reinvented Wheels
[Where existing solutions apply]

## Recommended Reading
[Specific sources from unexpected fields]"""
    },
    {
        "model": "x-ai/grok-4.1-fast:free",
        "name": "The Steel Man Advocate",
        "persona": """charitable interpreter focused on making the STRONGEST possible version of the argument.

Unlike skeptical reviewers, your job is to STRENGTHEN the author's case.

Your mandate:

1. Charitable interpretation:
   - Assume the author means the most defensible version
   - Fill gaps with the best possible arguments
   - Steelman weak points into strong ones
   - Find the insight even in confused exposition

2. Potential identification:
   - What is the author TRYING to say that they failed to articulate?
   - What's the diamond in the rough?
   - If this idea were fully developed, what would it become?
   - What adjacent ideas would make this stronger?

3. Argument reconstruction:
   - Rebuild weak arguments in their strongest form
   - Supply missing premises that would make conclusions valid
   - Reframe in more defensible language
   - Connect to established frameworks that support the claim

4. Defense preparation:
   - Anticipate objections and prepare responses
   - Identify which criticisms the author can actually answer
   - Find evidence the author could have cited
   - Suggest framings that preempt common attacks

5. Vision articulation:
   - If this is right, why does it matter?
   - What's the best-case scenario if this succeeds?
   - Who would this help and how?
   - What does the world look like if this idea wins?

Output format:
## Core Insight (Steel Manned)
[The strongest version of the main claim]

## Unrealized Potential
[What the author is reaching for but not quite grasping]

## Reconstructed Arguments
[Weak points made strong]

## Defense Preparation
[Answers to likely objections]

## Best-Case Vision
[Why this matters if it succeeds]

## Suggested Strengthening
[Specific additions that would make this compelling]"""
    },
]

# Combined list
REVIEWERS = ORIGINAL_REVIEWERS + PLUS_REVIEWERS

# Fallback models if primary ones fail
FALLBACK_MODELS = [
    "x-ai/grok-4.1-fast:free",
    "anthropic/claude-haiku-4.5",
    "openai/gpt-5-nano",
]


def openrouter_request(model: str, messages: List[Dict], max_tokens: int = 2000) -> str:
    """Make a request to OpenRouter API."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/Eden-Eldith/Trial-by-Hex",
        "X-Title": "Trial by Hex+ - Enhanced Multi-Model Peer Review",
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
        timeout=180  # Longer timeout for complex analysis
    )
    response.raise_for_status()

    data = response.json()
    return data['choices'][0]['message']['content']


def get_review(content: str, reviewer: Dict) -> str:
    """Get a single blind review from a specific model."""
    # Check if this is an original reviewer or plus reviewer
    if "name" in reviewer:
        # Plus reviewer with specialized persona
        system_prompt = f"""You are {reviewer['name']}, a {reviewer['persona']}

You are conducting a blind peer review. Focus ONLY on your specialized domain.
Do NOT reference author credentials or affiliations - this is blind review.
Be specific. Cite sections. Provide actionable feedback."""
    else:
        # Original reviewer
        system_prompt = f"""You are a {reviewer['persona']} conducting a blind peer review.

Evaluate this work on:
1. Technical accuracy
2. Clarity of argument
3. Evidence quality
4. Novel contribution
5. Weaknesses and gaps

Be specific. Cite sections. Provide actionable feedback.
Do NOT reference author credentials or affiliations - this is blind review.
Focus purely on the quality of the work itself."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": content}
    ]

    try:
        return openrouter_request(reviewer['model'], messages, max_tokens=2000)
    except Exception as e:
        # Try fallback models
        for fallback in FALLBACK_MODELS:
            try:
                print(f"    Falling back to {fallback}...")
                return openrouter_request(fallback, messages, max_tokens=2000)
            except:
                continue
        raise e


def synthesize_reviews(reviews: List[str], reviewer_info: List[Dict], synthesis_model: str = "anthropic/claude-opus-4.5") -> str:
    """Synthesize all reviews into actionable summary using Opus 4.5."""
    # Format reviews with reviewer identity
    formatted_reviews = []
    for i, (review, reviewer) in enumerate(zip(reviews, reviewer_info)):
        name = reviewer.get('name', f"Reviewer {i+1}")
        formatted_reviews.append(f"### {name}\n{review}")

    combined = "\n\n---REVIEW---\n\n".join(formatted_reviews)

    messages = [
        {
            "role": "system",
            "content": """Synthesize these 12 specialized blind reviews into a comprehensive actionable summary.

The reviewers include:
- 6 traditional academic reviewers (methodology, skeptic, constructive, accessibility, literature, reproducibility)
- 6 specialized philosophical/systems reviewers:
  - Logical Consistency Reviewer (Godelian analysis)
  - Semantic Analyst (Wittgensteinian language debugging)
  - Ethical Alignment Sentinel (bias and impact)
  - Systems Architect (feasibility and implementation)
  - Interdisciplinary Catalyst (cross-domain connections)
  - Steel Man Advocate (charitable strongest interpretation)

OUTPUT FORMAT:

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

**Technical Quality:** [1-5 stars]
**Logical Coherence:** [1-5 stars]
**Ethical Alignment:** [1-5 stars]
**Feasibility:** [1-5 stars]
**Novelty:** [1-5 stars]

**Overall:** PASS | REVISE | REJECT

**Priority Actions:**
1. [Most important fix]
2. [Second priority]
3. [Third priority]

Remove any credentialism-based dismissals. Focus on substance."""
        },
        {
            "role": "user",
            "content": combined
        }
    ]

    return openrouter_request(synthesis_model, messages, max_tokens=3000)


def trial_by_hex_plus(input_file: str, output_file: str) -> Dict:
    """Run full trial by hex+ on a document with 12 specialized reviewers."""
    if not OPENROUTER_API_KEY:
        print("=" * 70)
        print("ERROR: OPENROUTER_API_KEY not set!")
        print("=" * 70)
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

    print("=" * 70)
    print("  TRIAL BY HEX+ - Enhanced Multi-Model Blind Peer Review")
    print("  12 Specialized Reviewers (6 Traditional + 6 Philosophical)")
    print("  Powered by OpenRouter")
    print("=" * 70)
    print(f"\nDocument: {input_path}")
    print(f"\nOriginal Reviewers (1-6):")
    for i, r in enumerate(ORIGINAL_REVIEWERS):
        print(f"   [{i+1}] {r['model'].split('/')[-1]}: {r['persona'][:50]}...")
    print(f"\nPlus Reviewers (7-12):")
    for i, r in enumerate(PLUS_REVIEWERS):
        print(f"   [{i+7}] {r['name']}")
    print(f"\nCollecting 12 specialized blind reviews...\n")

    reviews = []
    for i, reviewer in enumerate(REVIEWERS):
        model_short = reviewer['model'].split('/')[-1]
        name = reviewer.get('name', reviewer['persona'][:40])
        print(f"  [{i+1:2}/12] {name}...")
        try:
            review = get_review(content, reviewer)
            reviews.append(review)
            print(f"          Complete ({model_short})")
        except Exception as e:
            print(f"          Error: {e}")
            reviews.append(f"Review failed: {e}")

    print("\nSynthesizing 12 reviews with Claude Opus 4.5...")
    synthesis = synthesize_reviews(reviews, REVIEWERS)

    # Determine verdict
    passed = "PASS" in synthesis.upper() and "REJECT" not in synthesis.upper()

    # Resolve output path
    output_path = Path(output_file).resolve()

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Build individual reviews section
    individual_reviews = ""
    for i, (review, reviewer) in enumerate(zip(reviews, REVIEWERS)):
        name = reviewer.get('name', f"Reviewer {i+1}")
        persona = reviewer.get('persona', '')[:200]
        individual_reviews += f"""### {i+1}. {name}
**Model:** {reviewer['model']}
**Focus:** {persona[:100]}{"..." if len(persona) > 100 else ""}

{review}

---

"""

    output_path.write_text(f"""# Trial by Hex+ Review

**Document:** {input_path.name}
**Date:** {datetime.now().isoformat()}
**Verdict:** {"PASSED" if passed else "NEEDS REVISION"}
**Reviewers:** 12 specialized AI reviewers via OpenRouter

---

## Synthesized Review

{synthesis}

---

## Individual Reviews

{individual_reviews}
""", encoding='utf-8')

    print(f"\n{'=' * 70}")
    print(f"  Review saved to: {output_path}")
    print(f"  Verdict: {'PASSED' if passed else 'NEEDS REVISION'}")
    print(f"{'=' * 70}")

    return {"passed": passed, "synthesis": synthesis}


def print_usage():
    """Print usage information."""
    print("=" * 70)
    print("  TRIAL BY HEX+ - Enhanced Multi-Model Blind Peer Review")
    print("  12 Specialized Reviewers for Rigorous Analysis")
    print("=" * 70)
    print("\nUsage: python trial_by_hex_plus.py <input_file> <output_file>")
    print("\nExamples:")
    print('  python trial_by_hex_plus.py ./thesis.md ./thesis_review.md')
    print('  python trial_by_hex_plus.py "path/to/document.txt" "path/to/review.md"')
    print("\nOriginal Reviewers (1-6):")
    for i, r in enumerate(ORIGINAL_REVIEWERS):
        print(f"  {i+1}. {r['model']}")
        print(f"     -> {r['persona']}")
    print("\nPlus Reviewers (7-12):")
    for i, r in enumerate(PLUS_REVIEWERS):
        print(f"  {i+7}. {r['name']}")
        print(f"     -> {r['model']}")
    print("\nSetup:")
    print("  1. pip install -r requirements.txt")
    print("  2. Set OPENROUTER_API_KEY (env var or .env file)")
    print("\nGet your API key at: https://openrouter.ai")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    trial_by_hex_plus(sys.argv[1], sys.argv[2])

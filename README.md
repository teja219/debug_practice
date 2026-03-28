# OrderFlow — System Debugging Interview

## Files in this folder

| File | Who sees it | Purpose |
|------|-------------|---------|
| `system_spec.md` | Candidate | Reference architecture & design |
| `reported_problems.md` | Candidate | The 6 bug reports to diagnose |
| `buggy_system.py` | Candidate | The implementation to review |
| `answer_key_INTERVIEWER_ONLY.py` | Interviewer only | Root causes + scoring hints |

## Interview Flow

1. Share `system_spec.md` and `reported_problems.md` with the candidate first.
2. Then reveal `buggy_system.py` for them to cross-reference.
3. Ask them to talk through each problem — root cause, location, and fix.
4. Use `answer_key_INTERVIEWER_ONLY.py` privately to score responses.

## What to evaluate

- **Accuracy** — Do they find the right line / mechanism?
- **Reasoning** — Can they explain *why* it's a bug vs just pointing at it?
- **Fix quality** — Is the proposed fix correct and production-appropriate?
- **Spec awareness** — Do they notice when the code violates the spec?

## Running the answer key

```bash
python answer_key_INTERVIEWER_ONLY.py
```

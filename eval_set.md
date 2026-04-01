# Evaluation Set: Meeting → Action Items Extraction

## Task Definition
Given a meeting transcript (possibly noisy, long, and unstructured), extract clear, actionable to-do items.

Each output should:
- Focus only on actionable tasks (not general discussion)
- Be concise and structured
- Include responsible person (if mentioned)
- Include deadline (if mentioned)
- Avoid hallucinating missing information

---

## Case 1 — Normal Case ✅

### Input
Team meeting notes:

"Alright, quick updates. John finished the frontend login page. Sarah, can you finalize the API integration by Friday? Also, we need someone to prepare slides for Monday’s client meeting. Mike, can you take that? Oh and we should fix the payment bug reported yesterday."

### Expected Behavior
- Extract all actionable items
- Assign owners where specified
- Capture deadlines

### Good Output Should:
- Include:
  - Sarah → API integration → deadline Friday
  - Mike → prepare slides → deadline Monday
  - Fix payment bug → (no owner, should not hallucinate)
- Ignore "John finished..." (not a task)

---

## Case 2 — Edge Case (Very Noisy / Small Talk Heavy) ⚠️

### Input
"Hey everyone, how was your weekend? Mine was great. Anyway, let’s get started. So yeah, the marketing campaign is doing okay. We might want to improve the landing page. Not urgent though. Also, I think we should probably review the analytics dashboard sometime this week."

### Expected Behavior
- Filter out irrelevant content
- Extract weak/implicit tasks carefully

### Good Output Should:
- Identify:
  - Improve landing page (low priority / no deadline)
  - Review analytics dashboard (this week)
- Avoid extracting small talk
- Avoid over-interpreting vague language

---

## Case 3 — Failure-Prone / Hallucination Risk 🚨

### Input
"We discussed several ideas about improving user retention. Maybe onboarding could be better. Some people mentioned emails, but nothing is decided yet."

### Expected Behavior
- Recognize that NO clear actionable tasks exist

### Good Output Should:
- Either:
  - Return empty list
  - OR say "No clear action items identified"
- MUST NOT hallucinate tasks like:
  - "Improve onboarding"
  - "Send emails"

---

## Case 4 — Complex Multi-Speaker / Multi-Task 📊

### Input
"Okay, let’s align on next steps. Alice will redesign the dashboard UI by next Wednesday. Bob and Charlie will work together on database optimization, no strict deadline yet. Also, we need to hire a new backend engineer—HR team should start drafting the job description."

### Expected Behavior
- Handle multiple tasks and multiple assignees
- Keep structure clear

### Good Output Should:
- Include:
  - Alice → redesign dashboard UI → next Wednesday
  - Bob & Charlie → database optimization
  - HR team → draft job description
- Preserve multi-person assignments

---

## Case 5 — Long Context / Mixed Signal 📚

### Input
"Let’s go through updates. Sales numbers are up 10%, which is great. The customer feedback indicates issues with checkout speed. We should investigate that. Also, the mobile app crash reported last week still hasn’t been fixed—can someone take ownership? David, can you look into that by Thursday? Lastly, we might explore AI features in Q3."

### Expected Behavior
- Distinguish between:
  - metrics
  - insights
  - actual tasks

### Good Output Should:
- Include:
  - Investigate checkout speed issue
  - David → fix mobile app crash → Thursday
- Ignore:
  - "Sales numbers up"
  - "explore AI features in Q3" (too vague / strategic)

---

## Summary of Evaluation Coverage

| Case | Type |
|------|------|
| Case 1 | Normal |
| Case 2 | Edge (noisy input) |
| Case 3 | Hallucination risk |
| Case 4 | Multi-actor complexity |
| Case 5 | Long + mixed signal |

---

## Evaluation Criteria

When testing models, check:

1. **Precision** → No hallucinated tasks
2. **Recall** → All real tasks captured
3. **Structure** → Clear, readable action items
4. **Attribution** → Correct owner assignment
5. **Restraint** → Avoid extracting vague/non-actionable content
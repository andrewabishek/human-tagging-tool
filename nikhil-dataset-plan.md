# Plan: Leverage Nikhil's Dataset

## Source Files

- `Nikhil's dataset/TeamsConversationWithoutRAI.csv` (1,000 conversations)
- `Nikhil's dataset/data.csv` (200-row subset)

## What to Use

### SmartCard_Chat (9 conversations) — HIGH VALUE

- Realistic workplace scenarios: telemetry debugging, project delays, marketing launches, offsite planning, onboarding
- Adapt 5-8 as new conversations in our golden dataset format
- Need to: reformat flat text → message-level structure, assign HasTask/IsImportant, add metadata

### Decisions (15 conversations) — HIGH VALUE

- Team decision-making: roadmap, login features, security audit, testing strategy
- Good task delegation patterns ("I'll set up X", "I'll handle Y")
- Mine 5-10 for new scenarios

### new_similaropenitems (76) + simmilarOpenItems (7) — MEDIUM VALUE

- PR review workflows, lockbox access, budget approvals
- We already have Engineering coverage, but could add variety
- Cherry-pick a few unique patterns

## What NOT to Use

- GeneralSyntheticDatasets (~880): Philosophical chitchat (aliens, yoga, gaming) — not workplace
- Language_support (14): Non-English — out of scope
- Harmful_jailbreak (3): Adversarial test data

## Data Quality Notes

- 1 row has LLM chain-of-thought leaked into LLM_knowledge field
- ThreadId always null — no threading structure
- Users have placeholder surnames ("NA", "\_")
- Conversations are thread-level (concatenated), not message-level
- Labels use action/knowledge/commitment taxonomy, not HasTask/IsImportant

## Estimated Yield

- ~20-25 high-quality conversations adaptable to our format
- Would primarily add: product planning, cross-team decision-making, offsite coordination

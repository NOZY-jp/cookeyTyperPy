# Bug Fixes & Upgrade System Overhaul - Work Plan

## TL;DR

> **Quick Summary**: Fix upgrade parsing bug, add cookie number formatting with suffixes, update upgrade data from Cookie Clicker wiki, ensure consistent int display
>
> **Deliverables**:
> - Fixed `into_upgrade` function (support spaces & underscores)
> - `format_cookies()` utility with Cookie Clicker-style suffixes
> - Updated `cookeyTyperData.py` with tiered upgrades for Cursor, Grandma, Farm, Mine
> - Consistent int() formatting across all displays
> - Updated help text
>
> **Estimated Effort**: Large
> **Parallel Execution**: NO - sequential dependencies
> **Critical Path**: Fix bugs → Add formatting → Update upgrades → Test

---

## Context

### Original Request
ユーザーが発見したバグを修正：
1. アップグレード購入時の名前入力がスペースを含むと失敗する
2. クッキー数値のfloat表示（少数点以下が表示される）
3. 大数表示にsuffixがない（Cookie Clicker準拠）
4. アップグレード内容不足（Cookie Clicker wiki準拠）

### User Decisions
- **Upgrade Input**: Spaces preferred (underscores also allowed)
- **Cookie Display**: Always integer (no decimals)
- **Upgrade Scope**: ALL types for all facilities (tiered, grandma types, clicking upgrades)
- **Language**: Keep English names
- **Work Scope**: Full implementation (all bug fixes + upgrade data update)

---

## Work Objectives

### Core Objective
Fix identified bugs and expand upgrade system to match Cookie Clicker wiki, with proper number formatting for large numbers.

### Concrete Deliverables
- Fixed `into_upgrade()` in `cookeyTyperModels.py`
- New `format_cookies()` utility in `cookeyTyperUtils.py`
- Updated `cookeyTyperData.py` with comprehensive upgrade data
- All cookie displays use consistent formatting
- Updated help text

### Definition of Done
- [ ] Upgrade names with spaces parse correctly
- [ ] All cookie displays show int with proper suffixes
- [ ] At least Cursor/Keyboard, Grandma, Farm, Mine have full upgrade tiers
- [ ] All tests pass (basedpyright, integration tests)
- [ ] No float decimals in any cookie display

### Must Have
- Support both spaces and underscores in upgrade names
- Cookie Clicker-style suffixes (million, billion, etc.)
- Tiered upgrades for early facilities (Cursor, Grandma, Farm, Mine)
- Upgrade data matches wiki (names, prices, unlock conditions)

### Must NOT Have (Guardrails)
- Adding Milk, Achievements, Heavenly upgrades (per user request)
- Adding global kitten upgrades (out of scope - achievements system needed first)
- Changing game balance or mechanics (data-only changes)

---

## Verification Strategy (Mandatory)

### Test Decision
- **Infrastructure exists**: YES
- **User wants tests**: YES (Automated Verification Only)
- **Framework**: Custom test scripts + manual verification procedures

### Automated Verification (Agent-Executable)

**For Bug Fixes**:
```bash
# Test upgrade parsing with spaces
echo 'u buy reinforced index finger' | python -c "from cookeyTyperCore import CookeyTyper; import sys; engine=CookeyTyper(); engine.cookies=1000000; result=engine.handler.parse_command(sys.stdin.read().strip()); print('OK' if 'CommandUpgrade' in str(type(result.value)) else 'FAIL')"

# Test large number formatting
python -c "from cookeyTyperUtils import format_cookies; print(format_cookies(1000000000.123))"
# Expected: "1.000 million cookies"
```

**For Display Fixes**:
```bash
# Run game and check all displays
python -c "
from cookeyTyperCore import CookeyTyper
engine = CookeyTyper()
engine.cookies = 999999999.999
# Verify no float decimals in any display
" | grep -r "engine\.cookies" --include="*.py" | while read line; do python -c "print('$line' in $(python3 -c \"
from cookeyTyperCore import CookeyTyper
engine = CookeyTyper()
engine.cookies = 999999999.999
print('PASS' if 'float' not in '$line' else 'FAIL')
\")"
done
```

**For Upgrade Data**:
```bash
# Verify upgrade count
python -c "from cookeyTyperData import upgrades; print(f'Upgrades: {len(upgrades())}'); print('Cursor upgrades: [u for u in upgrades() if \"cursor\" in u[\"name\"].lower()])"

# Expected: At least 11 Cursor upgrades
```

**Evidence to Capture**:
- [ ] Terminal output from upgrade parsing tests
- [ ] Screenshot of large number formatting display
- [ ] Terminal output from upgrade count verification

---

## Execution Strategy

### Parallel Execution Waves
**Sequential execution** - tasks depend on each other:
1. Bug fixes first
2. Formatting utility
3. Upgrade data updates
4. Testing

```
Wave 1 (Bug Fixes):
├── Fix into_upgrade parsing
├── Create format_cookies utility
├── Apply format_cookies to displays
└── Fix int() inconsistencies

Wave 2 (Upgrade Data):
├── Add Cursor/Keyboard tiered upgrades (11 upgrades)
├── Add Grandma tiered upgrades (11 upgrades)
├── Add Farm tiered upgrades (11 upgrades)
├── Add Mine tiered upgrades (11 upgrades)
└── Add grandma type upgrades (4 upgrades per facility)

Critical Path: Wave 1 → Wave 2 → Final Test
```

---

## TODOs

- [ ] 1. Fix `into_upgrade` in `cookeyTyperModels.py`
  **What to do**:
  - Normalize user input by replacing spaces with underscores
  - Support both input formats for user convenience
  - Test: "reinforced index finger" should match "Reinforced index finger"

  **Must NOT do**:
  - Change config name format (keep English names with spaces)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Single function fix, straightforward logic
  - **Skills**: `[]`
    - No specialized skills needed for this simple fix

  **Parallelization**:
  - **Can Run In Parallel**: NO | Sequential
  - **Parallel Group**: Wave 1 | Sequential
  - **Blocks**: Tasks 2-9
  - **Blocked By**: None (can start immediately)

  **References** (CRITICAL - Be Exhaustive):

  > The executor has NO context from your interview. References are their ONLY guide.
  > Each reference must answer: "What should I look at and WHY?"

  **Pattern References** (existing code to follow):
  - `cookeyTyperModels.py:172-173` - Current into_upgrade implementation (fix this logic)

  **API/Type References** (contracts to implement against):
  - `cookeyTyperTypes.py:UpgradeTypes` - Enum of upgrade IDs
  - `cookeyTyperTypes.py:UpgradeConfig` - Config dict structure (name, price, target, etc.)

  **Test References** (testing patterns to follow):
  - No existing upgrade parsing tests - create new tests

  **Documentation References** (specs and requirements):
  - This work plan - Fix upgrade parsing to support spaces

  **External References** (libraries and frameworks):
  - User request: "Upgrade names contain spaces, user can't buy them"

  **WHY Each Reference Matters** (explain the relevance):
  - `cookeyTyperModels.py:172-173` - Shows the exact line causing the bug where config name spaces are converted but user input isn't

  **Acceptance Criteria**:

  > **CRITICAL: AGENT-EXECUTABLE VERIFICATION ONLY**
  >
  > - Acceptance = EXECUTION by the agent, not "user checks if it works"
  > - Every criterion MUST be verifiable by running a command or using a tool
  > - NO steps like "user opens browser", "user clicks", "user confirms"
  > - If you write "[placeholder]" - REPLACE IT with actual values based on task context

  **Automated Verification**:
  - [ ] Test parsing with space: `echo "u buy reinforced index finger" | run_game.py` → Should succeed
  - [ ] Test parsing with underscore: `echo "u buy reinforced_index_finger" | run_game.py` → Should succeed
  - [ ] Test invalid name: `echo "u buy invalid_upgrade" | run_game.py` → Should show error
  - [ ] Run basedpyright on cookeyTyperModels.py → 0 errors

  **Evidence to Capture**:
  - [ ] Terminal output of successful upgrade buy with space
  - [ ] basedpyright output (0 errors)

  **Commit**: YES
  - Message: `fix(upgrade): Support space-separated upgrade names in into_upgrade parser`
  - Files: `cookeyTyperModels.py`

- [ ] 2. Create `cookeyTyperUtils.py` with `format_cookies()` function
  **What to do**:
  - Create new utility file
  - Implement Cookie Clicker-style number formatting
  - Suffixes: thousand, million, billion, trillion, quadrillion, quintillion, sextillion, septillion, octillion, nonillion, decillion, undecillion, duodecillion, tredecillion, quattuordecillion, quindecillion
  - Format: "X.XXX {suffix} cookies" (e.g., "1.235 million cookies")

  **Must NOT do**:
  - Change how cookies are stored (keep as float internally)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Utility function creation, straightforward number formatting
  - **Skills**: `[]`
    - No specialized skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO | Sequential
  - **Parallel Group**: Wave 1 | Sequential
  - **Blocks**: Tasks 3-9
  - **Blocked By**: Task 1

  **References** (CRITICAL - Be Exhaustive):

  **Pattern References** (existing code to follow):
  - Python f-string formatting patterns in cookeyTyperHandler.py (e.g., `{facility.price:,}`)

  **API/Type References** (contracts to implement against):
  - Python `float` type for cookie values
  - Cookie Clicker formatting standards (from wiki)

  **Test References** (testing patterns to follow):
  - No existing format_cookies tests - create verification

  **Documentation References** (specs and requirements):
  - This work plan - Implement Cookie Clicker-style number formatting

  **External References** (libraries and frameworks):
  - Cookie Clicker wiki: Number format conventions (1.000 million cookies)
  - Python format specification for float to string conversion

  **WHY Each Reference Matters** (explain the relevance):
  - F-string patterns in cookeyTyperHandler.py - Show current formatting approach that needs replacement
  - Cookie Clicker wiki - Defines the exact suffix format used in the original game

  **Acceptance Criteria**:

  > **CRITICAL: AGENT-EXECUTABLE VERIFICATION ONLY**
  >
  > - Acceptance = EXECUTION by the agent, not "user checks if it works"
  > - Every criterion MUST be verifiable by running a command or using a tool
  > - NO steps like "user opens browser", "user clicks", "user confirms"
  > - If you write "[placeholder]" - REPLACE IT with actual values based on task context

  **Automated Verification**:
  - [ ] Test small number: `format_cookies(100)` → "100 cookies"
  - [ ] Test thousand: `format_cookies(1000)` → "1.000 thousand cookies"
  - [ ] Test million: `format_cookies(1000000)` → "1.000 million cookies"
  - [ ] Test billion: `format_cookies(1000000000)` → "1.000 billion cookies"
  - [ ] Test trillion: `format_cookies(1000000000000)` → "1.000 trillion cookies"
  - [ ] Test with decimals: `format_cookies(1234567.89)` → "1.235 million cookies"
  - [ ] Run basedpyright on cookeyTyperUtils.py → 0 errors

  **Evidence to Capture**:
  - [ ] Terminal output showing formatted numbers for various magnitudes
  - [ ] basedpyright output (0 errors)

  **Commit**: YES
  - Message: `feat(utils): Add format_cookies utility with Cookie Clicker-style suffixes`
  - Files: `cookeyTyperUtils.py`

- [ ] 3. Apply `format_cookies()` to all cookie displays in `cookeyTyperHandler.py`
  **What to do**:
  - Replace all `{self.engine.cookies}` with `format_cookies(self.engine.cookies)`
  - Replace all `{facility.next_cost()}` with `format_cookies(facility.next_cost())`
  - Replace all `{upgrade.price}` with `format_cookies(upgrade.price)`
  - Ensure all displays show int values (no float decimals)

  **Must NOT do**:
  - Change internal cookie storage (keep as float)
  - Change game logic (display-only change)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Display updates, straightforward find-and-replace
  - **Skills**: `[]`
    - No specialized skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO | Sequential
  - **Parallel Group**: Wave 1 | Sequential
  - **Blocks**: Tasks 4-9
  - **Blocked By**: Task 2

  **References** (CRITICAL - Be Exhaustive):

  **Pattern References** (existing code to follow):
  - `cookeyTyperHandler.py:272` - `{int(facility.next_cost()):,}` pattern
  - `cookeyTyperHandler.py:411` - `print(f"Current Cookies: {self.engine.cookies}")` (needs fix)
  - `cookeyTyperHandler.py:463, 486, 510` - upgrade price displays

  **API/Type References** (contracts to implement against):
  - `format_cookies()` function from Task 2
  - `engine.cookies` (float) → display (formatted string)
  - `facility.next_cost()` (float) → display (formatted string)
  - `upgrade.price` (int) → display (formatted string)

  **Test References** (testing patterns to follow):
  - No existing display format tests - visual verification

  **Documentation References** (specs and requirements):
  - This work plan - Apply consistent int formatting to all cookie displays

  **External References** (libraries and frameworks):
  - Cookie Clicker wiki: Display format conventions

  **WHY Each Reference Matters** (explain the relevance):
  - `cookeyTyperHandler.py:411` - Shows the exact line causing float display bug
  - `cookeyTyperHandler.py:272` - Shows pattern already using int() that should be followed

  **Acceptance Criteria**:

  > **CRITICAL: AGENT-EXECUTABLE VERIFICATION ONLY**
  >
  > - Acceptance = EXECUTION by the agent, not "user checks if it works"
  > - Every criterion MUST be verifiable by running a command or using a tool
  > - NO steps like "user opens browser", "user clicks", "user confirms"
  > - If you write "[placeholder]" - REPLACE IT with actual values based on task context

  **Automated Verification**:
  - [ ] Run: `grep -n "engine\.cookies" cookeyTyperHandler.py` → Find all lines
  - [ ] Verify each line uses `format_cookies()` instead of raw float
  - [ ] Run: `grep -n "next_cost" cookeyTyperHandler.py` → Verify cost displays
  - [ ] Run: `grep -n "upgrade\.price" cookeyTyperHandler.py` → Verify price displays
  - [ ] Run basedpyright on cookeyTyperHandler.py → 0 errors

  **Evidence to Capture**:
  - [ ] Grep output showing all cookie display locations updated
  - [ ] basedpyright output (0 errors)

  **Commit**: YES
  - Message: `fix(display): Apply format_cookies to all cookie displays`
  - Files: `cookeyTyperHandler.py`

- [ ] 4. Update `cookeyTyperData.py` - Add Cursor/Keyboard tiered upgrades
  **What to do**:
  - Replace existing 9 upgrades with full Cursor/Keyboard tiered upgrades (11 upgrades)
  - Use Cookie Clicker wiki data (names, prices, effects, unlock conditions)
  - Tier 1: Reinforced index finger (100, own 1 cursor, +2x)
  - Tier 2: Carpal tunnel prevention cream (500, own 1 cursor, +2x)
  - Tier 3: Ambidextrous (10000, own 10 cursors, +2x)
  - Tier 4: Thousand fingers (100000, own 25 cursors, +0.1 per non-cursor)
  - Tier 5-11: Million fingers through Nonillion fingers (matching wiki)

  **Must NOT do**:
  - Add Milk, Achievements, Heavenly upgrades (out of scope)
  - Add Grandma types or Synergy upgrades (separate task)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Data entry task, straightforward config addition
  - **Skills**: `[]`
    - No specialized skills needed for data entry

  **Parallelization**:
  - **Can Run In Parallel**: NO | Sequential
  - **Parallel Group**: Wave 2 (with Tasks 5-7) | Sequential
  - **Blocks**: Tasks 8-9
  - **Blocked By**: Task 3

  **References** (CRITICAL - Be Exhaustive):

  **Pattern References** (existing code to follow):
  - `cookeyTyperData.py:upgrades()` - Current upgrade config structure (follow this format)

  **API/Type References** (contracts to implement against):
  - `cookeyTyperTypes.py:UpgradeConfig` - Config dict keys: name, description, price, target, effect_type, value, unlock_facility, unlock_count
  - `cookeyTyperTypes.py:UpgradeTypes` - Enum values for cursor upgrades
  - `cookeyTyperTypes.py:EffectType` - ADD or MULTIPLIER

  **Test References** (testing patterns to follow):
  - No existing upgrade config tests - data validation

  **Documentation References** (specs and requirements):
  - Cookie Clicker wiki (downloaded tool output) - Cursor upgrade data
  - This work plan - Add tiered Cursor/Keyboard upgrades matching wiki

  **External References** (libraries and frameworks):
  - Cookie Clicker wiki: https://cookieclicker.wiki.gg/wiki/Upgrades
  - Tool output: `/home/nozy/.local/share/opencode/tool-output/tool_c1299ba6d001uESTtDMzM2jMHf` (lines 300-600 contain Cursor upgrade data)

  **WHY Each Reference Matters** (explain the relevance):
  - `cookeyTyperData.py:upgrades()` - Shows exact structure to follow for new upgrade entries
  - Cookie Clicker wiki tool output - Contains authoritative data for upgrade names, prices, and unlock conditions

  **Acceptance Criteria**:

  > **CRITICAL: AGENT-EXECUTABLE VERIFICATION ONLY**
  >
  > - Acceptance = EXECUTION by the agent, not "user checks if it works"
  > - Every criterion MUST be verifiable by running a command or using a tool
  > - NO steps like "user opens browser", "user clicks", "user confirms"
  > - If you write "[placeholder]" - REPLACE IT with actual values based on task context

  **Automated Verification**:
  - [ ] Run: `python -c "from cookeyTyperData import upgrades; print(f'Total: {len(upgrades())}')" | grep "Total: 11"`
  - [ ] Verify upgrade names match wiki (e.g., "Reinforced index finger", "Carpal tunnel prevention cream")
  - [ ] Verify unlock conditions (e.g., Tier 1: own 1 cursor, Tier 2: own 1 cursor, Tier 3: own 10 cursors)
  - [ ] Run basedpyright on cookeyTyperData.py → 0 errors

  **Evidence to Capture**:
  - [ ] Terminal output showing 11 Cursor upgrades
  - [ ] basedpyright output (0 errors)

  **Commit**: YES
  - Message: `feat(upgrades): Add full tiered Cursor/Keyboard upgrades from Cookie Clicker wiki`
  - Files: `cookeyTyperData.py`

- [ ] 5. Update `cookeyTyperData.py` - Add Grandma tiered upgrades
  **What to do**:
  - Add 11 Grandma tiered upgrades matching Cookie Clicker wiki
  - Tier 1: Forwards from grandma (1000, own 1 grandma, +2x)
  - Tier 2: Steel-plated rolling pins (5000, own 5 grandmas, +2x)
  - Tier 3-11: Through "Good manners" (matching wiki prices and unlock counts)

  **Must NOT do**:
  - Add Grandma type upgrades (separate task)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Data entry task, straightforward config addition
  - **Skills**: `[]`
    - No specialized skills needed for data entry

  **Parallelization**:
  - **Can Run In Parallel**: YES | With Task 4
  - **Parallel Group**: Wave 2 (with Task 4) | Sequential
  - **Blocks**: Tasks 8-9
  - **Blocked By**: Task 3

  **References** (CRITICAL - Be Exhaustive):

  **Pattern References** (existing code to follow):
  - `cookeyTyperData.py:upgrades()` - Upgrade config structure

  **API/Type References** (contracts to implement against):
  - `cookeyTyperTypes.py:FacilityTypes.GRANDMA` - Target for grandma upgrades
  - `cookeyTyperTypes.py:EffectType` - Upgrade effect type

  **Documentation References** (specs and requirements):
  - Cookie Clicker wiki - Grandma upgrade data (from tool output)
  - This work plan - Add tiered Grandma upgrades

  **External References** (libraries and frameworks):
  - Cookie Clicker wiki tool output - Grandma upgrade data

  **Acceptance Criteria**:

  > **CRITICAL: AGENT-EXECUTABLE VERIFICATION ONLY**
  >
  > - Acceptance = EXECUTION by the agent, not "user checks if it works"
  > - Every criterion MUST be verifiable by running a command or using a tool
  > - NO steps like "user opens browser", "user clicks", "user confirms"
  > - If you write "[placeholder]" - REPLACE IT with actual values based on task context

  **Automated Verification**:
  - [ ] Run: `python -c "from cookeyTyperData import upgrades; print([u['name'] for u in upgrades().values() if 'grandma' in u['name'].lower()])" | wc -l → Should output 11
  - [ ] Verify upgrade names (e.g., "Forwards from grandma", "Steel-plated rolling pins")
  - [ ] Run basedpyright on cookeyTyperData.py → 0 errors

  **Evidence to Capture**:
  - [ ] Terminal output showing 11 Grandma upgrades
  - [ ] basedpyright output (0 errors)

  **Commit**: YES
  - Message: `feat(upgrades): Add tiered Grandma upgrades from Cookie Clicker wiki`
  - Files: `cookeyTyperData.py`

- [ ] 6. Update `cookeyTyperData.py` - Add Farm tiered upgrades
  **What to do**:
  - Add 11 Farm tiered upgrades matching Cookie Clicker wiki
  - Tier 1: Cheap hoes (11000, own 1 farm, +2x)
  - Tier 2-11: Through "Self-driving tractors" (matching wiki)

  **Must NOT do**:
  - Add Grandma type upgrades or Synergies (separate task)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Data entry task, straightforward config addition
  - **Skills**: `[]`
    - No specialized skills needed for data entry

  **Parallelization**:
  - **Can Run In Parallel**: YES | With Tasks 4-5
  - **Parallel Group**: Wave 2 (with Tasks 4-5) | Sequential
  - **Blocks**: Tasks 8-9
  - **Blocked By**: Task 3

  **References** (CRITICAL - Be Exhaustive):

  **Pattern References** (existing code to follow):
  - `cookeyTyperData.py:upgrades()` - Upgrade config structure

  **API/Type References** (contracts to implement against):
  - `cookeyTyperTypes.py:FacilityTypes.FARM` - Target for farm upgrades

  **Documentation References** (specs and requirements):
  - Cookie Clicker wiki - Farm upgrade data (from tool output)

  **Acceptance Criteria**:

  > **CRITICAL: AGENT-EXECUTABLE VERIFICATION ONLY**
  >
  > - Acceptance = EXECUTION by the agent, not "user checks if it works"
  > - Every criterion MUST be verifiable by running a command or using a tool
  > - NO steps like "user opens browser", "user clicks", "user confirms"
  > - If you write "[placeholder]" - REPLACE IT with actual values based on task context

  **Automated Verification**:
  - [ ] Run: `python -c "from cookeyTyperData import upgrades; print([u['name'] for u in upgrades().values() if 'farm' in u['name'].lower()])" | wc -l → Should output 11
  - [ ] Verify upgrade names (e.g., "Cheap hoes", "Fertilizer")
  - [ ] Run basedpyright on cookeyTyperData.py → 0 errors

  **Evidence to Capture**:
  - [ ] Terminal output showing 11 Farm upgrades
  - [ ] basedpyright output (0 errors)

  **Commit**: YES
  - Message: `feat(upgrades): Add tiered Farm upgrades from Cookie Clicker wiki`
  - Files: `cookeyTyperData.py`

- [ ] 7. Update `cookeyTyperData.py` - Add Mine tiered upgrades
  **What to do**:
  - Add 11 Mine tiered upgrades matching Cookie Clicker wiki
  - Tier 1: Sugar gas (120000, own 1 mine, +2x)
  - Tier 2-11: Through "Mineshaft supports" (matching wiki)

  **Must NOT do**:
  - Add Grandma type upgrades or Synergies (separate task)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Data entry task, straightforward config addition
  - **Skills**: `[]`
    - No specialized skills needed for data entry

  **Parallelization**:
  - **Can Run In Parallel**: YES | With Tasks 4-6
  - **Parallel Group**: Wave 2 (with Tasks 4-6) | Sequential
  - **Blocks**: Tasks 8-9
  - **Blocked By**: Task 3

  **References** (CRITICAL - Be Exhaustive):

  **Pattern References** (existing code to follow):
  - `cookeyTyperData.py:upgrades()` - Upgrade config structure

  **API/Type References** (contracts to implement against):
  - `cookeyTyperTypes.py:FacilityTypes.MINE` - Target for mine upgrades

  **Documentation References** (specs and requirements):
  - Cookie Clicker wiki - Mine upgrade data (from tool output)

  **Acceptance Criteria**:

  > **CRITICAL: AGENT-EXECUTABLE VERIFICATION ONLY**
  >
  > - Acceptance = EXECUTION by the agent, not "user checks if it works"
  > - Every criterion MUST be verifiable by running a command or using a tool
  > - NO steps like "user opens browser", "user clicks", "user confirms"
  > - If you write "[placeholder]" - REPLACE IT with actual values based on task context

  **Automated Verification**:
  - [ ] Run: `python -c "from cookeyTyperData import upgrades; print([u['name'] for u in upgrades().values() if 'mine' in u['name'].lower()])" | wc -l → Should output 11
  - [ ] Verify upgrade names (e.g., "Sugar gas", "Megadrill")
  - [ ] Run basedpyright on cookeyTyperData.py → 0 errors

  **Evidence to Capture**:
  - [ ] Terminal output showing 11 Mine upgrades
  - [ ] basedpyright output (0 errors)

  **Commit**: YES
  - Message: `feat(upgrades): Add tiered Mine upgrades from Cookie Clicker wiki`
  - Files: `cookeyTyperData.py`

- [ ] 8. Update `cookeyTyperData.py` - Add Grandma type upgrades for Cursor, Grandma, Farm, Mine
  **What to do**:
  - Add 1 Grandma type upgrade per facility (4 total)
  - Cursor: "Worker grandmas" (own 1 cursor, 10 grandmas, +0.1 CpS per cursor)
  - Grandma: "Farmer grandmas" (own 1 farm, 10 grandmas, +0.1 CpS per farm)
  - Farm: "Miner grandmas" (own 1 mine, 10 grandmas, +0.1 CpS per mine)
  - Mine: "Factory grandmas" (own 1 factory, 10 grandmas, +0.1 CpS per factory)

  **Must NOT do**:
  - Add Synergy upgrades or Milk/Achievement effects (out of scope)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Data entry task, straightforward config addition
  - **Skills**: `[]`
    - No specialized skills needed for data entry

  **Parallelization**:
  - **Can Run In Parallel**: NO | Sequential
  - **Parallel Group**: Wave 2 (after Tasks 4-7) | Sequential
  - **Blocks**: Task 9
  - **Blocked By**: Tasks 4-7

  **References** (CRITICAL - Be Exhaustive):

  **Pattern References** (existing code to follow):
  - `cookeyTyperData.py:upgrades()` - Upgrade config structure

  **API/Type References** (contracts to implement against):
  - `cookeyTyperTypes.py:FacilityTypes` - Target facilities for grandma types
  - `cookeyTyperTypes.py:EffectType` - ADD type for grandma types

  **Documentation References** (specs and requirements):
  - Cookie Clicker wiki - Grandma type upgrade data (need to research specific names from wiki)

  **Acceptance Criteria**:

  > **CRITICAL: AGENT-EXECUTABLE VERIFICATION ONLY**
  >
  > - Acceptance = EXECUTION by the agent, not "user checks if it works"
  > - Every criterion MUST be verifiable by running a command or using a tool
  > - NO steps like "user opens browser", "user clicks", "user confirms"
  > - If you write "[placeholder]" - REPLACE IT with actual values based on task context

  **Automated Verification**:
  - [ ] Run: `python -c "from cookeyTyperData import upgrades; print([u['name'] for u in upgrades().values() if 'worker grandmas' in u['name'].lower() or 'farmer grandmas' in u['name'].lower()])" | wc -l → Should output 4
  - [ ] Verify unlock conditions (e.g., own 1 cursor + 10 grandmas for "Worker grandmas")
  - [ ] Run basedpyright on cookeyTyperData.py → 0 errors

  **Evidence to Capture**:
  - [ ] Terminal output showing 4 Grandma type upgrades
  - [ ] basedpyright output (0 errors)

  **Commit**: YES
  - Message: `feat(upgrades): Add Grandma type upgrades from Cookie Clicker wiki`
  - Files: `cookeyTyperData.py`

- [ ] 9. Update `cookeyTyperHandler.py` - Help text update
  **What to do**:
  - Document upgrade command format (spaces allowed, underscores also work)
  - List available upgrade categories (tiered, grandma types, clicking)
  - Update facility count in help text

  **Must NOT do**:
  - Add new command types (only documentation update)

  **Recommended Agent Profile**:
  > - **Category**: `quick`
    - Reason: Documentation update, straightforward text modification
  - **Skills**: `[]`
    - No specialized skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO | Sequential
  - **Parallel Group**: Wave 3 (after Tasks 1-8) | Sequential
  - **Blocks**: Testing
  - **Blocked By**: Tasks 1-8

  **References** (CRITICAL - Be Exhaustive):

  **Pattern References** (existing code to follow):
  - `cookeyTyperHandler.py:200-225` - Current help command implementation

  **Documentation References** (specs and requirements):
  - This work plan - Update help text with upgrade information

  **Acceptance Criteria**:

  > **CRITICAL: AGENT-EXECUTABLE VERIFICATION ONLY**
  >
  > - Acceptance = EXECUTION by the agent, not "user checks if it works"
  > - Every criterion MUST be verifiable by running a command or using a tool
  > - NO steps like "user opens browser", "user clicks", "user confirms"
  > - If you write "[placeholder]" - REPLACE IT with actual values based on task context

  **Automated Verification**:
  - [ ] Run: `echo "help" | python -c "from cookeyTyperCore import CookeyTyper; import sys; engine=CookeyTyper(); result=engine.handler.parse_command(sys.stdin.read().strip()); engine.handler.execute_command(result.value)"` | grep "upgrade" → Should show upgrade help
  - [ ] Verify help shows "upgrade (u, upg)" section
  - [ ] Run basedpyright on cookeyTyperHandler.py → 0 errors

  **Evidence to Capture**:
  - [ ] Terminal output of help command showing upgrade documentation
  - [ ] basedpyright output (0 errors)

  **Commit**: YES
  - Message: `docs(help): Update help text with upgrade command documentation`
  - Files: `cookeyTyperHandler.py`

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|--------|-------------|
| 1 | `fix(upgrade): Support space-separated upgrade names in into_upgrade parser` | `cookeyTyperModels.py` | `python -c "test_upgrade_parsing.py"` |
| 2 | `feat(utils): Add format_cookies utility with Cookie Clicker-style suffixes` | `cookeyTyperUtils.py` | `python -c "test_format_cookies.py"` |
| 3 | `fix(display): Apply format_cookies to all cookie displays` | `cookeyTyperHandler.py` | `grep -n "engine\.cookies" cookeyTyperHandler.py` |
| 4 | `feat(upgrades): Add tiered Cursor/Keyboard upgrades from Cookie Clicker wiki` | `cookeyTyperData.py` | `python -c "count_cursor_upgrades.py"` |
| 5 | `feat(upgrades): Add tiered Grandma upgrades from Cookie Clicker wiki` | `cookeyTyperData.py` | `python -c "count_grandma_upgrades.py"` |
| 6 | `feat(upgrades): Add tiered Farm upgrades from Cookie Clicker wiki` | `cookeyTyperData.py` | `python -c "count_farm_upgrades.py"` |
| 7 | `feat(upgrades): Add tiered Mine upgrades from Cookie Clicker wiki` | `cookeyTyperData.py` | `python -c "count_mine_upgrades.py"` |
| 8 | `feat(upgrades): Add Grandma type upgrades from Cookie Clicker wiki` | `cookeyTyperData.py` | `python -c "count_grandma_type_upgrades.py"` |
| 9 | `docs(help): Update help text with upgrade command documentation` | `cookeyTyperHandler.py` | `echo "help" | run_game.py` |

---

## Success Criteria

### Verification Commands
```bash
# Upgrade parsing test
echo "u buy reinforced index finger" | python main.py
# Expected: Purchase successful

# Number formatting test
python -c "from cookeyTyperUtils import format_cookies; print(format_cookies(1234567890.123))"
# Expected: "1.235 billion cookies"

# Upgrade count test
python -c "from cookeyTyperData import upgrades; print(f'Total upgrades: {len(upgrades())}')"
# Expected: At least 48 upgrades (11+11+11+11+4)

# Type check
basedpyright
# Expected: 0 errors
```

### Final Checklist
- [ ] All 9 TODOs completed
- [ ] All tests pass
- [ ] No float decimals in cookie displays
- [ ] Upgrade names with spaces work
- [ ] Cookie Clicker-style number formatting applied
- [ ] At least 4 facilities have full upgrade tiers
- [ ] Help text updated

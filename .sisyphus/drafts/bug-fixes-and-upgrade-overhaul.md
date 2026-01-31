# Draft: Bug Fixes & Upgrade System Overhaul

## User Decisions
- **Upgrade Input**: Spaces preferred (underscores also allowed for compatibility)
- **Cookie Display**: Always integer (no decimals)
- **Upgrade Scope**: ALL types for all facilities (tiered, grandma types, clicking upgrades)
- **Language**: Keep English names
- **Work Scope**: Full implementation (all bug fixes + upgrade data update)

---

## Issues Identified

### 1. Upgrade Name Parsing Bug
**Location**: `cookeyTyperModels.py:172-173` (`into_upgrade` function)

**Current Logic**:
```python
name = config["name"].lower().replace(" ", "_").replace("-", "_")
if name == arg.lower() or upgrade_type.name.lower() == arg.lower():
```

**Problem**:
- Config name: "Reinforced index finger" → converted to "reinforced_index_finger"
- User input: "reinforced index finger" (with space)
- Comparison: "reinforced_index_finger" != "reinforced index finger" → FAIL

**Solution**: Normalize user input to match config format (replace spaces with underscores)

### 2. Cookie Float Display Bug
**Locations**:
- `cookeyTyperHandler.py:411`: `print(f"Current Cookies: {self.engine.cookies}")`
- `cookeyTyperHandler.py:272, 296, 351, 361`: Using `int(facility.next_cost())`
- Inconsistent: Some use `int()`, some don't

**Solution**:
- Create `format_cookies()` function
- Apply to all cookie displays

### 3. Large Number Formatting
**Current**: Raw numbers or comma-separated (e.g., "1,234,567")
**Required**: Cookie Clicker style (e.g., "1.235 million cookies")

**Suffixes**: thousand, million, billion, trillion, quadrillion, quintillion, sextillion, septillion, octillion, nonillion, decillion, undecillion, duodecillion, tredecillion, quattuordecillion, quindecillion

### 4. Upgrade Content Mismatch
**Current**: 9 upgrades only
**Cookie Clicker Wiki**:
- ~300 building upgrades total
- 11 tiered upgrades per facility
- Grandma type upgrades per facility
- Clicking upgrades
- Golden cookie upgrades (may exclude as complex)
- Kitten upgrades (exclude per user decision)

---

## Implementation Plan

### Phase 1: Bug Fixes
1. Fix `into_upgrade` to normalize user input
2. Create `format_cookies()` function with suffixes
3. Apply `format_cookies()` to all cookie displays
4. Update all upgrade price displays

### Phase 2: Number Formatting Utility
Create in `cookeyTyperUtils.py`:
- `format_cookies(value: float) -> str`
- Support for all Cookie Clicker suffixes
- Format: "X.XXX {suffix} cookies"

### Phase 3: Upgrade Data Overhaul
Based on Cookie Clicker wiki data:

#### Facility Mappings
- Keyboard/Cursor → Cursor upgrades
- Grandma → Grandma upgrades
- Farm → Farm upgrades
- Mine → Mine upgrades
- Factory → Factory upgrades
- Bank → Bank upgrades
- Temple → Temple upgrades
- Wizard Tower → Wizard Tower upgrades
- etc.

#### Upgrade Categories
1. **Tiered Upgrades**: 11 per facility (doubles CpS)
2. **Grandma Types**: 1 per facility (e.g., "Worker grandmas", "Farmer grandmas")
3. **Clicking Upgrades**: ~10 for Cursor, others for specific facilities

### Phase 4: Update Help Text
- Add upgrade command documentation
- Explain name format (spaces allowed)
- List available upgrades format

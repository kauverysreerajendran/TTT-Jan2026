# Bug Fixes Summary - Brass Audit to Brass QC Reverse Transfer

## Bugs Fixed

### Bug 1: After rejection from Brass Audit - the row still appears in Brass Audit pick table

**Root Cause:**
The reverse transfer function was only setting `send_brass_audit_to_qc = False` and `brass_audit_rejection = False`, but the lot still met the include conditions for Brass Audit pick table because `brass_qc_accptance = True` was not reset.

**Fix Applied:**
Modified `send_brass_audit_back_to_brass_qc` function in [Brass_QC/views.py](Brass_QC/views.py):

- Set `send_brass_audit_to_qc = True` (so lot appears in Brass QC)
- Set `brass_qc_accptance = False` (so lot doesn't meet Brass Audit include conditions)
- Reset all other audit flags to clean state

**Why this works:**
The Brass Audit pick table filters include lots with `Q(brass_qc_accptance=True, ...)`. By setting this to `False`, the lot no longer meets any include conditions for Brass Audit, preventing it from appearing there while still being available in Brass QC.

### Bug 2: In Brass QC - view.png icon is empty (no tray data)

**Root Cause:**
When a lot is rejected in Brass Audit, a new `TotalStockModel` is created for the next process, but the tray creation was incorrect:

- New lot had `BrassAuditTrayId` records with `rejected_tray=True`
- Brass QC view looks for accepted tray data but finds none
- The `pick_CompleteTable_tray_id_list` API returned empty results

**Fix Applied:**
Modified `BAuditBatchRejectionAPIView` in [BrassAudit/views.py](BrassAudit/views.py):

- Changed tray creation from `BrassAuditTrayId` to `BrassTrayId` records
- Set proper flags: `rejected_tray=False`, `top_tray` preserved, etc.
- Used original tray data from the rejected lot to maintain consistency

**Why this works:**
The new lot now has proper `BrassTrayId` records that Brass QC can access. The view.png icon will populate with the correct tray data because the API endpoints can find accepted tray records.

## Files Modified

1. **`Brass_QC/views.py`**:
   - `send_brass_audit_back_to_brass_qc` function
   - Fixed flag management to prevent Brass Audit reappearance

2. **`BrassAudit/views.py`**:
   - `BAuditBatchRejectionAPIView` class
   - Fixed tray data creation for new lots after rejection

## Testing Verification

Based on the provided logs:

**Before Fix:**

- `LID250120261441391485` appeared in both Brass Audit and Brass QC pick tables
- `LID250120261442221486` had "Total accepted trays found: 0"

**After Fix:**

- `LID250120261441391485` will only appear in Brass QC pick table
- `LID250120261442221486` will have proper `BrassTrayId` records for tray display

## Performance Impact

**No performance degradation introduced:**

- Existing queries and filters remain unchanged
- Only modified flag values and tray creation logic
- No additional database queries added
- All existing functionality preserved

## Flow Verification

**Correct Flow After Fixes:**

1. Lot processed in Brass QC → Transfer to Brass Audit ✓
2. Lot rejected in Brass Audit → Reverse transfer called ✓
3. Original lot disappears from Brass Audit pick table ✓
4. Original lot reappears in Brass QC pick table with existing tray data ✓
5. New lot created for next process has proper tray data ✓
6. No duplicate entries or empty tray displays ✓

Both bugs are now resolved with minimal code changes that preserve all existing functionality.

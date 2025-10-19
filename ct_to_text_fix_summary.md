# CT to Text Workflow - Command Injection Fix

## Issue Summary

The CT to Text Analysis workflow was failing during the "Check Blacklist" step with command injection errors:

```
/home/runner/work/_temp/a95fd329-3202-455b-bdf7-152a833f1f96.sh: line 2: 000620417: command not found
/home/runner/work/_temp/a95fd329-3202-455b-bdf7-152a833f1f96.sh: line 2: json: command not found
/home/runner/work/_temp/a95fd329-3202-455b-bdf7-152a833f1f96.sh: line 4: system_create_dtsi:: command not found
/home/runner/work/_temp/a95fd329-3202-455b-bdf7-152a833f1f96.sh: line 5: system_modified_dtsi:: command not found
...
```

## Root Cause

The issue occurred when GitHub Actions interpolated `${{ steps.fetch_release.outputs.release_body }}` into bash scripts. When the release body contained JSON data with special characters (from MorphoSource API releases), GitHub Actions variable expansion caused bash to interpret parts of the JSON as commands instead of data.

The problematic pattern was:
```yaml
run: |
  printf '%s\n' "${{ steps.fetch_release.outputs.release_body }}" > temp_release.txt
```

Even using `printf '%s\n'` was not sufficient because the GitHub Actions interpolation happened **before** bash received the script, causing JSON fields like `"id": "000620417"` to be interpreted as bash commands.

## Solution

The fix writes the release body to a file immediately after fetching it, **before** any GitHub Actions variable interpolation can cause issues:

### Step 4: Fetch Latest Release (FIXED)
```yaml
- name: Fetch latest release
  id: fetch_release
  env:
    GH_TOKEN: ${{ github.token }}
  run: |
    release=$(gh api -H "Accept: application/vnd.github+json" /repos/$GITHUB_REPOSITORY/releases/latest)
    echo "release_tag=$(echo $release | jq -r .tag_name)" >> "$GITHUB_OUTPUT"
    
    # Write release body directly to file to avoid command injection
    echo "$release" | jq -r .body > release_body.txt
```

### Subsequent Steps (FIXED)
All steps that need the release body now read from `release_body.txt`:

**Step 8: Check for record data**
```yaml
- name: Check for record data
  run: |
    # Use the release_body.txt file created in step 4
    if grep -q "^New Record #[0-9]" release_body.txt; then
      echo "has_records=true" >> "$GITHUB_OUTPUT"
    elif grep -q "### Full API JSON for latest record" release_body.txt; then
      echo "has_records=true" >> "$GITHUB_OUTPUT"
    fi
```

**Step 9: Check Blacklist**
```yaml
- name: Check Blacklist
  run: |
    # Use the release_body.txt file created in step 4
    while IFS= read -r line || [[ -n "$line" ]]; do
      [[ $line =~ ^#.*$ || -z $line ]] && continue
      if grep -F -x "$line" release_body.txt; then
        echo "is_blacklisted=true" >> "$GITHUB_OUTPUT"
        exit 0
      fi
    done < .github/blacklist.txt
```

**Step 11: Run CT to Text**
```yaml
- name: Run CT to Text
  run: |
    # Use the release_body.txt file created in step 4
    python .github/scripts/ct_to_text.py release_body.txt > ct_output.txt
```

## Why This Works

1. **No Variable Interpolation**: The release body is written to a file using `jq -r .body`, which happens within the bash script context, not through GitHub Actions variable expansion.

2. **File-Based Processing**: All subsequent steps read from `release_body.txt`, so the JSON content is never passed through GitHub Actions variable interpolation.

3. **Bash Safety**: Bash never sees the JSON content as part of the script itself—it's just file data being read by commands like `grep` and `cat`.

## Changes Made

### Files Modified
1. `.github/workflows/ct_to_text.yml` - Fixed 4 steps:
   - Step 4: Fetch latest release - now creates `release_body.txt`
   - Step 8: Check for record data - reads from `release_body.txt`
   - Step 9: Check Blacklist - reads from `release_body.txt`
   - Step 11: Run CT to Text - reads from `release_body.txt`

2. `docs/ct_to_text_api_support.md` - Updated documentation to reflect new approach

### Removed
- Removed `release_body` output from `fetch_release` step
- Removed all `printf '%s\n' "${{ steps.fetch_release.outputs.release_body }}"` commands
- Removed temporary file creation in steps 8, 9, and 11

## Testing

The fix has been verified with:

1. **YAML Validation**: Workflow YAML syntax is valid
2. **Command Injection Prevention**: JSON fields no longer cause "command not found" errors
3. **Functionality Preservation**: All grep operations and file processing work correctly
4. **API Release Compatibility**: MorphoSource API releases with JSON are properly handled

## Backward Compatibility

This change is fully backward compatible:
- Traditional "New Record #" format releases still work
- API releases with JSON data now work correctly
- No changes to the Python script or blacklist functionality
- All conditional logic remains the same

## Security Impact

This fix **resolves a high-priority security issue** by preventing command injection through crafted release bodies. The file-based approach ensures that no user-controlled data (release content) is ever interpreted as shell commands.

## Related Documentation

- `docs/ct_to_text_api_support.md` - API release format and processing
- `.github/workflows/ct_to_text.yml` - The workflow file itself
- `.github/scripts/ct_to_text.py` - Python script that parses releases

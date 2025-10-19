# Data Compression Strategy

## Problem

The repository was experiencing slow GitHub Actions checkout times due to the large size of the `data/` directory:

- **Size**: ~9.9 GB
- **Directories**: 255 timestamped data directories
- **Large files**: Each directory contains `morphosource_data_complete.json` files (~63 MB each)
- **Impact**: Checkout operations in GitHub Actions were taking several minutes, causing:
  - Remote: Enumerating 481,938 objects
  - Resolving 466,189 deltas
  - Downloading ~179 MB over the network

## Solution

A hybrid data compression strategy that:
1. Keeps the most recent data directories uncompressed
2. Compresses older historical data into an archive
3. Maintains workflow compatibility
4. Significantly reduces repository size

### Why Hybrid Instead of Full Compression?

Daily and monthly workflows need access to recent data directories for comparison and analysis. By keeping the most recent directories (default: 3) uncompressed:
- ✅ Workflows continue to function without modification
- ✅ Checkout times are drastically reduced
- ✅ Historical data is preserved and accessible when needed
- ✅ Repository size is optimized

## Implementation

### Workflow: `compress-data.yml`

**Location**: `.github/workflows/compress-data.yml`

**Trigger**: Manual (workflow_dispatch)

**Inputs**:
- `compression_level`: 1-9 (default: 6)
- `keep_recent`: Number of recent directories to keep uncompressed (default: 3)

**Actions**:
1. Sets up Git LFS for handling large files
2. Identifies all data directories sorted by timestamp
3. Keeps N most recent directories uncompressed
4. Moves older directories to a temporary location
5. Creates compressed archive: `data_archive.tar.gz`
6. Removes archived directories from git tracking
7. Creates extraction script and documentation
8. Commits and pushes changes (with Git LFS handling the large archive)

### Generated Files

When run, the workflow creates:

1. **`data_archive.tar.gz`**: Compressed archive of historical data (managed by Git LFS)
2. **`extract-data-archive.sh`**: Script to extract archived data locally
3. **`DATA_ARCHIVE_README.md`**: Documentation for the archive
4. **Updated `.gitignore`**: Comments explaining the archive strategy
5. **`.gitattributes`**: Configures Git LFS to track the archive file

## Usage

### Running the Compression Workflow

1. Go to the **Actions** tab in GitHub
2. Select **"Compress Data Directory"** workflow
3. Click **"Run workflow"**
4. Optionally configure:
   - Compression level (higher = better compression, slower)
   - Number of recent directories to keep

### Extracting Historical Data Locally

If you need to work with historical data:

```bash
# Run the extraction script
./extract-data-archive.sh

# Or manually extract
tar -xzf data_archive.tar.gz -C /tmp/
mv /tmp/old_data/* data/
```

### For Workflow Maintainers

Most existing workflows don't need any changes - they'll continue to work with the recent data that remains uncompressed.

If a workflow needs historical data, add this step:

```yaml
- name: Extract historical data if needed
  if: hashFiles('data_archive.tar.gz') != ''
  run: |
    echo "Extracting historical data..."
    tar -xzf data_archive.tar.gz -C /tmp/
    mv /tmp/old_data/* data/ 2>/dev/null || true
```

## Expected Benefits

### Before Compression
- Repository size: ~9.9 GB
- Checkout time: Several minutes
- Objects to enumerate: 481,938
- Network transfer: ~179 MB

### After Compression
- Repository size: ~1-2 GB (estimated, depends on compression)
- Checkout time: < 1 minute (estimated)
- Objects to enumerate: Significantly reduced
- Network transfer: Much smaller

The exact savings depend on:
- Number of directories archived
- Compression level chosen
- Data compressibility

## Maintenance

### When to Re-run Compression

Run the compression workflow when:
- Repository size grows beyond acceptable limits
- Many new data directories have been added
- You want to adjust the number of recent directories kept

### Recommended Schedule

- **Initial run**: Compress all historical data, keep 3 most recent
- **Ongoing**: Run monthly or when 10+ new directories accumulate
- **Before major work**: If doing extensive local development

## Trade-offs

### Advantages
- ✅ Dramatically faster GitHub Actions checkout
- ✅ Reduced repository size
- ✅ Lower bandwidth usage
- ✅ Maintains workflow compatibility
- ✅ Historical data preserved

### Considerations
- ⚠️ Historical data requires extraction for local access
- ⚠️ One-time compression/push operation takes time
- ⚠️ Archive grows over time (may need periodic re-compression)

## Technical Details

### Compression Algorithm
- Uses gzip compression via tar
- Configurable compression level (1-9)
- Level 6 (default) provides good balance of speed and size

### Directory Selection
- Only timestamped directories (format: `YYYY-MM-DD_HH-MM-SS`) are considered for compression
- Special directories (e.g., `parquet/`, `reactions/`) are always kept uncompressed
- Timestamped directories sorted by name
- Most recent N timestamped directories kept uncompressed
- Older timestamped directories moved to archive

### Git Operations
- Archived directories removed from git tracking
- Archive file added to repository via Git LFS (handles files >100 MB)
- Atomic commit with descriptive message

### Git LFS (Large File Storage)
- The archive file is tracked using Git LFS to handle files exceeding GitHub's 100 MB limit
- Git LFS stores large files outside the main repository
- The workflow automatically configures and uses Git LFS
- `.gitattributes` file configures LFS tracking for `data_archive.tar.gz`

## Troubleshooting

### "Not enough directories to compress"
The workflow requires more than `keep_recent` directories to run. Add more data or reduce the `keep_recent` parameter.

### "Push failed"
The workflow includes retry logic. If it fails, check for:
- Concurrent pushes from other workflows
- Network issues
- Permission problems
- Git LFS quota (GitHub provides 1 GB free storage per month)

### "Extraction failed"
Ensure `data_archive.tar.gz` exists and is not corrupted:
```bash
# Verify archive integrity
tar -tzf data_archive.tar.gz | head
```

## Related Files

- Workflow: `.github/workflows/compress-data.yml`
- Archive: `data_archive.tar.gz`
- Extraction script: `extract-data-archive.sh`
- Archive docs: `DATA_ARCHIVE_README.md`
- This document: `docs/data-compression-strategy.md`

## See Also

- [GitHub Actions workflow optimization](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsuses)
- [actions/checkout documentation](https://github.com/actions/checkout)

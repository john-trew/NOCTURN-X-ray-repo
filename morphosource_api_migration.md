# MorphoSource API Migration

## Overview

This document describes the migration from web scraping to using the MorphoSource JSON API for data collection.

## Background

Previously, the repository used web scraping with BeautifulSoup to extract data from MorphoSource's HTML pages. This approach had several issues:

1. **Bot Detection**: Frequent requests triggered bot detection mechanisms
2. **Fragility**: HTML structure changes could break the scraper
3. **Performance**: Parsing HTML is slower than consuming structured JSON
4. **Rate Limiting**: Web scraping is more likely to hit rate limits

## Solution

MorphoSource uses Blacklight/Solr, which provides JSON API endpoints. By migrating to the API:

1. **Reliability**: Official API endpoints are more stable
2. **Performance**: JSON parsing is faster than HTML parsing
3. **Bot Detection**: API requests are less likely to trigger bot detection
4. **Structured Data**: Consistent, documented data format

## API Client

### Module: `morphosource_api.py`

A new Python module provides a clean interface to the MorphoSource API:

```python
from morphosource_api import MorphoSourceAPI

# Create API client
api = MorphoSourceAPI()

# Get total count of records
count = api.get_total_count(query="X-Ray Computed Tomography")

# Get latest records
records = api.get_latest_records(n=10, query="X-Ray Computed Tomography")

# Search with pagination
result = api.search_media(
    query="X-Ray Computed Tomography",
    sort="system_create_dtsi desc",
    page=1,
    per_page=100
)

# Iterate all records
for record in api.iterate_all_records(query="X-Ray Computed Tomography"):
    print(record['title'])
```

### Key Features

- **Retry Logic**: Automatic retries with exponential backoff
- **Rate Limiting**: Built-in delays to respect server limits
- **Error Handling**: Graceful handling of temporary outages
- **Normalization**: Converts API responses to match previous scraping format
- **Backward Compatible**: Existing code continues to work with minimal changes

## Updated Scripts

### 1. `scrape_morphosource.py`

**Before**: Used BeautifulSoup to parse HTML and extract record counts and details.

**After**: Uses `MorphoSourceAPI.get_total_count()` and `get_latest_records()`.

**Key Changes**:
- Removed BeautifulSoup dependency
- Removed HTML parsing logic
- Removed manual retry/backoff logic (now in API client)
- Maintained same output format for compatibility

### 2. `daily.py`

**Before**: Scraped pages iteratively using BeautifulSoup.

**After**: Uses `MorphoSourceAPI.search_media()` with pagination.

**Key Changes**:
- `DailyMorphoSourceExtractor` no longer needs base URL
- `get_all_records()` uses API pagination
- Removed `parse_record()` method (normalization in API client)
- Maintains same data format

### 3. `monthly.py`

**Before**: Scraped all pages to collect complete dataset.

**After**: Uses `MorphoSourceAPI.search_media()` with pagination.

**Key Changes**:
- `MonthlyMorphoSourceCollector` no longer needs base URL
- `collect_all_records()` uses API pagination
- Removed `parse_record()` method (normalization in API client)
- Maintains same data format

### 4. `check_modified_morphosource.py`

**Before**: Scraped sorted-by-modification page to find latest modified record.

**After**: Uses `MorphoSourceAPI.get_latest_modified_record()`.

**Key Changes**:
- Uses dedicated method for modified records
- Removed BeautifulSoup dependency
- Cleaner, more maintainable code

## API Endpoints

### Search Endpoint

```
GET https://www.morphosource.org/catalog.json
```

**Parameters**:
- `q`: Search query (e.g., "X-Ray Computed Tomography")
- `search_field`: Field to search (default: "all_fields")
- `sort`: Sort field and direction (e.g., "system_create_dtsi desc")
- `page`: Page number (1-indexed)
- `per_page`: Results per page (max 100)

**Response Structure**:
```json
{
  "data": [
    {
      "id": "000123456",
      "title_sms": ["Specimen Title"],
      "taxonomy_class_sms": ["Mammalia"],
      "element_sms": ["skull"],
      "publication_status_sms": ["published"],
      ...
    }
  ],
  "meta": {
    "pages": {
      "total_count": 108000,
      "current_page": 1,
      "limit_value": 20,
      "total_pages": 5400
    }
  }
}
```

## Testing

Unit tests are provided in `test_morphosource_api.py`:

```bash
cd .github/scripts
python3 test_morphosource_api.py
```

Tests cover:
- API client initialization
- Response parsing
- Record normalization
- Error handling
- Backward compatibility

## Migration Benefits

1. **Reduced Bot Detection**: API requests use proper User-Agent and respect rate limits
2. **Better Performance**: JSON parsing is faster than HTML parsing
3. **More Reliable**: Official API is less likely to change than HTML structure
4. **Cleaner Code**: Less complex parsing logic
5. **Better Error Handling**: Standardized error responses from API
6. **Maintainability**: Single API client module instead of scattered scraping code

## Backward Compatibility

The API client's `normalize_record()` method ensures that API responses are converted to match the format previously used by web scraping. This means:

- Existing workflows continue to work without modification
- Data files maintain the same structure
- Release notes and reporting remain unchanged

## Rate Limiting

The API client includes several rate limiting features:

1. **Per-Request Delays**: 2-second delay between paginated requests
2. **Retry Backoff**: Exponential backoff on failures (5, 10, 20 seconds)
3. **Connection Pooling**: Limited to 1 concurrent connection
4. **Respect Server Headers**: Honors `Retry-After` headers

## Future Enhancements

Potential improvements for the API client:

1. **Caching**: Cache API responses to reduce duplicate requests
2. **Batch Operations**: Optimize bulk data collection
3. **WebSocket Support**: Real-time updates if API supports it
4. **Metrics**: Track API usage and performance
5. **Configuration**: External config file for API settings

## Troubleshooting

### API Returns Empty Results

Check if:
- Query syntax is correct
- Sort field is valid
- Page number is within range

### Rate Limiting Issues

If rate limited:
- Increase delay between requests
- Use smaller `per_page` values
- Check API documentation for limits

### Server Errors

If API returns 500 errors:
- Check MorphoSource status
- Retry with exponential backoff
- Fall back to previous data if available

## Resources

- [MorphoSource Website](https://www.morphosource.org)
- [Blacklight Documentation](https://github.com/projectblacklight/blacklight)
- [Solr API Documentation](https://solr.apache.org/guide/)

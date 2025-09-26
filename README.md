# vidIQ Python API

[![PyPI version](https://badge.fury.io/py/vidiq-api.svg)](https://badge.fury.io/py/vidiq-api)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A clean, simple Python wrapper for the vidIQ YouTube keyword analysis API. Perfect for integrating YouTube SEO research into your Python projects.

## 🚀 Features

- **Simple API**: Just one class, easy to use
- **Case Insensitive**: Works with any keyword capitalization
- **Rate Limited**: Built-in delays to respect API limits
- **Error Handling**: Comprehensive error messages
- **Type Hints**: Full type annotations for better IDE support
- **CSV Export**: Export keyword research data to CSV files
- **Multiple Data Types**: Related keywords, matching keywords, and questions
- **No Dependencies**: Only requires `requests`

## 📦 Installation

```bash
pip install vidiq-api
```

## 🔑 Getting Your API Token

1. Install the vidIQ browser extension
2. Open browser developer tools (F12)
3. Go to Network tab
4. Visit any YouTube page
5. Look for requests to `api.vidiq.com`
6. Copy the `Authorization` header value (starts with "Bearer")

## 🎯 Quick Start

```python
from vidiq_api import VidiqAPI

# Initialize with your token
api = VidiqAPI("your_vidiq_token_here")

# Analyze a keyword
result = api.analyze_keyword("youtube SEO")

print(f"Keyword: {result['keyword']}")
print(f"Monthly Searches: {result['data']['estimated_monthly_search']:,}")
print(f"Competition: {result['data']['competition']}")
print(f"Difficulty: {result['levels']['overall_level']}")
```

**Output:**
```
Keyword: youtube SEO
Monthly Searches: 191,875
Competition: 54.5
Difficulty: High
```

## 📊 Response Format

```python
{
    'keyword': 'youtube SEO',
    'timestamp': '2024-01-15 14:30:00',
    'data': {
        'volume': 78.86,
        'competition': 54.5,
        'estimated_monthly_search': 191875.0,
        'overall': 65.52
    },
    'levels': {
        'volume_level': 'High',
        'competition_level': 'Medium',
        'overall_level': 'High'
    }
}
```

## 🔄 Batch Processing

```python
# Analyze multiple keywords
keywords = ["youtube SEO", "video marketing", "content creation"]
results = api.analyze_multiple_keywords(keywords, delay=1.0)

for keyword, data in results.items():
    if 'error' not in data:
        print(f"{keyword}: {data['data']['estimated_monthly_search']:,} searches/month")
```

## 🛠️ Advanced Usage

### Environment Variables
```bash
export VIDIQ_TOKEN="your_token_here"
python -c "from vidiq_api import VidiqAPI; print(VidiqAPI().analyze_keyword('youtube SEO'))"
```

### Custom Rate Limiting
```python
# Slower requests for heavy usage
result = api.analyze_keyword("youtube SEO", delay=2.0)

# Batch with custom delays
results = api.analyze_multiple_keywords(keywords, delay=1.5)
```

### Error Handling
```python
try:
    result = api.analyze_keyword("youtube SEO")
    print(f"Success: {result['data']['volume']}")
except Exception as e:
    print(f"Error: {e}")
    # Handle rate limits, invalid tokens, etc.
```

## 📊 CSV Export Features

Export comprehensive keyword research data to CSV files for analysis in Excel, Google Sheets, or other tools.

### Combined CSV Export
Export all keyword types (related, matching, questions) to a single CSV file:

```python
from vidiq_api import VidiqAPI

api = VidiqAPI("your_token")

# Export to default filename (keyword_keywords.csv)
csv_file = api.export_to_csv("youtube SEO", limit=50)
print(f"Exported to: {csv_file}")

# Export to custom filename
csv_file = api.export_to_csv("video marketing", "my_keywords.csv", limit=100)
```

### Separate CSV Files
Export each keyword type to separate CSV files:

```python
# Export to separate files
file_paths = api.export_separate_csvs("content creation", output_dir="exports", limit=50)

print("Exported files:")
for data_type, file_path in file_paths.items():
    print(f"  {data_type}: {file_path}")
```

### CSV Format
The exported CSV files contain the following columns:

| Column | Description |
|--------|-------------|
| `keyword` | The keyword text |
| `type` | Type of keyword (related, matching, question) |
| `score` | Relevance/quality score |
| `volume` | Search volume estimate |
| `competition` | Competition level |
| `source_keyword` | Original search keyword |
| `timestamp` | When the data was collected |

### Complete Workflow with CSV
```python
def complete_keyword_research(keyword):
    api = VidiqAPI("your_token")
    
    # Get all keyword data
    print(f"Researching: {keyword}")
    
    # Export combined CSV
    combined_file = api.export_to_csv(keyword, limit=100)
    
    # Export separate CSVs for detailed analysis
    separate_files = api.export_separate_csvs(keyword, "detailed_exports", limit=200)
    
    print(f"Combined export: {combined_file}")
    print(f"Detailed exports: {separate_files}")
    
    return combined_file, separate_files

# Use the function
combined, separate = complete_keyword_research("youtube automation")
```

## 🎮 Command Line Usage

```bash
# Set your token
export VIDIQ_TOKEN="your_token_here"

# Analyze keywords
python -m vidiq_api "youtube SEO"
python -m vidiq_api "video marketing"
```

## 🔧 Integration Examples

### Web Scraping Integration
```python
import requests
from vidiq_api import VidiqAPI

def analyze_scraped_keywords(keywords):
    api = VidiqAPI("your_token")
    results = {}
    
    for keyword in keywords:
        try:
            result = api.analyze_keyword(keyword)
            results[keyword] = {
                'volume': result['data']['estimated_monthly_search'],
                'difficulty': result['levels']['overall_level']
            }
        except Exception as e:
            results[keyword] = {'error': str(e)}
    
    return results
```

### Content Strategy
```python
def find_easy_keywords(keywords):
    api = VidiqAPI("your_token")
    easy_keywords = []
    
    for keyword in keywords:
        try:
            result = api.analyze_keyword(keyword)
            if result['levels']['overall_level'] in ['Very Low', 'Low']:
                easy_keywords.append({
                    'keyword': keyword,
                    'searches': result['data']['estimated_monthly_search'],
                    'competition': result['data']['competition']
                })
        except:
            continue
    
    return sorted(easy_keywords, key=lambda x: x['searches'], reverse=True)
```

## 📋 API Reference

### `VidiqAPI(auth_token: str)`
Initialize the API client.

**Parameters:**
- `auth_token` (str): Your vidIQ authorization token

### `analyze_keyword(keyword: str, delay: float = 1.0) -> Dict`
Analyze a single keyword.

**Parameters:**
- `keyword` (str): The keyword to analyze
- `delay` (float): Delay in seconds before making the request

**Returns:**
- `Dict`: Keyword analysis data

**Raises:**
- `ValueError`: If keyword is empty
- `Exception`: If API call fails

### `analyze_multiple_keywords(keywords: List[str], delay: float = 1.0) -> Dict`
Analyze multiple keywords with automatic error handling.

**Parameters:**
- `keywords` (List[str]): List of keywords to analyze
- `delay` (float): Delay between requests

**Returns:**
- `Dict`: Results for each keyword

### `get_related_keywords(keyword: str, min_related_score: int = 0, delay: float = 1.0) -> Dict`
Get related keywords for a given keyword.

**Parameters:**
- `keyword` (str): The keyword to find related terms for
- `min_related_score` (int): Minimum score for related keywords
- `delay` (float): Delay between requests

**Returns:**
- `Dict`: Related keywords data

### `get_matching_keywords(keyword: str, limit: int = 300, delay: float = 1.0) -> Dict`
Get matching keywords (permutations) for a given keyword.

**Parameters:**
- `keyword` (str): The keyword to find matches for
- `limit` (int): Maximum number of results to return
- `delay` (float): Delay between requests

**Returns:**
- `Dict`: Matching keywords data

### `get_questions(keyword: str, limit: int = 300, delay: float = 1.0) -> Dict`
Get question-based keywords for a given keyword.

**Parameters:**
- `keyword` (str): The keyword to find questions for
- `limit` (int): Maximum number of results to return
- `delay` (float): Delay between requests

**Returns:**
- `Dict`: Question keywords data

### `export_to_csv(keyword: str, output_file: str = None, limit: int = 300, delay: float = 1.0) -> str`
Export all keyword research data to a single CSV file.

**Parameters:**
- `keyword` (str): The keyword to research
- `output_file` (str, optional): Path to output CSV file
- `limit` (int): Maximum number of results per category
- `delay` (float): Delay between API requests

**Returns:**
- `str`: Path to the created CSV file

### `export_separate_csvs(keyword: str, output_dir: str = ".", limit: int = 300, delay: float = 1.0) -> Dict[str, str]`
Export keyword research data to separate CSV files for each type.

**Parameters:**
- `keyword` (str): The keyword to research
- `output_dir` (str): Directory to save CSV files
- `limit` (int): Maximum number of results per category
- `delay` (float): Delay between API requests

**Returns:**
- `Dict[str, str]`: Dictionary with file paths for each exported CSV type

## ⚠️ Rate Limiting

The API includes built-in rate limiting to respect vidIQ's servers:

- Default delay: 1 second between requests
- Configurable delays for different use cases
- Automatic error handling for rate limit responses

For heavy usage (100+ keywords), consider:
- Increasing delay to 2-3 seconds
- Processing in smaller batches
- Using multiple API tokens

## 🐛 Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `Invalid token` | Wrong/expired auth token | Get fresh token from browser |
| `No data found` | Keyword not in database | Try related keywords |
| `Rate limit` | Too many requests | Increase delay parameter |
| `Network error` | Connection issues | Check internet connection |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚡ Performance Tips

- **Batch Processing**: Use `analyze_multiple_keywords()` for multiple keywords
- **Caching**: Cache results to avoid repeated API calls
- **Rate Limiting**: Respect the API limits with appropriate delays
- **Error Handling**: Always wrap API calls in try-catch blocks

## 🔗 Links

- [PyPI Package](https://pypi.org/project/vidiq-api/)
- [GitHub Repository](https://github.com/yourusername/vidiq-python-api)
- [Issue Tracker](https://github.com/yourusername/vidiq-python-api/issues)
- [vidIQ Website](https://vidiq.com/)

## 📈 Changelog

### v1.1.0
- **NEW**: CSV export functionality
- **NEW**: Related keywords API (`get_related_keywords()`)
- **NEW**: Matching keywords API (`get_matching_keywords()`)
- **NEW**: Questions API (`get_questions()`)
- **NEW**: Combined CSV export (`export_to_csv()`)
- **NEW**: Separate CSV exports (`export_separate_csvs()`)
- Enhanced example usage with CSV workflows
- Comprehensive CSV format documentation

### v1.0.0
- Initial release
- Basic keyword analysis
- Batch processing
- Command line interface
- Comprehensive error handling
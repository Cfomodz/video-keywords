#!/usr/bin/env python3
"""
vidIQ API Python Wrapper
Simple Python script for analyzing YouTube keywords using vidIQ API

Usage:
    from vidiq_api import VidiqAPI
    
    api = VidiqAPI("your_auth_token_here")
    result = api.analyze_keyword("youtube SEO")
    print(result)
"""

import requests
import json
import time
import os
import csv
from typing import Dict, Optional, Any, List


class VidiqAPI:
    """Simple Python wrapper for vidIQ API"""
    
    def __init__(self, auth_token: str):
        """
        Initialize the vidIQ API client
        
        Args:
            auth_token: Your vidIQ authorization token
        """
        self.auth_token = auth_token
        self.base_url = "https://api.vidiq.com/v0/hottersearch"
        self.keyword_search_url = "https://api.vidiq.com/xwords/keyword_search/"
        self.related_search_url = "https://api.vidiq.com/xwords/hottersearch"
        self.session = requests.Session()
        self.session.headers.update({
            'Host': 'api.vidiq.com',
            'Authorization': f'Bearer {auth_token}',
            'User-Agent': 'PostmanRuntime/7.29.2'
        })
    
    def analyze_keyword(self, keyword: str, delay: float = 1.0) -> Dict[str, Any]:
        """
        Analyze a single keyword using vidIQ API
        
        Args:
            keyword: The keyword to analyze
            delay: Delay between requests (seconds)
            
        Returns:
            Dictionary containing keyword analysis data
            
        Raises:
            Exception: If API call fails or returns error
        """
        if not keyword.strip():
            raise ValueError("Keyword cannot be empty")
        
        # Add delay to respect rate limits
        if delay > 0:
            time.sleep(delay)
        
        # Prepare API request
        params = {
            'q': keyword.strip(),
            'im': '4.5',
            'group': 'V5',
            'src': ''
        }
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API errors
            if not data or 'search_stats' not in data:
                raise Exception(f"No data returned for keyword: {keyword}")
            
            # Extract keyword data - try different case variations
            search_stats = data.get('search_stats', {})
            compvol = search_stats.get('compvol', {})
            
            # Try exact match first, then case variations
            keyword_data = None
            variations = [keyword, keyword.lower(), keyword.upper(), keyword.title()]
            
            for variation in variations:
                if variation in compvol:
                    keyword_data = compvol[variation]
                    break
            
            if not keyword_data:
                available_keys = list(compvol.keys())
                raise Exception(f"No analysis data found for keyword: {keyword}. Available keywords: {available_keys}")
            
            # Format response
            result = {
                'keyword': keyword,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'data': {
                    'volume': keyword_data.get('volume', 'N/A'),
                    'competition': keyword_data.get('competition', 'N/A'),
                    'estimated_monthly_search': keyword_data.get('estimated_monthly_search', 'N/A'),
                    'overall': keyword_data.get('overall', 'N/A')
                },
                'levels': {
                    'volume_level': self._get_competition_level(keyword_data.get('volume', 0)),
                    'competition_level': self._get_competition_level(keyword_data.get('competition', 0)),
                    'overall_level': self._get_competition_level(keyword_data.get('overall', 0))
                }
            }
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            raise Exception(f"API error: {str(e)}")
    
    def _get_competition_level(self, value: float) -> str:
        """Convert numeric value to competition level"""
        if value <= 20:
            return "Very Low"
        elif value <= 40:
            return "Low"
        elif value <= 60:
            return "Medium"
        elif value <= 80:
            return "High"
        else:
            return "Very High"
    
    def analyze_multiple_keywords(self, keywords: list, delay: float = 1.0) -> Dict[str, Dict[str, Any]]:
        """
        Analyze multiple keywords
        
        Args:
            keywords: List of keywords to analyze
            delay: Delay between requests (seconds)
            
        Returns:
            Dictionary with keyword as key and analysis as value
        """
        results = {}
        
        for keyword in keywords:
            try:
                results[keyword] = self.analyze_keyword(keyword, delay)
                print(f"✅ Analyzed: {keyword}")
            except Exception as e:
                print(f"❌ Failed: {keyword} - {str(e)}")
                results[keyword] = {'error': str(e)}
        
        return results
    
    def get_matching_keywords(self, keyword: str, limit: int = 300, delay: float = 1.0) -> Dict[str, Any]:
        """
        Get matching keywords (permutations) for a given keyword
        
        Args:
            keyword: The keyword to find matches for
            limit: Maximum number of results to return (default: 300)
            delay: Delay between requests (seconds)
            
        Returns:
            Dictionary containing matching keywords data
            
        Raises:
            Exception: If API call fails or returns error
        """
        if not keyword.strip():
            raise ValueError("Keyword cannot be empty")
        
        # Add delay to respect rate limits
        if delay > 0:
            time.sleep(delay)
        
        params = {
            'term': keyword.strip(),
            'part': 'permutations',
            'limit': limit
        }
        
        try:
            response = self.session.get(self.keyword_search_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if not data:
                raise Exception(f"No matching keywords found for: {keyword}")
            
            # Format response
            result = {
                'keyword': keyword,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'matching_keywords',
                'data': data,
                'count': len(data.get('permutations', [])) if 'permutations' in data else 0
            }
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            raise Exception(f"API error: {str(e)}")
    
    def get_related_keywords(self, keyword: str, min_related_score: int = 0, group: str = "v5", delay: float = 1.0) -> Dict[str, Any]:
        """
        Get related keywords for a given keyword
        
        Args:
            keyword: The keyword to find related terms for
            min_related_score: Minimum score for related keywords (default: 0)
            group: API group version (default: "v5")
            delay: Delay between requests (seconds)
            
        Returns:
            Dictionary containing related keywords data
            
        Raises:
            Exception: If API call fails or returns error
        """
        if not keyword.strip():
            raise ValueError("Keyword cannot be empty")
        
        # Add delay to respect rate limits
        if delay > 0:
            time.sleep(delay)
        
        params = {
            'q': keyword.strip(),
            'min_related_score': min_related_score,
            'group': group
        }
        
        try:
            response = self.session.get(self.related_search_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if not data:
                raise Exception(f"No related keywords found for: {keyword}")
            
            # Extract related keywords from the response
            related_keywords = []
            if 'keywords' in data:
                related_keywords = data['keywords']
            elif 'related_keywords' in data:
                related_keywords = data['related_keywords']
            elif 'search_stats' in data and 'related' in data['search_stats']:
                related_keywords = data['search_stats']['related']
            
            # Format response
            result = {
                'keyword': keyword,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'related_keywords',
                'data': related_keywords,
                'count': len(related_keywords),
                'raw_response': data  # Include full response for debugging
            }
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            raise Exception(f"API error: {str(e)}")
    
    def get_questions(self, keyword: str, limit: int = 300, delay: float = 1.0) -> Dict[str, Any]:
        """
        Get question-based keywords for a given keyword
        
        Args:
            keyword: The keyword to find questions for
            limit: Maximum number of results to return (default: 300)
            delay: Delay between requests (seconds)
            
        Returns:
            Dictionary containing question keywords data
            
        Raises:
            Exception: If API call fails or returns error
        """
        if not keyword.strip():
            raise ValueError("Keyword cannot be empty")
        
        # Add delay to respect rate limits
        if delay > 0:
            time.sleep(delay)
        
        params = {
            'term': keyword.strip(),
            'part': 'questions',
            'limit': limit
        }
        
        try:
            response = self.session.get(self.keyword_search_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if not data:
                raise Exception(f"No questions found for: {keyword}")
            
            # Format response
            result = {
                'keyword': keyword,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'questions',
                'data': data,
                'count': len(data.get('questions', [])) if 'questions' in data else 0
            }
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            raise Exception(f"API error: {str(e)}")
    
    def export_to_csv(self, keyword: str, output_file: str = None, limit: int = 300, delay: float = 1.0) -> str:
        """
        Export all keyword research data (related, matching, questions) to CSV format
        
        Args:
            keyword: The keyword to research
            output_file: Path to output CSV file (optional, defaults to keyword-based filename)
            limit: Maximum number of results per category (default: 300)
            delay: Delay between API requests (seconds)
            
        Returns:
            Path to the created CSV file
            
        Raises:
            Exception: If any API call fails or CSV creation fails
        """
        if not keyword.strip():
            raise ValueError("Keyword cannot be empty")
        
        # Generate default filename if not provided
        if not output_file:
            safe_keyword = "".join(c for c in keyword if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_keyword = safe_keyword.replace(' ', '_')
            output_file = f"{safe_keyword}_keywords.csv"
        
        try:
            print(f"🔍 Gathering keyword data for: {keyword}")
            
            # Get all three types of data
            related_data = self.get_related_keywords(keyword, delay=delay)
            matching_data = self.get_matching_keywords(keyword, limit=limit, delay=delay)
            questions_data = self.get_questions(keyword, limit=limit, delay=delay)
            
            # Prepare CSV data
            csv_rows = []
            
            # Add related keywords
            self._add_related_to_csv(csv_rows, related_data)
            
            # Add matching keywords
            self._add_matching_to_csv(csv_rows, matching_data)
            
            # Add questions
            self._add_questions_to_csv(csv_rows, questions_data)
            
            # Write to CSV file
            self._write_csv_file(output_file, csv_rows, keyword)
            
            print(f"✅ CSV exported successfully: {output_file}")
            print(f"📊 Total keywords exported: {len(csv_rows)}")
            
            return output_file
            
        except Exception as e:
            raise Exception(f"Failed to export CSV: {str(e)}")
    
    def _add_related_to_csv(self, csv_rows: List[Dict], related_data: Dict) -> None:
        """Add related keywords data to CSV rows"""
        related_keywords = related_data.get('data', [])
        
        for item in related_keywords:
            if isinstance(item, dict):
                keyword_text = item.get('keyword', str(item))
                score = item.get('score', 'N/A')
                volume = item.get('volume', 'N/A')
                competition = item.get('competition', 'N/A')
            else:
                keyword_text = str(item)
                score = 'N/A'
                volume = 'N/A'
                competition = 'N/A'
            
            csv_rows.append({
                'keyword': keyword_text,
                'type': 'related',
                'score': score,
                'volume': volume,
                'competition': competition,
                'source_keyword': related_data.get('keyword', ''),
                'timestamp': related_data.get('timestamp', '')
            })
    
    def _add_matching_to_csv(self, csv_rows: List[Dict], matching_data: Dict) -> None:
        """Add matching keywords data to CSV rows"""
        permutations = matching_data.get('data', {}).get('permutations', [])
        
        for item in permutations:
            if isinstance(item, dict):
                keyword_text = item.get('keyword', str(item))
                score = item.get('score', 'N/A')
                volume = item.get('volume', 'N/A')
                competition = item.get('competition', 'N/A')
            else:
                keyword_text = str(item)
                score = 'N/A'
                volume = 'N/A'
                competition = 'N/A'
            
            csv_rows.append({
                'keyword': keyword_text,
                'type': 'matching',
                'score': score,
                'volume': volume,
                'competition': competition,
                'source_keyword': matching_data.get('keyword', ''),
                'timestamp': matching_data.get('timestamp', '')
            })
    
    def _add_questions_to_csv(self, csv_rows: List[Dict], questions_data: Dict) -> None:
        """Add questions data to CSV rows"""
        questions = questions_data.get('data', {}).get('questions', [])
        
        for item in questions:
            if isinstance(item, dict):
                keyword_text = item.get('keyword', str(item))
                score = item.get('score', 'N/A')
                volume = item.get('volume', 'N/A')
                competition = item.get('competition', 'N/A')
            else:
                keyword_text = str(item)
                score = 'N/A'
                volume = 'N/A'
                competition = 'N/A'
            
            csv_rows.append({
                'keyword': keyword_text,
                'type': 'question',
                'score': score,
                'volume': volume,
                'competition': competition,
                'source_keyword': questions_data.get('keyword', ''),
                'timestamp': questions_data.get('timestamp', '')
            })
    
    def _write_csv_file(self, output_file: str, csv_rows: List[Dict], source_keyword: str) -> None:
        """Write CSV data to file"""
        if not csv_rows:
            raise Exception("No data to export")
        
        # Define CSV headers
        headers = ['keyword', 'type', 'score', 'volume', 'competition', 'source_keyword', 'timestamp']
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                
                # Write header
                writer.writeheader()
                
                # Write data rows
                for row in csv_rows:
                    writer.writerow(row)
                    
        except Exception as e:
            raise Exception(f"Failed to write CSV file: {str(e)}")
    
    def export_separate_csvs(self, keyword: str, output_dir: str = ".", limit: int = 300, delay: float = 1.0) -> Dict[str, str]:
        """
        Export keyword research data to separate CSV files for each type
        
        Args:
            keyword: The keyword to research
            output_dir: Directory to save CSV files (default: current directory)
            limit: Maximum number of results per category (default: 300)
            delay: Delay between API requests (seconds)
            
        Returns:
            Dictionary with file paths for each exported CSV type
            
        Raises:
            Exception: If any API call fails or CSV creation fails
        """
        if not keyword.strip():
            raise ValueError("Keyword cannot be empty")
        
        # Create safe filename base
        safe_keyword = "".join(c for c in keyword if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_keyword = safe_keyword.replace(' ', '_')
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        file_paths = {}
        
        try:
            print(f"🔍 Gathering keyword data for: {keyword}")
            
            # Export related keywords
            related_data = self.get_related_keywords(keyword, delay=delay)
            related_file = os.path.join(output_dir, f"{safe_keyword}_related.csv")
            self._export_single_type_csv(related_data, related_file, 'related')
            file_paths['related'] = related_file
            
            # Export matching keywords
            matching_data = self.get_matching_keywords(keyword, limit=limit, delay=delay)
            matching_file = os.path.join(output_dir, f"{safe_keyword}_matching.csv")
            self._export_single_type_csv(matching_data, matching_file, 'matching')
            file_paths['matching'] = matching_file
            
            # Export questions
            questions_data = self.get_questions(keyword, limit=limit, delay=delay)
            questions_file = os.path.join(output_dir, f"{safe_keyword}_questions.csv")
            self._export_single_type_csv(questions_data, questions_file, 'questions')
            file_paths['questions'] = questions_file
            
            print(f"✅ All CSV files exported successfully to: {output_dir}")
            
            return file_paths
            
        except Exception as e:
            raise Exception(f"Failed to export separate CSVs: {str(e)}")
    
    def _export_single_type_csv(self, data: Dict, output_file: str, data_type: str) -> None:
        """Export a single type of data to CSV"""
        csv_rows = []
        
        if data_type == 'related':
            self._add_related_to_csv(csv_rows, data)
        elif data_type == 'matching':
            self._add_matching_to_csv(csv_rows, data)
        elif data_type == 'questions':
            self._add_questions_to_csv(csv_rows, data)
        
        self._write_csv_file(output_file, csv_rows, data.get('keyword', ''))
        
        print(f"📄 Exported {len(csv_rows)} {data_type} keywords to: {output_file}")


def main():
    """Command line interface"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python vidiq_api.py 'your keyword'")
        print("Example: python vidiq_api.py 'youtube SEO'")
        sys.exit(1)
    
    # Get auth token from environment variable or command line
    auth_token = os.getenv('VIDIQ_TOKEN')
    
    if not auth_token:
        print("Error: Please set your vidIQ auth token as VIDIQ_TOKEN environment variable")
        print("Example: export VIDIQ_TOKEN='your_token_here'")
        print("Or: VIDIQ_TOKEN='your_token' python vidiq_api.py 'keyword'")
        sys.exit(1)
    
    keyword = sys.argv[1]
    
    try:
        api = VidiqAPI(auth_token)
        result = api.analyze_keyword(keyword)
        
        print(f"\n📊 Keyword Analysis: {result['keyword']}")
        print("=" * 50)
        print(f"Volume: {result['data']['volume']}")
        print(f"Competition: {result['data']['competition']}")
        print(f"Monthly Searches: {result['data']['estimated_monthly_search']}")
        print(f"Overall Score: {result['data']['overall']}")
        print(f"Volume Level: {result['levels']['volume_level']}")
        print(f"Competition Level: {result['levels']['competition_level']}")
        print("=" * 50)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

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
from typing import Dict, Optional, Any


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

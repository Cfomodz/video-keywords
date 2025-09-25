"""
Main VidiqAPI client for keyword analysis.
"""

import os
import time
from typing import Dict, List, Optional
import requests


class VidiqAPI:
    """
    A Python wrapper for the vidIQ keyword analysis API.
    
    This class provides methods to analyze YouTube keywords using vidIQ's API,
    including batch processing and rate limiting capabilities.
    """
    
    BASE_URL = "https://api.vidiq.com/v1/youtube/keywords"
    
    def __init__(self, auth_token: Optional[str] = None):
        """
        Initialize the VidiqAPI client.
        
        Args:
            auth_token: Your vidIQ authorization token. If not provided,
                       will try to get from VIDIQ_TOKEN environment variable.
        
        Raises:
            ValueError: If no auth token is provided or found in environment.
        """
        self.auth_token = auth_token or os.getenv('VIDIQ_TOKEN')
        if not self.auth_token:
            raise ValueError(
                "No auth token provided. Either pass it directly or set VIDIQ_TOKEN environment variable."
            )
        
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json',
            'User-Agent': 'vidiq-python-api/1.0.0'
        })
    
    def analyze_keyword(self, keyword: str, delay: float = 1.0) -> Dict:
        """
        Analyze a single keyword for YouTube SEO metrics.
        
        Args:
            keyword: The keyword to analyze
            delay: Delay in seconds before making the request (rate limiting)
        
        Returns:
            Dict containing keyword analysis data including volume, competition,
            and difficulty levels.
        
        Raises:
            ValueError: If keyword is empty or invalid
            Exception: If API request fails
        """
        if not keyword or not keyword.strip():
            raise ValueError("Keyword cannot be empty")
        
        keyword = keyword.strip()
        
        # Rate limiting
        if delay > 0:
            time.sleep(delay)
        
        try:
            response = self.session.get(
                self.BASE_URL,
                params={'keyword': keyword}
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Process and format the response
            return self._format_response(keyword, data)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed for keyword '{keyword}': {str(e)}")
    
    def analyze_multiple_keywords(self, keywords: List[str], delay: float = 1.0) -> Dict:
        """
        Analyze multiple keywords with automatic error handling.
        
        Args:
            keywords: List of keywords to analyze
            delay: Delay between requests in seconds
        
        Returns:
            Dict with keyword as key and analysis data as value.
            Failed requests will have 'error' key in their data.
        """
        results = {}
        
        for keyword in keywords:
            try:
                result = self.analyze_keyword(keyword, delay)
                results[keyword] = result
            except Exception as e:
                results[keyword] = {'error': str(e)}
        
        return results
    
    def _format_response(self, keyword: str, data: Dict) -> Dict:
        """
        Format the API response into a consistent structure.
        
        Args:
            keyword: The original keyword
            data: Raw API response data
        
        Returns:
            Formatted response dictionary
        """
        # Extract metrics from API response
        volume = data.get('volume', 0)
        competition = data.get('competition', 0)
        estimated_searches = data.get('estimated_monthly_search', 0)
        overall_score = data.get('overall', 0)
        
        # Calculate difficulty levels
        volume_level = self._get_level(volume, [20, 40, 60, 80])
        competition_level = self._get_level(competition, [20, 40, 60, 80])
        overall_level = self._get_level(overall_score, [20, 40, 60, 80])
        
        return {
            'keyword': keyword,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'data': {
                'volume': volume,
                'competition': competition,
                'estimated_monthly_search': estimated_searches,
                'overall': overall_score
            },
            'levels': {
                'volume_level': volume_level,
                'competition_level': competition_level,
                'overall_level': overall_level
            }
        }
    
    def _get_level(self, score: float, thresholds: List[int]) -> str:
        """
        Convert numeric score to difficulty level.
        
        Args:
            score: Numeric score (0-100)
            thresholds: List of threshold values
        
        Returns:
            String representation of difficulty level
        """
        levels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
        
        for i, threshold in enumerate(thresholds):
            if score <= threshold:
                return levels[i]
        
        return levels[-1]

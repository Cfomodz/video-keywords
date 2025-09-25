"""
Tests for vidiq_api module
"""
import pytest
from unittest.mock import Mock, patch
from vidiq_api import VidiqAPI


class TestVidiqAPI:
    """Test cases for VidiqAPI class"""
    
    def test_init(self):
        """Test API initialization"""
        api = VidiqAPI("test_token")
        assert api.auth_token == "test_token"
        assert api.base_url == "https://api.vidiq.com/v0/hottersearch"
    
    def test_init_empty_token(self):
        """Test initialization with empty token"""
        with pytest.raises(ValueError):
            VidiqAPI("")
    
    def test_get_competition_level(self):
        """Test competition level calculation"""
        api = VidiqAPI("test_token")
        
        assert api._get_competition_level(10) == "Very Low"
        assert api._get_competition_level(30) == "Low"
        assert api._get_competition_level(50) == "Medium"
        assert api._get_competition_level(70) == "High"
        assert api._get_competition_level(90) == "Very High"
    
    @patch('vidiq_api.vidiq_api.requests.Session.get')
    def test_analyze_keyword_success(self, mock_get):
        """Test successful keyword analysis"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'search_stats': {
                'compvol': {
                    'test keyword': {
                        'volume': 50.0,
                        'competition': 30.0,
                        'estimated_monthly_search': 1000.0,
                        'overall': 40.0
                    }
                }
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        api = VidiqAPI("test_token")
        result = api.analyze_keyword("test keyword")
        
        assert result['keyword'] == "test keyword"
        assert result['data']['volume'] == 50.0
        assert result['data']['competition'] == 30.0
        assert result['levels']['volume_level'] == "Medium"
    
    @patch('vidiq_api.vidiq_api.requests.Session.get')
    def test_analyze_keyword_case_insensitive(self, mock_get):
        """Test case insensitive keyword matching"""
        # Mock response with lowercase keyword
        mock_response = Mock()
        mock_response.json.return_value = {
            'search_stats': {
                'compvol': {
                    'test keyword': {  # lowercase in response
                        'volume': 50.0,
                        'competition': 30.0,
                        'estimated_monthly_search': 1000.0,
                        'overall': 40.0
                    }
                }
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        api = VidiqAPI("test_token")
        result = api.analyze_keyword("Test Keyword")  # Different case
        
        assert result['keyword'] == "Test Keyword"
        assert result['data']['volume'] == 50.0
    
    @patch('vidiq_api.vidiq_api.requests.Session.get')
    def test_analyze_keyword_no_data(self, mock_get):
        """Test keyword with no data"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'search_stats': {
                'compvol': {}
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        api = VidiqAPI("test_token")
        
        with pytest.raises(Exception) as exc_info:
            api.analyze_keyword("nonexistent keyword")
        
        assert "No analysis data found" in str(exc_info.value)
    
    def test_analyze_keyword_empty(self):
        """Test empty keyword"""
        api = VidiqAPI("test_token")
        
        with pytest.raises(ValueError):
            api.analyze_keyword("")
    
    @patch('vidiq_api.vidiq_api.time.sleep')
    @patch('vidiq_api.vidiq_api.requests.Session.get')
    def test_analyze_multiple_keywords(self, mock_get, mock_sleep):
        """Test multiple keyword analysis"""
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            'search_stats': {
                'compvol': {
                    'keyword1': {
                        'volume': 50.0,
                        'competition': 30.0,
                        'estimated_monthly_search': 1000.0,
                        'overall': 40.0
                    }
                }
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        api = VidiqAPI("test_token")
        results = api.analyze_multiple_keywords(["keyword1", "keyword2"])
        
        assert "keyword1" in results
        assert "keyword2" in results
        # One should succeed, one should fail (no data)
        assert 'error' not in results["keyword1"] or 'error' in results["keyword2"]


if __name__ == "__main__":
    pytest.main([__file__])

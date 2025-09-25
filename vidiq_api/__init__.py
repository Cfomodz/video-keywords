"""
vidIQ Python API - YouTube Keyword Analysis

A simple Python wrapper for vidIQ keyword analysis API.
Perfect for integrating YouTube SEO research into your Python projects.

Usage:
    from vidiq_api import VidiqAPI
    
    api = VidiqAPI("your_auth_token")
    result = api.analyze_keyword("youtube SEO")
    print(result['data']['volume'])
"""

from .vidiq_api import VidiqAPI

__version__ = "1.0.0"
__author__ = "vidIQ API Wrapper"
__all__ = ["VidiqAPI"]

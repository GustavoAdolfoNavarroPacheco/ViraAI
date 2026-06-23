import json
import time
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any, Optional
from app.core.config import settings

class SocialService:
    @staticmethod
    def _make_http_request(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None, data: Any = None) -> Any:
        """
        Helper method to execute HTTP requests using urllib without external dependencies.
        """
        headers = headers or {}
        req_data = None
        
        if data is not None:
            if headers.get("Content-Type") == "application/json":
                req_data = json.dumps(data).encode("utf-8")
            else:
                req_data = urllib.parse.urlencode(data).encode("utf-8")
                
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_content = e.read().decode("utf-8")
            try:
                err_json = json.loads(err_content)
                msg = err_json.get("error_description") or err_json.get("message") or err_content
            except Exception:
                msg = err_content
            raise ValueError(f"HTTP Error {e.code}: {msg}")
        except Exception as e:
            raise ValueError(f"Connection Error: {str(e)}")

    @classmethod
    def get_auth_url(cls, platform: str, state: str = "state") -> str:
        """
        Generates the OAuth 2.0 authorization URL.
        If credentials are not configured, returns a mock URL pointing directly to the callback.
        """
        platform_lower = platform.lower().strip()
        if platform_lower == "linkedin":
            if not settings.LINKEDIN_CLIENT_ID:
                # Mock route: returns callback redirect with mock params directly
                return f"{settings.LINKEDIN_REDIRECT_URI}?code=mock_linkedin_code_abc123&state={state}"
            
            params = {
                "response_type": "code",
                "client_id": settings.LINKEDIN_CLIENT_ID,
                "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
                "state": state,
                "scope": "w_member_social"
            }
            return f"https://www.linkedin.com/oauth/v2/authorization?{urllib.parse.urlencode(params)}"
            
        elif platform_lower == "twitter":
            if not settings.TWITTER_CLIENT_ID:
                return f"{settings.TWITTER_REDIRECT_URI}?code=mock_twitter_code_xyz789&state={state}"
                
            params = {
                "response_type": "code",
                "client_id": settings.TWITTER_CLIENT_ID,
                "redirect_uri": settings.TWITTER_REDIRECT_URI,
                "state": state,
                "code_challenge": "challenge",
                "code_challenge_method": "plain",
                "scope": "tweet.read tweet.write offline.access"
            }
            return f"https://twitter.com/i/oauth2/authorize?{urllib.parse.urlencode(params)}"
        else:
            raise ValueError(f"Platform {platform} is not supported")

    @classmethod
    def exchange_code_for_tokens(cls, platform: str, code: str) -> Dict[str, Any]:
        """
        Exchanges the authorization code for access and refresh tokens.
        """
        platform_lower = platform.lower().strip()
        
        # Mode: Simulation
        if code.startswith("mock_"):
            return {
                "access_token": f"mock_access_token_{platform_lower}_{int(time.time())}",
                "refresh_token": f"mock_refresh_token_{platform_lower}_{int(time.time())}",
                "expires_in": 3600,
                "name": f"Mock {platform.capitalize()} Creator",
                "profile_url": f"https://{platform_lower}.com/mock_profile"
            }
            
        if platform_lower == "linkedin":
            if not settings.LINKEDIN_CLIENT_ID or not settings.LINKEDIN_CLIENT_SECRET:
                raise ValueError("LinkedIn credentials are not configured")
                
            token_url = "https://www.linkedin.com/oauth/v2/accessToken"
            payload = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
                "client_id": settings.LINKEDIN_CLIENT_ID,
                "client_secret": settings.LINKEDIN_CLIENT_SECRET
            }
            token_data = cls._make_http_request(token_url, method="POST", data=payload)
            
            # Fetch profile name
            profile_url = "https://api.linkedin.com/v2/userinfo"
            headers = {"Authorization": f"Bearer {token_data['access_token']}"}
            profile_data = cls._make_http_request(profile_url, headers=headers)
            
            name = profile_data.get("name") or f"LinkedIn Profile {profile_data.get('sub')}"
            
            return {
                "access_token": token_data["access_token"],
                "refresh_token": token_data.get("refresh_token"),
                "expires_in": token_data.get("expires_in", 3600),
                "name": name,
                "profile_url": f"https://linkedin.com/in/{profile_data.get('sub', 'profile')}"
            }
            
        elif platform_lower == "twitter":
            if not settings.TWITTER_CLIENT_ID or not settings.TWITTER_CLIENT_SECRET:
                raise ValueError("Twitter credentials are not configured")
                
            token_url = "https://api.twitter.com/2/oauth2/token"
            payload = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.TWITTER_REDIRECT_URI,
                "client_id": settings.TWITTER_CLIENT_ID,
                "code_verifier": "challenge"
            }
            
            # Twitter requires Basic Auth header for client authentication
            import base64
            auth_str = f"{settings.TWITTER_CLIENT_ID}:{settings.TWITTER_CLIENT_SECRET}"
            encoded_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
            headers = {
                "Authorization": f"Basic {encoded_auth}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            token_data = cls._make_http_request(token_url, method="POST", headers=headers, data=payload)
            
            # Fetch user profile
            profile_url = "https://api.twitter.com/2/users/me"
            headers_profile = {"Authorization": f"Bearer {token_data['access_token']}"}
            profile_data = cls._make_http_request(profile_url, headers=headers_profile)
            
            username = profile_data.get("data", {}).get("username", "profile")
            name = profile_data.get("data", {}).get("name", f"Twitter User {username}")
            
            return {
                "access_token": token_data["access_token"],
                "refresh_token": token_data.get("refresh_token"),
                "expires_in": token_data.get("expires_in", 7200),
                "name": name,
                "profile_url": f"https://twitter.com/{username}"
            }
        else:
            raise ValueError(f"Platform {platform} is not supported")

    @classmethod
    def refresh_access_token(cls, platform: str, refresh_token: str) -> Dict[str, Any]:
        """
        Renews the access token using the refresh token.
        """
        platform_lower = platform.lower().strip()
        
        # Mode: Simulation
        if not refresh_token or refresh_token.startswith("mock_"):
            return {
                "access_token": f"mock_access_token_{platform_lower}_refreshed_{int(time.time())}",
                "refresh_token": f"mock_refresh_token_{platform_lower}_refreshed_{int(time.time())}",
                "expires_in": 3600
            }
            
        if platform_lower == "linkedin":
            if not settings.LINKEDIN_CLIENT_ID or not settings.LINKEDIN_CLIENT_SECRET:
                raise ValueError("LinkedIn credentials are not configured")
                
            token_url = "https://www.linkedin.com/oauth/v2/accessToken"
            payload = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": settings.LINKEDIN_CLIENT_ID,
                "client_secret": settings.LINKEDIN_CLIENT_SECRET
            }
            token_data = cls._make_http_request(token_url, method="POST", data=payload)
            return {
                "access_token": token_data["access_token"],
                "refresh_token": token_data.get("refresh_token"),
                "expires_in": token_data.get("expires_in", 3600)
            }
            
        elif platform_lower == "twitter":
            if not settings.TWITTER_CLIENT_ID or not settings.TWITTER_CLIENT_SECRET:
                raise ValueError("Twitter credentials are not configured")
                
            token_url = "https://api.twitter.com/2/oauth2/token"
            payload = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": settings.TWITTER_CLIENT_ID
            }
            
            import base64
            auth_str = f"{settings.TWITTER_CLIENT_ID}:{settings.TWITTER_CLIENT_SECRET}"
            encoded_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
            headers = {
                "Authorization": f"Basic {encoded_auth}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            token_data = cls._make_http_request(token_url, method="POST", headers=headers, data=payload)
            return {
                "access_token": token_data["access_token"],
                "refresh_token": token_data.get("refresh_token"),
                "expires_in": token_data.get("expires_in", 7200)
            }
        else:
            raise ValueError(f"Platform {platform} is not supported")

    @classmethod
    def publish_post(cls, platform: str, access_token: str, content: str, media_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Publishes content to LinkedIn or Twitter/X.
        Supports Mock fallback if access_token starts with mock_.
        """
        platform_lower = platform.lower().strip()
        
        # Mode: Simulation
        if not access_token or access_token.startswith("mock_"):
            print(f"[Mock Publish] Content published to {platform_lower} successfully!")
            return {
                "success": True,
                "post_id": f"mock_post_{platform_lower}_{int(time.time())}",
                "url": f"https://{platform_lower}.com/post/mock_post_{platform_lower}"
            }
            
        if platform_lower == "linkedin":
            # For LinkedIn we need the member ID/URN first
            # Userinfo returns the sub / subject (which is the member ID)
            profile_url = "https://api.linkedin.com/v2/userinfo"
            headers = {"Authorization": f"Bearer {access_token}"}
            profile_data = cls._make_http_request(profile_url, headers=headers)
            member_id = profile_data.get("sub")
            
            if not member_id:
                raise ValueError("Could not retrieve member ID from LinkedIn Userinfo")
                
            post_url = "https://api.linkedin.com/v2/posts"
            headers_post = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            # Formulate the post payload
            payload = {
                "author": f"urn:li:person:{member_id}",
                "commentary": content,
                "visibility": "PUBLIC",
                "distribution": {
                    "feedDistribution": "MAIN_FEED",
                    "targetEntities": []
                },
                "lifecycleState": "PUBLISHED"
            }
            
            # If media is provided, we can handle it or include it. In standard posts API,
            # publishing media requires dynamic upload, but to be simple and safe we embed the url in text
            if media_url:
                payload["commentary"] = f"{content}\n\n{media_url}"
                
            response = cls._make_http_request(post_url, method="POST", headers=headers_post, data=payload)
            # The API returns 201 Created with x-restli-id header in response.
            # Our _make_http_request helper handles JSON response, LinkedIn posts endpoint might return empty body or post details.
            # To be safe, we parse response or build a success object.
            return {
                "success": True,
                "post_id": response.get("id") or f"urn:li:share:{member_id}",
                "url": f"https://linkedin.com"
            }
            
        elif platform_lower == "twitter":
            post_url = "https://api.twitter.com/2/tweets"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {"text": content}
            if media_url:
                payload["text"] = f"{content} {media_url}"
                
            response = cls._make_http_request(post_url, method="POST", headers=headers, data=payload)
            tweet_id = response.get("data", {}).get("id")
            
            return {
                "success": True,
                "post_id": tweet_id,
                "url": f"https://twitter.com/i/web/status/{tweet_id}"
            }
        else:
            raise ValueError(f"Platform {platform} is not supported")

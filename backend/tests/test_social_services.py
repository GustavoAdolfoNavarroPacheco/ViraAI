import unittest
from app.infrastructure.social_services import SocialService

class TestSocialServices(unittest.TestCase):
    def test_get_auth_url_mock(self):
        print("Testing get_auth_url in mock mode...")
        linkedin_url = SocialService.get_auth_url("linkedin", "my_state")
        assert "callback/linkedin" in linkedin_url
        assert "code=mock_linkedin_code" in linkedin_url
        assert "state=my_state" in linkedin_url

        twitter_url = SocialService.get_auth_url("twitter", "state_123")
        assert "callback/twitter" in twitter_url
        assert "code=mock_twitter_code" in twitter_url
        assert "state=state_123" in twitter_url
        print("-> test_get_auth_url_mock: PASSED")

    def test_exchange_code_for_tokens_mock(self):
        print("Testing exchange_code_for_tokens in mock mode...")
        token_data = SocialService.exchange_code_for_tokens("linkedin", "mock_linkedin_code")
        assert "access_token" in token_data
        assert "refresh_token" in token_data
        assert "expires_in" in token_data
        assert token_data["name"] == "Mock Linkedin Creator"
        assert "linkedin.com" in token_data["profile_url"]
        print("-> test_exchange_code_for_tokens_mock: PASSED")

    def test_refresh_access_token_mock(self):
        print("Testing refresh_access_token in mock mode...")
        refresh_data = SocialService.refresh_access_token("linkedin", "mock_refresh_token_123")
        assert "access_token" in refresh_data
        assert "mock_access_token_linkedin_refreshed" in refresh_data["access_token"]
        assert "expires_in" in refresh_data
        print("-> test_refresh_access_token_mock: PASSED")

    def test_publish_post_mock(self):
        print("Testing publish_post in mock mode...")
        publish_result = SocialService.publish_post(
            platform="twitter",
            access_token="mock_token_abc",
            content="Testing mock publishing!",
            media_url="http://example.com/image.png"
        )
        assert publish_result["success"] is True
        assert "mock_post_twitter" in publish_result["post_id"]
        assert "twitter.com" in publish_result["url"]
        print("-> test_publish_post_mock: PASSED")

if __name__ == "__main__":
    unittest.main()

import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient

# Import our application
from infrastructure.main import app
from domain.services.domclick_service import DomClickService
from infrastructure.external.validator_client import ValidatorClient
from domain.models.search import SearchResult


class TestValidatorClient:
    """Test Validator API client"""
    
    def setup_method(self):
        self.client = ValidatorClient(endpoint="http://test-validator")
    
    @pytest.mark.asyncio
    async def test_fallback_validation_phone(self):
        """Test fallback validation for phone numbers"""
        queries = ["79319999999", "testuser@gmail.com"]
        
        results = self.client._fallback_validation(queries)
        
        assert len(results) == 2
        
        # Check phone result
        phone_result = results[0]
        assert phone_result.body["type"] == "phone"
        assert phone_result.body["clean_data"] == "79319999999"
        
        # Check email result
        email_result = results[1]
        assert email_result.body["type"] == "email"
        assert email_result.body["clean_data"] == "testuser@gmail.com"
    
    @pytest.mark.asyncio
    async def test_fallback_validation_unknown(self):
        """Test fallback validation for unknown types"""
        queries = ["random_text"]
        
        results = self.client._fallback_validation(queries)
        
        assert len(results) == 1
        assert results[0].body["type"] == "unknown"
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.post')
    async def test_validate_api_success(self, mock_post):
        """Test successful API validation"""
        # Mock successful API response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=[
            {
                "headers": {"sender": "tw.tools.validator"},
                "body": {
                    "request_data": "79319999999",
                    "type": "phone",
                    "clean_data": "79319999999"
                },
                "extra": {"country_name": "Россия"}
            }
        ])
        mock_post.return_value.__aenter__.return_value = mock_response
        
        results = await self.client.validate_queries(["79319999999"])
        
        assert len(results) == 1
        assert results[0].body["type"] == "phone"
    
    @pytest.mark.asyncio
    @patch('aiohttp.ClientSession.post')
    async def test_validate_api_failure_uses_fallback(self, mock_post):
        """Test fallback when API fails"""
        # Mock API failure
        mock_post.side_effect = Exception("Connection error")
        
        results = await self.client.validate_queries(["79319999999"])
        
        # Should use fallback validation
        assert len(results) == 1
        assert results[0].body["type"] == "phone"


class TestDomClickService:
    """Test DomClickService functionality"""
    
    def setup_method(self):
        self.service = DomClickService()

    @pytest.mark.asyncio
    async def test_search_with_valid_data(self):
        """Test search with mock successful response"""
        phone = "79319999999"
        
        # Mock the DomClick client to return valid data
        mock_response = {
            "casId": "1234567",
            "firstName": "Иван",
            "middleName": "Петрович",
            "lastName": "Сидоров",
            "partnerCard": {
                "photoUrl": "https://example.com/avatar.jpg",
                "clientReview": "4.8",
                "registeredAt": "2022-03-15T10:30:00Z",
                "dealsCount": 45,
                "clientCommentsCount": 23
            }
        }
        
        with patch('infrastructure.external.domclick_client.DomClickClient.search_user') as mock_search:
            mock_search.return_value = mock_response
            
            result = await self.service.search(phone)
            
            assert len(result) == 1
            assert result[0].first_name == "Иван"
            assert result[0].middle_name == "Петрович"
            assert result[0].last_name == "Сидоров"
            assert result[0].user_id == 1234567
            assert result[0].is_registered == "Да"
            assert result[0].is_partner == "Да"
            assert result[0].avatar == "https://example.com/avatar.jpg"
            assert result[0].partner_link == "https://agencies.domclick.ru/agent/1234567"
            assert result[0].client_review == "4.8"
            assert result[0].deals_count == 45
            assert result[0].client_comments_count == 23

    @pytest.mark.asyncio
    async def test_search_with_no_data(self):
        """Test search when no data is found"""
        phone = "79319999999"
        
        # Mock response with no casId (triggers empty result)
        mock_response = {
            "firstName": "Иван",
            # Missing casId field
        }
        
        with patch('infrastructure.external.domclick_client.DomClickClient.search_user') as mock_search:
            mock_search.return_value = mock_response
            
            result = await self.service.search(phone)
            
            assert result == []

    @pytest.mark.asyncio
    async def test_search_with_client_error(self):
        """Test search when client throws error"""
        phone = "79319999999"
        
        with patch('infrastructure.external.domclick_client.DomClickClient.search_user') as mock_search:
            mock_search.side_effect = Exception("API error")
            
            result = await self.service.search(phone)
            
            assert result == []

    @pytest.mark.asyncio
    async def test_adapt_response_without_partner_card(self):
        """Test response adaptation without partner card"""
        service = DomClickService()
        
        response_data = {
            "casId": "1234567",
            "firstName": "Иван",
            "middleName": "Петрович",
            "lastName": "Сидоров"
            # No partnerCard
        }
        
        results = service._adapt_response(response_data)
        
        assert len(results) == 1
        result = results[0]
        assert result.is_partner == "Нет"
        assert result.partner_link is None
        assert result.avatar is None
        assert result.client_review is None
        assert result.deals_count is None


class TestControllerIntegration:
    """Integration tests for controllers"""
    
    def setup_method(self):
        self.client = TestClient(app)

    @pytest.mark.asyncio
    async def test_common_controller_process_queries(self):
        """Test common controller processes multiple queries"""
        with patch('controllers.common_controller.validator_client.validate_queries') as mock_validate:
            with patch('controllers.common_controller.domclick_service.search') as mock_search:
                # Mock validator response
                mock_validate.return_value = [
                    {
                        "headers": {"sender": "tw.tools.validator"},
                        "body": {
                            "request_data": "79319999999",
                            "type": "phone",
                            "clean_data": "79319999999"
                        },
                        "extra": {"country_name": "Россия"}
                    },
                    {
                        "headers": {"sender": "tw.tools.validator"},
                        "body": {
                            "request_data": "test@example.com",
                            "type": "email", 
                            "clean_data": "test@example.com"
                        },
                        "extra": {}
                    }
                ]
                
                # Mock DomClick service response for phone
                mock_search.return_value = [SearchResult(
                    first_name="Иван",
                    middle_name="Петрович",
                    last_name="Сидоров",
                    user_id=1234567,
                    is_registered="Да",
                    is_partner="Да"
                )]
                
                response = self.client.post(
                    "/api/v1/common/process",
                    json={"queries": ["79319999999", "test@example.com"]}
                )
                
                assert response.status_code == 200
                data = response.json()
                
                assert len(data) == 2
                
                # Phone result should have search data
                phone_result = data[0]
                assert phone_result["headers"]["sender"] == "domclick-service"
                assert phone_result["body"]["results"][0]["first_name"] == "Иван"
                assert phone_result["extra"]["data_type"] == "phone"
                
                # Email result should indicate unsupported
                email_result = data[1]
                assert email_result["headers"]["sender"] == "common-controller"
                assert "Unsupported data type" in email_result["body"]["error"]

    @pytest.mark.asyncio
    async def test_domclick_controller_search_phone(self):
        """Test DomClick controller phone search"""
        with patch('controllers.domclick_controller.search_service.search') as mock_search:
            mock_search.return_value = [SearchResult(
                first_name="Иван",
                middle_name="Петрович",
                last_name="Сидоров", 
                user_id=1234567,
                is_registered="Да",
                is_partner="Да"
            )]
            
            response = self.client.get("/api/v1/domclick/search/phone/79319999999")
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["headers"]["sender"] == "domclick-service"
            assert len(data["body"]["results"]) == 1
            assert data["body"]["results"][0]["first_name"] == "Иван"
            assert data["extra"]["results_count"] == 1

    @pytest.mark.asyncio
    async def test_domclick_controller_search_no_data(self):
        """Test DomClick controller when no data found"""
        with patch('controllers.domclick_controller.search_service.search') as mock_search:
            mock_search.return_value = []  # No data found
            
            response = self.client.get("/api/v1/domclick/search/phone/79310000000")
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["body"]["results"] == []
            assert data["extra"]["results_count"] == 0

    @pytest.mark.asyncio
    async def test_common_controller_empty_queries(self):
        """Test common controller with empty queries"""
        response = self.client.post("/api/v1/common/process", json={"queries": []})
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_common_controller_validator_failure(self):
        """Test common controller when validator fails"""
        with patch('controllers.common_controller.validator_client.validate_queries') as mock_validate:
            mock_validate.return_value = []  # Empty response indicates validator failure

            response = self.client.post(
                "/api/v1/common/process",
                json={"queries": ["79319999999"]}
            )

            assert response.status_code == 500


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def setup_method(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        """Test health endpoint returns correct status"""
        response = self.client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "mode" in data

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = self.client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["message"] == "Sfera Information System API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "operational"

    def test_api_documentation_accessible(self):
        """Test API documentation is accessible"""
        response = self.client.get("/docs")
        assert response.status_code == 200

    def test_redoc_accessible(self):
        """Test ReDoc documentation is accessible"""
        response = self.client.get("/redoc")
        assert response.status_code == 200


class TestErrorScenarios:
    """Test error scenarios and edge cases"""
    
    def setup_method(self):
        self.client = TestClient(app)

    @pytest.mark.asyncio
    async def test_domclick_service_exception_handling(self):
        """Test DomClick service handles exceptions gracefully"""
        with patch('controllers.domclick_controller.search_service.search') as mock_search:
            mock_search.side_effect = Exception("Service unavailable")
            
            response = self.client.get("/api/v1/domclick/search/phone/79319999999")
            
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data

    @pytest.mark.asyncio
    async def test_common_controller_partial_failure(self):
        """Test common controller handles partial failures"""
        with patch('controllers.common_controller.validator_client.validate_queries') as mock_validate:
            with patch('controllers.common_controller.domclick_service.search') as mock_search:
                # Mock validator response with mixed types
                mock_validate.return_value = [
                    {
                        "body": {"type": "phone", "clean_data": "79319999999"},
                        "extra": {}
                    },
                    {
                        "body": {"type": "phone", "clean_data": "79319999998"},
                        "extra": {}
                    }
                ]
                
                # First search succeeds, second fails
                mock_search.side_effect = [
                    [SearchResult(first_name="Иван", user_id=1234567)],  # First call
                    Exception("Service error")  # Second call fails
                ]
                
                response = self.client.post(
                    "/api/v1/common/process",
                    json={"queries": ["79319999999", "79319999998"]}
                )
                
                # Should still return 200 with mixed results
                assert response.status_code == 200
                data = response.json()
                assert len(data) == 2
                
                # First result should be successful
                assert data[0]["body"]["results"][0]["first_name"] == "Иван"
                
                # Second result should indicate error
                assert "error" in data[1]["body"]


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])


# Running test commands:
# PYTHONPATH=. pytest tests/test_sfera.py -v
# PYTHONPATH=. pytest tests/test_sfera.py::TestDomClickService -v
# PYTHONPATH=. pytest tests/test_sfera.py::TestControllerIntegration -v
# PYTHONPATH=. pytest tests/test_sfera.py::TestHealthEndpoints -v

# Run with coverage:
# PYTHONPATH=. pytest tests/test_sfera.py --cov=./ --cov-report=html
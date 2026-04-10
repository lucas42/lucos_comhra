import pytest
from flask import Flask
import auth


@pytest.fixture
def app():
    application = Flask(__name__)
    application.config['TESTING'] = True
    application.config['SERVER_NAME'] = 'localhost'
    return application


def make_response(app):
    """Helper: return a minimal response object."""
    with app.app_context():
        from flask import Response
        return Response()


class TestSetAuthCookies:

    def test_valid_token_sets_cookie(self, app):
        """A well-formed token that is already validated gets written to the cookie."""
        token = 'abc123-valid_token'
        auth.valid_tokens.clear()
        auth.valid_tokens.append(token)
        with app.test_request_context(f'/?token={token}'):
            response = make_response(app)
            result = auth.setAuthCookies(response)
        assert 'token' in result.headers.get('Set-Cookie', '')

    def test_token_with_semicolon_rejected(self, app):
        """A token containing a semicolon (cookie-injection char) must not be set."""
        token = 'valid; SameSite=None'
        auth.valid_tokens.clear()
        auth.valid_tokens.append(token)
        with app.test_request_context(f'/?token={token}'):
            response = make_response(app)
            result = auth.setAuthCookies(response)
        assert 'Set-Cookie' not in result.headers

    def test_token_with_crlf_rejected(self, app):
        """A token containing CRLF (response-splitting char) must not be set."""
        token = 'legit\r\nSet-Cookie: evil=1'
        auth.valid_tokens.clear()
        auth.valid_tokens.append(token)
        with app.test_request_context(f'/?token=legit%0d%0aSet-Cookie%3a+evil%3d1'):
            response = make_response(app)
            result = auth.setAuthCookies(response)
        assert 'evil' not in result.headers.get('Set-Cookie', '')
        assert 'Set-Cookie' not in result.headers

    def test_no_token_in_query_string_no_cookie_set(self, app):
        """If no token query param, no cookie should be set."""
        with app.test_request_context('/'):
            response = make_response(app)
            result = auth.setAuthCookies(response)
        assert 'Set-Cookie' not in result.headers

    def test_token_already_in_cookie_not_reset(self, app):
        """If the token cookie already matches the query param, don't re-set it."""
        token = 'abc123'
        auth.valid_tokens.clear()
        auth.valid_tokens.append(token)
        with app.test_request_context(f'/?token={token}', headers={'Cookie': f'token={token}'}):
            response = make_response(app)
            result = auth.setAuthCookies(response)
        assert 'Set-Cookie' not in result.headers

    def test_unknown_token_not_set(self, app):
        """A token not in valid_tokens must not be set in a cookie, even if it looks safe."""
        auth.valid_tokens.clear()
        with app.test_request_context('/?token=unknown-token'):
            response = make_response(app)
            result = auth.setAuthCookies(response)
        assert 'Set-Cookie' not in result.headers

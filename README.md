# django_oauth_anonymous
Django authentication backend runs with OAuth2 (OAuth Tool Kit) and this authentication backend validates access token and pass User or AnonymousUser.

This authentication backend returns user if access_token is valid. Otherwise, it returns AnonymousUser rather than returnning 401 Unauthorized.

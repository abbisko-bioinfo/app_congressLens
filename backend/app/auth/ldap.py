"""LDAP authentication using ldap3 library."""

import logging

logger = logging.getLogger(__name__)


class LDAPAuthError(Exception):
    """Raised when LDAP authentication fails."""


async def authenticate_ldap(username: str, password: str) -> dict | None:
    """Authenticate a user against LDAP and return user attributes.

    Returns a dict with keys: ldap_uid, display_name, email, or None if auth fails.
    """
    try:
        import ldap3
    except ImportError:
        logger.warning("ldap3 not installed — LDAP auth unavailable")
        return None

    from app.core.config import settings

    if not settings.ldap_enabled:
        logger.info("LDAP is disabled; skipping LDAP authentication")
        return None

    server_url = settings.ldap_server
    bind_template = settings.ldap_bind_dn_template
    search_base = settings.ldap_search_base
    user_filter = settings.ldap_user_filter

    if not server_url or not bind_template:
        logger.warning("LDAP server URL or bind DN template not configured")
        return None

    bind_dn = bind_template.format(username=username)
    server = ldap3.Server(server_url, get_info=ldap3.ALL)

    try:
        conn = ldap3.Connection(server, user=bind_dn, password=password, auto_bind=True)

        if search_base:
            filter_str = user_filter.format(username=username) if user_filter else f"(sAMAccountName={username})"
            conn.search(
                search_base=search_base,
                search_filter=filter_str,
                attributes=["displayName", "mail", "sAMAccountName"],
                size_limit=1,
            )
            if conn.entries:
                entry = conn.entries[0]
                conn.unbind()
                return {
                    "ldap_uid": str(entry.sAMAccountName) if hasattr(entry, "sAMAccountName") else username,
                    "display_name": str(entry.displayName) if hasattr(entry, "displayName") else username,
                    "email": str(entry.mail) if hasattr(entry, "mail") else None,
                }

        # Fallback: return basic info without search
        conn.unbind()
        return {"ldap_uid": username, "display_name": username, "email": None}

    except ldap3.core.exceptions.LDAPBindError:
        logger.info(f"LDAP bind failed for user: {username}")
        return None
    except Exception as e:
        logger.error(f"LDAP error for user {username}: {e}")
        raise LDAPAuthError(f"LDAP authentication error: {e}") from e

# -*- coding: utf-8 -*-

"""
Copyright (C) 2019, Zato Source s.r.o. https://zato.io

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# Zato
from zato.sso import const, status_code, ValidationError
from zato.sso.password_reset import PasswordResetAPI
from zato.sso.user import Forbidden, User, UserAPI

# For pyflakes
const = const
Forbidden = Forbidden
status_code = status_code
User = User
ValidationError = ValidationError

# ################################################################################################################################

class SSOAPI(object):
    """ An object through which user management and SSO-related functionality is accessed.
    """
    def __init__(self, server, sso_conf, odb_session_func, encrypt_func, decrypt_func, hash_func, verify_hash_func,
            new_user_id_func):
        self.server = server
        self.sso_conf = sso_conf
        self.odb_session_func = odb_session_func
        self.encrypt_func = encrypt_func
        self.decrypt_func = decrypt_func
        self.hash_func = hash_func
        self.verify_hash_func = verify_hash_func
        self.new_user_id_func = new_user_id_func
        self.encrypt_email = self.sso_conf.main.encrypt_email
        self.encrypt_password = self.sso_conf.main.encrypt_password
        self.password_expiry = self.sso_conf.password.expiry

        # User management, including passwords
        self.user = UserAPI(server, sso_conf, odb_session_func, encrypt_func, decrypt_func, hash_func, verify_hash_func,
            new_user_id_func)

        # Management of Password reset tokens (PRT)
        self.password_reset = PasswordResetAPI(server, sso_conf, odb_session_func, decrypt_func, verify_hash_func)

    def post_configure(self, func, is_sqlite):
        self.odb_session_func = func
        self.user.post_configure(func, is_sqlite)
        self.password_reset.post_configure(func, is_sqlite)

# ################################################################################################################################

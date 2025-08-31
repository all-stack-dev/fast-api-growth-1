# Growth based development for Fastapi

This is the personal project of `theperfectguy`.

Following are the target for the development.

1. Yaml based environment configuration. [COMPLETED]
2. DB Connection within start.
3. BLOB Storage Connection using MINIO or BOTO3.
4. Middleware based usages.
   - Cors Middleware
   - Auth Middleware (Both for Authentication and Authorization)
   - Exception Handling Middleware
     - Authentication based Exception Handling
     - Client Exception Handling
     - Custom Exception Handling
     - Http Exception Handling
     - Payload Exception Handling
   - Request Logger Middleware
   - Session Middleware
   - Trusted Host Middleware
5. Url Structuring based on Hierarchies (Apps, Roles and Permissions).
6. Authentication Using Paseto
   - TOTP Verification Enabling
   - Reset based mails
   - Token Revocation after logout.
   - Singleton session management (Logout if multiple devices used).
7. Job Scheduling
8. Email Service
9. Websocket based system for communications.
10. Other related topics.

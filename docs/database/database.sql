-- 1. Create the database
CREATE DATABASE hamrahcel;

-- 2. Create a database user with a secure password
CREATE USER hamrahcel_user WITH PASSWORD 'sdjnnfejsajad3574nndfkd';

-- 3. Set role configurations for optimal behavior
ALTER ROLE hamrahcel_user SET client_encoding TO 'utf8';
ALTER ROLE hamrahcel_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE hamrahcel_user SET timezone TO 'UTC';

-- 4. Grant privileges to the user
GRANT CONNECT ON DATABASE hamrahcel TO hamrahcel_user;

-- 5. Set ownership and permissions carefully
ALTER DATABASE hamrahcel OWNER TO hamrahcel_user;

-- 6. Switch to the hamrahcel database for further permissions
\c hamrahcel

-- 7. Grant the user necessary permissions on the public schema
GRANT USAGE ON SCHEMA public TO hamrahcel_user;
GRANT CREATE ON SCHEMA public TO hamrahcel_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO hamrahcel_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO hamrahcel_user;

-- 8. Ensure the user gets permissions on future tables automatically
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO hamrahcel_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO hamrahcel_user;

-- 9. (Optional) Remove CREATEDB privilege if not needed
ALTER USER hamrahcel_user WITH NOCREATEDB;

-- 10. Check if the user has required privileges
SELECT has_schema_privilege('hamrahcel_user', 'public', 'CREATE');

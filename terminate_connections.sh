# Database connection details
DATABASE_URL="postgres://uzlhqkdsie5:sDgD5WQHrK3e@ep-gentle-mountain-a23bxz6h.eu-central-1.aws.neon.tech/carve_panda_mud_67225"

# Terminate connections
psql "$DATABASE_URL" -c "
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'carve_panda_mud_67225'
  AND pid <> pg_backend_pid();
"

CREATE TABLE IF NOT EXISTS "User" (
    telegram_id bigint PRIMARY KEY,
    username text,
    first_name text NOT NULL,
    last_name text,
    phone text,
    created_at timestamp with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS "Currency" (
    id serial PRIMARY KEY,
    buy jsonb NOT NULL,
    sell jsonb NOT NULL,
    created_at timestamp with time zone NOT NULL
);

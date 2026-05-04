-- schema.sql

-- 1. DROP TABLES (In reverse order of dependency)
DROP TABLE IF EXISTS strava_connections CASCADE;
DROP TABLE IF EXISTS social_comments CASCADE;
DROP TABLE IF EXISTS social_likes CASCADE;
DROP TABLE IF EXISTS friends CASCADE;
DROP TABLE IF EXISTS waterlog CASCADE;
DROP TABLE IF EXISTS foodlog CASCADE;
DROP TABLE IF EXISTS workouts CASCADE;
DROP TABLE IF EXISTS user_stats CASCADE;
DROP TABLE IF EXISTS user_profiles CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 2. CREATE USERS TABLE
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100),
    email VARCHAR(100),
    role VARCHAR(10),
    notification_status BOOLEAN DEFAULT TRUE,
    last_scheduled_email_id TEXT

);

-- 3. CREATE USER PROFILES
CREATE TABLE user_profiles (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    profile_picture_url TEXT,
    bio TEXT
);

-- 4. CREATE USER STATS
CREATE TABLE user_stats (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    age INTEGER,
    gender VARCHAR(20),
    height_cm NUMERIC(5, 2),
    current_weight_kg NUMERIC(5, 2),
    weight_goal_kg NUMERIC(5, 2),
    calorie_goal INTEGER,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_active DATE,
    steps_today INTEGER DEFAULT 0,
    salts_goal REAL,
    proteins_goal REAL,
    water_goal INTEGER
);

-- 5. CREATE WORKOUTS
CREATE TABLE workouts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50),
    calories INTEGER,
    duration INTERVAL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    source TEXT DEFAULT 'manual',
    source_activity_id BIGINT UNIQUE,
    activity_type TEXT,
    distance_km NUMERIC(10, 2),
    start_date TIMESTAMP,
    duration_seconds INTEGER,
    heart_rate INTEGER,
    elevation_gain DOUBLE PRECISION,
    steps INTEGER,
    path JSONB,
    reps INTEGER
);

-- 6. CREATE FOOD LOG
CREATE TABLE foodlog (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50),
    calories INTEGER,
    salts REAL,
    proteins REAL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    date DATE,
    mealtype TEXT
);

-- 7. CREATE WATER LOG
CREATE TABLE waterlog (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    water INTEGER,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date DATE
);

-- 8. CREATE FRIENDS (Self-referential)
CREATE TABLE friends (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    friend_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT friends_user_id_friend_id_key UNIQUE (user_id, friend_id)
);

-- 9. CREATE SOCIAL LIKES
CREATE TABLE social_likes (
    id SERIAL PRIMARY KEY,
    target_type VARCHAR(20) NOT NULL,
    target_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT social_likes_user_id_target_type_target_id_key UNIQUE (user_id, target_type, target_id),
    CONSTRAINT social_likes_target_type_check CHECK (target_type = ANY (ARRAY['workout'::text, 'meal'::text]))
);

-- 10. CREATE SOCIAL COMMENTS
CREATE TABLE social_comments (
    id SERIAL PRIMARY KEY,
    target_type VARCHAR(20) NOT NULL,
    target_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT social_comments_target_type_check CHECK (target_type = ANY (ARRAY['workout'::text, 'meal'::text]))
);

-- 11. CREATE STRAVA CONNECTIONS
CREATE TABLE strava_connections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    strava_athlete_id BIGINT NOT NULL,
    access_token TEXT NOT NULL,
    refresh_token TEXT NOT NULL,
    expires_at BIGINT NOT NULL
);
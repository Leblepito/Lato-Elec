-- ═══════════════════════════════════════════════════════════
-- ElectroPMS v5 — Database Schema
-- PostgreSQL 16
-- ═══════════════════════════════════════════════════════════

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ─── USERS & AUTH ─────────────────────────────────────────
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    full_name VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(512),
    role VARCHAR(50) NOT NULL DEFAULT 'technician',  -- admin, chief_engineer, technician, viewer
    lang VARCHAR(5) DEFAULT 'tr',  -- tr, th, en
    phone VARCHAR(50),
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE oauth_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,  -- line, facebook, google
    provider_user_id VARCHAR(255) NOT NULL,
    provider_email VARCHAR(255),
    provider_name VARCHAR(255),
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMPTZ,
    raw_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(provider, provider_user_id)
);

CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL UNIQUE,
    device_info JSONB,
    fcm_token VARCHAR(512),
    ip_address INET,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── EQUIPMENT ────────────────────────────────────────────
CREATE TABLE equipment (
    id VARCHAR(50) PRIMARY KEY,  -- PP-01, MDB, SDB-POOL etc.
    name_tr VARCHAR(255) NOT NULL,
    name_th VARCHAR(255),
    type VARCHAR(50) NOT NULL,  -- panel, pump, motor, generator, ups, pfc
    parent_id VARCHAR(50) REFERENCES equipment(id),
    location VARCHAR(255),
    specs JSONB NOT NULL DEFAULT '{}',  -- power_kw, voltage, breaker, etc.
    status VARCHAR(30) DEFAULT 'standby',
    last_reading JSONB DEFAULT '{}',  -- current, temp, vibration, etc.
    last_reading_at TIMESTAMPTZ,
    maintenance_interval_days INT DEFAULT 90,
    last_maintenance_at TIMESTAMPTZ,
    next_maintenance_at TIMESTAMPTZ,
    installed_at DATE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE equipment_readings (
    id BIGSERIAL PRIMARY KEY,
    equipment_id VARCHAR(50) NOT NULL REFERENCES equipment(id),
    reading_type VARCHAR(50) NOT NULL,  -- current, voltage, temperature, vibration, insulation, pf
    value_l1 REAL,
    value_l2 REAL,
    value_l3 REAL,
    value_avg REAL,
    unit VARCHAR(20),
    metadata JSONB DEFAULT '{}',
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── WORK ORDERS ──────────────────────────────────────────
CREATE TABLE work_orders (
    id VARCHAR(20) PRIMARY KEY,  -- WO-2026-0341
    equipment_id VARCHAR(50) REFERENCES equipment(id),
    title_tr VARCHAR(500) NOT NULL,
    title_th VARCHAR(500),
    description TEXT,
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',  -- critical, high, medium, low
    status VARCHAR(30) NOT NULL DEFAULT 'open',  -- open, accepted, in_progress, completed, cancelled
    assigned_to UUID REFERENCES users(id),
    created_by UUID REFERENCES users(id),
    accepted_at TIMESTAMPTZ,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    deadline TIMESTAMPTZ,
    estimated_hours REAL,
    actual_hours REAL,
    materials_used JSONB DEFAULT '[]',
    loto_required BOOLEAN DEFAULT false,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE work_order_photos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    work_order_id VARCHAR(20) NOT NULL REFERENCES work_orders(id) ON DELETE CASCADE,
    file_path VARCHAR(512) NOT NULL,
    thumbnail_path VARCHAR(512),
    caption VARCHAR(500),
    photo_type VARCHAR(50) DEFAULT 'documentation',  -- before, after, fault, documentation
    taken_by UUID REFERENCES users(id),
    gps_lat DOUBLE PRECISION,
    gps_lng DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── MESSAGES ─────────────────────────────────────────────
CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    channel VARCHAR(20) NOT NULL DEFAULT 'app',  -- app, line
    sender_id UUID REFERENCES users(id),
    sender_name VARCHAR(255),
    sender_type VARCHAR(30) DEFAULT 'user',  -- user, system, ai, line_bot
    message_type VARCHAR(30) DEFAULT 'text',  -- text, alarm, status, work_order, photo, file
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',  -- line_group_id, equipment_id, work_order_id
    reply_to BIGINT REFERENCES messages(id),
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── FILES ────────────────────────────────────────────────
CREATE TABLE uploaded_files (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    original_name VARCHAR(512) NOT NULL,
    stored_path VARCHAR(512) NOT NULL,
    mime_type VARCHAR(255),
    file_size BIGINT,
    file_category VARCHAR(50),  -- image, video, document, spreadsheet, cad, code, archive
    thumbnail_path VARCHAR(512),
    ai_analysis JSONB,
    ai_analyzed_at TIMESTAMPTZ,
    work_order_id VARCHAR(20) REFERENCES work_orders(id),
    equipment_id VARCHAR(50) REFERENCES equipment(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── ALERTS ───────────────────────────────────────────────
CREATE TABLE alerts (
    id BIGSERIAL PRIMARY KEY,
    equipment_id VARCHAR(50) REFERENCES equipment(id),
    alert_type VARCHAR(50) NOT NULL,  -- alarm, warning, info
    severity VARCHAR(20) NOT NULL DEFAULT 'medium',
    message_tr VARCHAR(500) NOT NULL,
    message_th VARCHAR(500),
    value REAL,
    threshold REAL,
    unit VARCHAR(20),
    acknowledged_by UUID REFERENCES users(id),
    acknowledged_at TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    auto_work_order_id VARCHAR(20) REFERENCES work_orders(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── STAFF LOCATION ───────────────────────────────────────
CREATE TABLE staff_locations (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    accuracy REAL,
    geofence_zone VARCHAR(100),
    is_inside_zone BOOLEAN,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── MAINTENANCE LOG ──────────────────────────────────────
CREATE TABLE maintenance_logs (
    id BIGSERIAL PRIMARY KEY,
    equipment_id VARCHAR(50) NOT NULL REFERENCES equipment(id),
    log_type VARCHAR(50) NOT NULL,  -- pm_daily, pm_weekly, pm_monthly, pm_quarterly, pm_semiannual, pm_annual, corrective, inspection
    performed_by UUID REFERENCES users(id),
    checklist JSONB DEFAULT '[]',
    readings JSONB DEFAULT '{}',
    notes TEXT,
    photos JSONB DEFAULT '[]',
    performed_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── LOTO RECORDS ─────────────────────────────────────────
CREATE TABLE loto_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    equipment_id VARCHAR(50) NOT NULL REFERENCES equipment(id),
    work_order_id VARCHAR(20) REFERENCES work_orders(id),
    initiated_by UUID NOT NULL REFERENCES users(id),
    steps_completed JSONB NOT NULL DEFAULT '[]',
    all_complete BOOLEAN DEFAULT false,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    released_at TIMESTAMPTZ,
    released_by UUID REFERENCES users(id)
);

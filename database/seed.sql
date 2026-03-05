-- ═══════════════════════════════════════════════════
-- ElectroPMS — Demo / Seed Data
-- ═══════════════════════════════════════════════════

-- ─── USERS (password: demo123) ────────────────────
INSERT INTO users (id, email, password_hash, full_name, role, lang, phone) VALUES
('a0000000-0000-0000-0000-000000000001', 'utku@antigravity.com', crypt('demo123', gen_salt('bf')), 'Utku (Admin)', 'admin', 'tr', '+66-xxx'),
('a0000000-0000-0000-0000-000000000002', 'somchai@hotel.com', crypt('demo123', gen_salt('bf')), 'Somchai Kaewmanee', 'technician', 'th', '+66-xxx'),
('a0000000-0000-0000-0000-000000000003', 'prasert@hotel.com', crypt('demo123', gen_salt('bf')), 'Prasert Suksawat', 'technician', 'th', '+66-xxx'),
('a0000000-0000-0000-0000-000000000004', 'wichai@hotel.com', crypt('demo123', gen_salt('bf')), 'Wichai Thongkham', 'chief_engineer', 'th', '+66-xxx');

-- ─── EQUIPMENT HIERARCHY ──────────────────────────
-- Level 0: Main
INSERT INTO equipment (id, name_tr, name_th, type, location, specs) VALUES
('MDB', 'Ana Dağıtım Panosu', 'ตู้จ่ายหลัก', 'panel', 'B1 Elektrik Odası', '{"busbar_a":1600,"breaker":"800A ACB","voltage":380,"phases":3}');

-- Level 1: Sub-distribution
INSERT INTO equipment (id, name_tr, name_th, type, parent_id, location, specs) VALUES
('SDB-GUEST', 'Misafir Katları', 'ชั้นผู้เข้าพัก', 'panel', 'MDB', 'Her kat', '{"breaker":"250A MCCB"}'),
('SDB-PLANT', 'Mekanik Oda', 'ห้องเครื่อง', 'panel', 'MDB', 'B1', '{"breaker":"400A MCCB"}'),
('SDB-POOL', 'Havuz Tesisatı', 'ระบบสระว่ายน้ำ', 'panel', 'MDB', 'Ground Floor', '{"breaker":"100A MCCB"}'),
('SDB-FIRE', 'Yangın Sistemi', 'ระบบดับเพลิง', 'panel', 'MDB', 'B1', '{"breaker":"160A MCCB"}'),
('SDB-KITCHEN', 'Mutfak', 'ครัว', 'panel', 'MDB', '1F', '{"breaker":"200A MCCB"}');

-- Level 2: Motors & Equipment
INSERT INTO equipment (id, name_tr, name_th, type, parent_id, location, specs, status) VALUES
('PP-01', 'Havuz Devir Pompası 1', 'ปั๊มหมุนเวียนสระ 1', 'pump', 'SDB-POOL', 'Havuz Makine Dairesi', '{"power_kw":11,"voltage":380,"start_method":"VFD","mccb":"32A","thermal":"18-25A","cable":"4x10mm2"}', 'running'),
('PP-02', 'Havuz Devir Pompası 2', 'ปั๊มหมุนเวียนสระ 2', 'pump', 'SDB-POOL', 'Havuz Makine Dairesi', '{"power_kw":11,"voltage":380,"start_method":"VFD","mccb":"32A","thermal":"18-25A","cable":"4x10mm2"}', 'standby'),
('SPA-01', 'Spa Jet Pompası', 'ปั๊มจ็ทสปา', 'pump', 'SDB-POOL', 'Spa Alan', '{"power_kw":5.5,"voltage":380,"start_method":"VFD"}', 'running'),
('DP-01', 'Tahliye Pompası 1', 'ปั๊มระบาย 1', 'pump', 'SDB-PLANT', 'B1 Sump', '{"power_kw":3.7,"voltage":380,"role":"lead"}', 'running'),
('DP-02', 'Tahliye Pompası 2', 'ปั๊มระบาย 2', 'pump', 'SDB-PLANT', 'B1 Sump', '{"power_kw":3.7,"voltage":380,"role":"lag"}', 'standby'),
('GEN-01', 'Jeneratör', 'เครื่องกำเนิดไฟฟ้า', 'generator', NULL, 'B1 Jeneratör Odası', '{"rating_kva":500,"fuel_type":"diesel","ats":true}', 'standby'),
('UPS-01', 'UPS Sistemi', 'ระบบ UPS', 'ups', NULL, 'B1 UPS Odası', '{"rating_kva":40,"battery_minutes":28,"type":"online_double_conversion"}', 'online'),
('PFC-01', 'Güç Faktörü Düzeltme', 'ระบบ PFC', 'pfc', 'MDB', 'B1 Elektrik Odası', '{"kvar_total":250,"steps":7,"detuned":true}', 'online');

-- MCC Starters
INSERT INTO equipment (id, name_tr, name_th, type, parent_id, location, specs, status) VALUES
('MCC-01', 'Chiller CW Pump', 'ปั๊ม CW ชิลเลอร์', 'motor', 'SDB-PLANT', 'B1 MCC', '{"power_kw":22,"mccb":"63A","thermal":"36-42A"}', 'running'),
('MCC-02', 'AHU Supply Fan', 'พัดลม AHU', 'motor', 'SDB-PLANT', 'B1 MCC', '{"power_kw":15,"mccb":"40A","thermal":"24-30A"}', 'running'),
('MCC-03', 'Fire Pump Main', 'ปั๊มดับเพลิงหลัก', 'motor', 'SDB-FIRE', 'B1 Fire Room', '{"power_kw":37,"mccb":"100A","thermal":"58-68A"}', 'standby'),
('MCC-04', 'Jockey Pump', 'ปั๊มจ็อคกี้', 'motor', 'SDB-FIRE', 'B1 Fire Room', '{"power_kw":2.2,"mccb":"10A","thermal":"3.8-5A"}', 'running');

-- ─── SAMPLE WORK ORDERS ───────────────────────────
INSERT INTO work_orders (id, equipment_id, title_tr, title_th, priority, status, assigned_to, created_by, deadline) VALUES
('WO-2026-0341', 'PP-01', 'Termik Röle Ayar Kontrolü', 'ตรวจสอบการตั้งค่าเทอร์มอลรีเลย์', 'high', 'open', 'a0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000001', NOW() + INTERVAL '12 hours'),
('WO-2026-0342', 'MDB', 'Termografik Tarama Q1', 'สแกนเทอร์โมกราฟี Q1', 'medium', 'in_progress', 'a0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000001', NOW() + INTERVAL '2 days'),
('WO-2026-0343', 'GEN-01', 'Jeneratör Aylık Yük Testi', 'ทดสอบโหลดเครื่องกำเนิดไฟฟ้ารายเดือน', 'medium', 'scheduled', 'a0000000-0000-0000-0000-000000000004', 'a0000000-0000-0000-0000-000000000001', NOW() + INTERVAL '7 days');

-- ─── SAMPLE MESSAGES ──────────────────────────────
INSERT INTO messages (channel, sender_id, sender_name, sender_type, message_type, content) VALUES
('line', 'a0000000-0000-0000-0000-000000000002', 'Somchai', 'user', 'status', 'PP-01 çalıştırıldı, akım 21.5A normal'),
('line', NULL, 'System', 'system', 'alarm', '[ALARM] MDB PF düşük: 0.84 — PFC kademe artırıldı'),
('app', 'a0000000-0000-0000-0000-000000000001', 'Utku', 'user', 'text', 'Havuz pompası 2 bakım tarihi ne zaman?'),
('app', NULL, 'AI', 'ai', 'text', 'PP-02 son bakım: 20 Ocak 2026. Sonraki: 20 Nisan 2026.');

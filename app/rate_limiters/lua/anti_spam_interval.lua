local key = KEYS[1]
local min_interval = tonumber(ARGV[1])          
local ttl_seconds = tonumber(ARGV[2]) or 300    

-- ВАЖНО: время получаем прямо на сервере Redis
local redis_current_time = redis.time()
local now = redis_current_time[1] + (redis_current_time[2] / 1000000)
-- redis.time() возвращает {сек, микросек}. Нам нужна float‑секунда.

local last_time_raw = redis.call('GET', key)

if not last_time_raw then
    -- Первый запрос: разрешаем, ставим время и TTL
    redis.call('SET', key, now, 'EX', ttl_seconds)
    return {true, 0}
end

local last_time = tonumber(last_time_raw)

-- Защита на случай, если last_time каким‑то образом стал nil или некорректным
if not last_time then
    redis.call('SET', key, now, 'EX', ttl_seconds)
    return {true, 0}
end

local delta = now - last_time

if delta < min_interval then
    local wait_time = min_interval - delta
    -- Возвращаем false и сколько ждать (в секундах, float)
    return {false, wait_time}
else
    -- Разрешаем, обновляем время и продлеваем TTL
    redis.call('SET', key, now, 'EX', ttl_seconds)
    return {true, 0}
end

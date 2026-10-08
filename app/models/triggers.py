from sqlalchemy import DDL


create_reviews_rating_trigger = DDL(
    """
    CREATE OR REPLACE FUNCTION recalc_product_rating()
    RETURNS TRIGGER AS $$
    DECLARE
        target_product_id BIGINT;
        avg_grade DOUBLE PRECISION;
        review_count INTEGER;
    BEGIN
        -- INSERT: просто пересчитываем для нового product_id
        IF (TG_OP = 'INSERT') THEN
            target_product_id := NEW.product_id;

        -- DELETE: пересчитываем для product_id удалённой записи
        ELSIF (TG_OP = 'DELETE') THEN
            target_product_id := OLD.product_id;

        -- UPDATE: пересчитываем ТОЛЬКО если изменились product_id, grade или is_active
        ELSIF (TG_OP = 'UPDATE') THEN
            IF  (NEW.product_id IS DISTINCT FROM OLD.product_id)
            OR (NEW.grade     IS DISTINCT FROM OLD.grade)
            OR (NEW.is_active IS DISTINCT FROM OLD.is_active)
            THEN
                -- Если product_id сменился — нужно пересчитать и старый, и новый
                IF NEW.product_id IS DISTINCT FROM OLD.product_id THEN
                    -- пересчёт для старого product_id
                    SELECT AVG(grade), COUNT(*)
                    INTO avg_grade, review_count
                    FROM reviews
                    WHERE product_id = OLD.product_id AND is_active = TRUE;

                    UPDATE products
                    SET rating = COALESCE(avg_grade, 0), reviews_count = COALESCE(review_count, 0)
                    WHERE id = OLD.product_id;
                END IF;

                target_product_id := NEW.product_id;
            ELSE
                -- Ничего важного не поменялось — триггер молчит
                RETURN NULL;
            END IF;
        END IF;

        -- Основной пересчёт для target_product_id
        SELECT AVG(grade), COUNT(*)
        INTO avg_grade, review_count
        FROM reviews
        WHERE product_id = target_product_id AND is_active = TRUE;

        UPDATE products
        SET rating       = COALESCE(avg_grade, 0),
            reviews_count = COALESCE(review_count, 0)
        WHERE id = target_product_id;

        RETURN NULL;
    END;
    $$ LANGUAGE plpgsql;

    -- Удаляем старый триггер, если был
    DROP TRIGGER IF EXISTS reviews_rating_trigger ON reviews;

    -- Создаём триггер на все три операции
    CREATE TRIGGER reviews_rating_trigger
        AFTER INSERT OR UPDATE OR DELETE ON reviews
        FOR EACH ROW
        EXECUTE FUNCTION recalc_product_rating();
    """
)

drop_reviews_rating_trigger = DDL(
    """
    DROP TRIGGER IF EXISTS reviews_rating_trigger ON reviews;
    DROP FUNCTION IF EXISTS recalc_product_rating();
    """
)

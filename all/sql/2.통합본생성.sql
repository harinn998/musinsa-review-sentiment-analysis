-- 통합 products
CREATE TABLE products_all AS
SELECT * FROM filluminate_products_001
UNION ALL
SELECT * FROM filluminate_products_002
UNION ALL
SELECT * FROM filluminate_products_003
UNION ALL
SELECT * FROM travel_products_001
UNION ALL
SELECT * FROM travel_products_002
UNION ALL
SELECT * FROM travel_products_003
UNION ALL
SELECT * FROM jemut_products_001
UNION ALL
SELECT * FROM jemut_products_002
UNION ALL
SELECT * FROM jemut_products_003;

-- 통합 reviews
CREATE TABLE reviews_all AS
SELECT * FROM filluminate_reviews_001
UNION ALL
SELECT * FROM filluminate_reviews_002
UNION ALL
SELECT * FROM filluminate_reviews_003
UNION ALL
SELECT * FROM travel_reviews_001
UNION ALL
SELECT * FROM travel_reviews_002
UNION ALL
SELECT * FROM travel_reviews_003
UNION ALL
SELECT * FROM jemut_reviews_001
UNION ALL
SELECT * FROM jemut_reviews_002
UNION ALL
SELECT * FROM jemut_reviews_003;
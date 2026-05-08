USE review_analysis;

-- DROP TABLE IF EXISTS survey_001, survey_002, survey_003;
-- DROP TABLE IF EXISTS reviews_001, reviews_002, reviews_003;
-- DROP TABLE IF EXISTS products_001, products_002, products_003;
-- drop table if exists products_all, reviews_all;

-- filluminate
CREATE TABLE filluminate_products_001 (
    goodsNo     BIGINT PRIMARY KEY,
    플랫폼        VARCHAR(50),
    카테고리       VARCHAR(100),
    브랜드        VARCHAR(100),
    상품명        VARCHAR(500),
    정가         BIGINT,
    판매가        BIGINT,
    할인율        BIGINT,
    조회수        BIGINT,
    누적판매수      BIGINT,
    리뷰수        BIGINT,
    리뷰점수       BIGINT,
    판매상태       VARCHAR(20)
);
CREATE TABLE filluminate_reviews_001 (
    리뷰번호    BIGINT PRIMARY KEY,
    goodsNo  BIGINT,
    리뷰타입    VARCHAR(50),
    작성자     VARCHAR(100),
    리뷰내용    TEXT,
    평점       BIGINT,
    체험단    VARCHAR(10),
    구매옵션    VARCHAR(200),
    키        BIGINT,
    몸무게     BIGINT,
    성별       VARCHAR(10),
    작성일     VARCHAR(50),
    만족도     VARCHAR(200),
    사진유무    VARCHAR(10),
    도움돼요    BIGINT,
    FOREIGN KEY (goodsNo) REFERENCES filluminate_products_001(goodsNo)
);

CREATE TABLE filluminate_products_002 (
    goodsNo     BIGINT PRIMARY KEY,
    플랫폼        VARCHAR(50),
    카테고리       VARCHAR(100),
    브랜드        VARCHAR(100),
    상품명        VARCHAR(500),
    정가         BIGINT,
    판매가        BIGINT,
    할인율        BIGINT,
    조회수        BIGINT,
    누적판매수      BIGINT,
    리뷰수        BIGINT,
    리뷰점수       BIGINT,
    판매상태        VARCHAR(20)
);
CREATE TABLE filluminate_reviews_002 (
    리뷰번호    BIGINT PRIMARY KEY,
    goodsNo  BIGINT,
    리뷰타입    VARCHAR(50),
    작성자     VARCHAR(100),
    리뷰내용    TEXT,
    평점       BIGINT,
    체험단    VARCHAR(10),
    구매옵션    VARCHAR(200),
    키        BIGINT,
    몸무게     BIGINT,
    성별       VARCHAR(10),
    작성일     VARCHAR(50),
    만족도     VARCHAR(200),
    사진유무    VARCHAR(10),
    도움돼요    BIGINT,
    FOREIGN KEY (goodsNo) REFERENCES filluminate_products_002(goodsNo)
);

CREATE TABLE filluminate_products_003 (
    goodsNo     BIGINT PRIMARY KEY,
    플랫폼        VARCHAR(50),
    카테고리       VARCHAR(100),
    브랜드        VARCHAR(100),
    상품명        VARCHAR(500),
    정가         BIGINT,
    판매가        BIGINT,
    할인율        BIGINT,
    조회수        BIGINT,
    누적판매수      BIGINT,
    리뷰수        BIGINT,
    리뷰점수       BIGINT,
    판매상태        VARCHAR(20)
);
CREATE TABLE filluminate_reviews_003 (
    리뷰번호    BIGINT PRIMARY KEY,
    goodsNo  BIGINT,
    리뷰타입    VARCHAR(50),
    작성자     VARCHAR(100),
    리뷰내용    TEXT,
    평점       BIGINT,
    체험단    VARCHAR(10),
    구매옵션    VARCHAR(200),
    키        BIGINT,
    몸무게     BIGINT,
    성별       VARCHAR(10),
    작성일     VARCHAR(50),
    만족도     VARCHAR(200),
    사진유무    VARCHAR(10),
    도움돼요    BIGINT,
    FOREIGN KEY (goodsNo) REFERENCES filluminate_products_003(goodsNo)
);

-- travel
CREATE TABLE travel_products_001 (
    goodsNo     BIGINT PRIMARY KEY,
    플랫폼        VARCHAR(50),
    카테고리       VARCHAR(100),
    브랜드        VARCHAR(100),
    상품명        VARCHAR(500),
    정가         BIGINT,
    판매가        BIGINT,
    할인율        BIGINT,
    조회수        BIGINT,
    누적판매수      BIGINT,
    리뷰수        BIGINT,
    리뷰점수       BIGINT,
    판매상태        VARCHAR(20)
);
CREATE TABLE travel_reviews_001 (
    리뷰번호    BIGINT PRIMARY KEY,
    goodsNo  BIGINT,
    리뷰타입    VARCHAR(50),
    작성자     VARCHAR(100),
    리뷰내용    TEXT,
    평점       BIGINT,
    체험단    VARCHAR(10),
    구매옵션    VARCHAR(200),
    키        BIGINT,
    몸무게     BIGINT,
    성별       VARCHAR(10),
    작성일     VARCHAR(50),
    만족도     VARCHAR(200),
    사진유무    VARCHAR(10),
    도움돼요    BIGINT,
    FOREIGN KEY (goodsNo) REFERENCES travel_products_001(goodsNo)
);

CREATE TABLE travel_products_002 (
    goodsNo     BIGINT PRIMARY KEY,
    플랫폼        VARCHAR(50),
    카테고리       VARCHAR(100),
    브랜드        VARCHAR(100),
    상품명        VARCHAR(500),
    정가         BIGINT,
    판매가        BIGINT,
    할인율        BIGINT,
    조회수        BIGINT,
    누적판매수      BIGINT,
    리뷰수        BIGINT,
    리뷰점수       BIGINT,
    판매상태        VARCHAR(20)
);
CREATE TABLE travel_reviews_002 (
    리뷰번호    BIGINT PRIMARY KEY,
    goodsNo  BIGINT,
    리뷰타입    VARCHAR(50),
    작성자     VARCHAR(100),
    리뷰내용    TEXT,
    평점       BIGINT,
    체험단    VARCHAR(10),
    구매옵션    VARCHAR(200),
    키        BIGINT,
    몸무게     BIGINT,
    성별       VARCHAR(10),
    작성일     VARCHAR(50),
    만족도     VARCHAR(200),
    사진유무    VARCHAR(10),
    도움돼요    BIGINT,
    FOREIGN KEY (goodsNo) REFERENCES travel_products_002(goodsNo)
);

CREATE TABLE travel_products_003 (
    goodsNo     BIGINT PRIMARY KEY,
    플랫폼        VARCHAR(50),
    카테고리       VARCHAR(100),
    브랜드        VARCHAR(100),
    상품명        VARCHAR(500),
    정가         BIGINT,
    판매가        BIGINT,
    할인율        BIGINT,
    조회수        BIGINT,
    누적판매수      BIGINT,
    리뷰수        BIGINT,
    리뷰점수       BIGINT,
    판매상태        VARCHAR(20)
);
CREATE TABLE travel_reviews_003 (
    리뷰번호    BIGINT PRIMARY KEY,
    goodsNo  BIGINT,
    리뷰타입    VARCHAR(50),
    작성자     VARCHAR(100),
    리뷰내용    TEXT,
    평점       BIGINT,
    체험단    VARCHAR(10),
    구매옵션    VARCHAR(200),
    키        BIGINT,
    몸무게     BIGINT,
    성별       VARCHAR(10),
    작성일     VARCHAR(50),
    만족도     VARCHAR(200),
    사진유무    VARCHAR(10),
    도움돼요    BIGINT,
    FOREIGN KEY (goodsNo) REFERENCES travel_products_003(goodsNo)
);

-- jemut
CREATE TABLE jemut_products_001 (
    goodsNo     BIGINT PRIMARY KEY,
    플랫폼        VARCHAR(50),
    카테고리       VARCHAR(100),
    브랜드        VARCHAR(100),
    상품명        VARCHAR(500),
    정가         BIGINT,
    판매가        BIGINT,
    할인율        BIGINT,
    조회수        BIGINT,
    누적판매수      BIGINT,
    리뷰수        BIGINT,
    리뷰점수       BIGINT,
    판매상태        VARCHAR(20)
);
CREATE TABLE jemut_reviews_001 (
    리뷰번호    BIGINT PRIMARY KEY,
    goodsNo  BIGINT,
    리뷰타입    VARCHAR(50),
    작성자     VARCHAR(100),
    리뷰내용    TEXT,
    평점       BIGINT,
    체험단    VARCHAR(10),
    구매옵션    VARCHAR(200),
    키        BIGINT,
    몸무게     BIGINT,
    성별       VARCHAR(10),
    작성일     VARCHAR(50),
    만족도     VARCHAR(200),
    사진유무    VARCHAR(10),
    도움돼요    BIGINT,
    FOREIGN KEY (goodsNo) REFERENCES jemut_products_001(goodsNo)
);

CREATE TABLE jemut_products_002 (
    goodsNo     BIGINT PRIMARY KEY,
    플랫폼        VARCHAR(50),
    카테고리       VARCHAR(100),
    브랜드        VARCHAR(100),
    상품명        VARCHAR(500),
    정가         BIGINT,
    판매가        BIGINT,
    할인율        BIGINT,
    조회수        BIGINT,
    누적판매수      BIGINT,
    리뷰수        BIGINT,
    리뷰점수       BIGINT,
    판매상태        VARCHAR(20)
);
CREATE TABLE jemut_reviews_002 (
    리뷰번호    BIGINT PRIMARY KEY,
    goodsNo  BIGINT,
    리뷰타입    VARCHAR(50),
    작성자     VARCHAR(100),
    리뷰내용    TEXT,
    평점       BIGINT,
    체험단    VARCHAR(10),
    구매옵션    VARCHAR(200),
    키        BIGINT,
    몸무게     BIGINT,
    성별       VARCHAR(10),
    작성일     VARCHAR(50),
    만족도     VARCHAR(200),
    사진유무    VARCHAR(10),
    도움돼요    BIGINT,
    FOREIGN KEY (goodsNo) REFERENCES jemut_products_002(goodsNo)
);

CREATE TABLE jemut_products_003 (
    goodsNo     BIGINT PRIMARY KEY,
    플랫폼        VARCHAR(50),
    카테고리       VARCHAR(100),
    브랜드        VARCHAR(100),
    상품명        VARCHAR(500),
    정가         BIGINT,
    판매가        BIGINT,
    할인율        BIGINT,
    조회수        BIGINT,
    누적판매수      BIGINT,
    리뷰수        BIGINT,
    리뷰점수       BIGINT,
    판매상태        VARCHAR(20)
);
CREATE TABLE jemut_reviews_003 (
    리뷰번호    BIGINT PRIMARY KEY,
    goodsNo  BIGINT,
    리뷰타입    VARCHAR(50),
    작성자     VARCHAR(100),
    리뷰내용    TEXT,
    평점       BIGINT,
    체험단    VARCHAR(10),
    구매옵션    VARCHAR(200),
    키        BIGINT,
    몸무게     BIGINT,
    성별       VARCHAR(10),
    작성일     VARCHAR(50),
    만족도     VARCHAR(200),
    사진유무    VARCHAR(10),
    도움돼요    BIGINT,
    FOREIGN KEY (goodsNo) REFERENCES jemut_products_003(goodsNo)
);
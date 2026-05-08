CREATE VIEW products_reviews_all AS
SELECT 
    p.goodsNo,
    p.플랫폼,
    p.카테고리,
    p.브랜드,
    p.상품명,
    p.정가,
    p.판매가,
    p.할인율,
    p.조회수,
    p.누적판매수,
    p.리뷰수,
    p.리뷰점수,
    r.리뷰번호,
    r.작성자,
    r.리뷰내용,
    r.평점,
    r.체험단,
    r.구매옵션,
    r.키,
    r.몸무게,
    r.성별,
    r.작성일,
    r.만족도,
    r.사진유무,
    r.도움돼요
FROM products_all p
LEFT JOIN reviews_all r ON p.goodsNo = r.goodsNo;
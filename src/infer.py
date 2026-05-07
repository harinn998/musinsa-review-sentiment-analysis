"""
이번 주 신규 리뷰에 대해 임베딩 + 토픽 할당 + 감성 분석.

입력:
    data/weekly_new.csv         - preprocess.py가 만든 이번 주 신규 정제 리뷰
    models/03_umap_model.pkl    - 학습된 UMAP (5.97GB)
    models/05_hdbscan_model.pkl - 학습된 HDBSCAN (95MB)
    models/06_topic_keywords_display.csv - topic_id ↔ 키워드 매핑

출력:
    outputs/weekly_results.csv  - Tableau 업로드용
"""

import gc
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSequenceClassification

import hdbscan  # approximate_predict


# ═══════════════════════════════════════════════════════════
# 설정
# ═══════════════════════════════════════════════════════════
EMBEDDING_MODEL = 'jhgan/ko-sroberta-multitask'
SENTIMENT_MODEL = 'nlp04/korean_sentiment_analysis_kcelectra'

# KcELECTRA 11개 emotion → 3-class 매핑 (Step 7-3a 노트북 기준)
KCELECTRA_POSITIVE = {
    '기쁨(행복한)', '고마운', '설레는(기대하는)',
    '사랑하는', '즐거운(신나는)',
}
KCELECTRA_NEGATIVE = {
    '슬픔(우울한)', '힘듦(지침)', '짜증남', '걱정스러운(불안한)',
}
KCELECTRA_NEUTRAL = {
    '일상적인', '생각이 많은',
}

# Step 7-3c human validation으로 결정된 threshold
SENTIMENT_THRESHOLD = 0.60

# 토픽 키워드 표시 시 상위 N개
TOPIC_TOP_N = 5


# ═══════════════════════════════════════════════════════════
# 임베딩
# ═══════════════════════════════════════════════════════════
def embed_texts(texts, batch_size=32):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"  device: {device}", flush=True)
    model = SentenceTransformer(EMBEDDING_MODEL, device=device)
    embeddings = model.encode(
        texts, batch_size=batch_size, show_progress_bar=False,
        convert_to_numpy=True, normalize_embeddings=False,
    )
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()
    return embeddings


# ═══════════════════════════════════════════════════════════
# UMAP (5.97GB 모델 로드 후 transform)
# ═══════════════════════════════════════════════════════════
def umap_transform(embeddings, umap_path):
    print(f"  UMAP 모델 로드 중 (~5.97GB, 1~3분 소요)...", flush=True)
    with open(umap_path, 'rb') as f:
        umap_model = pickle.load(f)
    print(f"  UMAP transform...", flush=True)
    umap_emb = umap_model.transform(embeddings)
    del umap_model
    gc.collect()
    return umap_emb


# ═══════════════════════════════════════════════════════════
# HDBSCAN approximate_predict
# ═══════════════════════════════════════════════════════════
def assign_topics(umap_emb, hdbscan_path):
    print(f"  HDBSCAN 모델 로드 중...", flush=True)
    with open(hdbscan_path, 'rb') as f:
        hdbscan_model = pickle.load(f)
    labels, strengths = hdbscan.approximate_predict(hdbscan_model, umap_emb)
    del hdbscan_model
    gc.collect()
    return labels, strengths


# ═══════════════════════════════════════════════════════════
# 토픽 키워드 매핑 (long → wide)
# ═══════════════════════════════════════════════════════════
def load_topic_keywords(csv_path, top_n=5):
    """
    long format → {topic_id: 'kw1, kw2, ..., kwN'} dict 변환.
    csv 컬럼: topic_id, topic_size, rank, word, category, ctfidf_score
    """
    df = pd.read_csv(csv_path)
    grouped = (
        df.sort_values(['topic_id', 'rank'])
          .groupby('topic_id')['word']
          .apply(lambda s: ', '.join(s.head(top_n).astype(str)))
    )
    return grouped.to_dict()


# ═══════════════════════════════════════════════════════════
# 감성 분석 (KcELECTRA + threshold 0.60)
# ═══════════════════════════════════════════════════════════
def analyze_sentiment(texts, batch_size=32, max_length=128):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"  device: {device}", flush=True)

    tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL).to(device)
    model.eval()

    id2label = model.config.id2label

    def label_to_group(label):
        if label in KCELECTRA_POSITIVE: return 'positive'
        if label in KCELECTRA_NEGATIVE: return 'negative'
        return 'neutral'

    sentiments, confidences = [], []

    with torch.no_grad():
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            inputs = tokenizer(batch, padding=True, truncation=True,
                               max_length=max_length, return_tensors='pt')
            inputs = {k: v.to(device) for k, v in inputs.items()}
            probs = torch.softmax(model(**inputs).logits, dim=-1).cpu().numpy()

            for prob_row in probs:
                # 11개 → 3 그룹 확률 합산
                gp = {'positive': 0.0, 'negative': 0.0, 'neutral': 0.0}
                for idx, label in id2label.items():
                    gp[label_to_group(label)] += float(prob_row[idx])

                # threshold 적용: max(p_pos, p_neg) >= 0.60 이면 모델 예측, 아니면 neutral
                max_pn = max(gp['positive'], gp['negative'])
                if max_pn >= SENTIMENT_THRESHOLD:
                    sent = 'positive' if gp['positive'] >= gp['negative'] else 'negative'
                    conf = max_pn
                else:
                    sent = 'neutral'
                    conf = gp['neutral']

                sentiments.append(sent)
                confidences.append(round(conf, 4))

    del model, tokenizer
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()

    return sentiments, confidences


# ═══════════════════════════════════════════════════════════
# 메인 진입점
# ═══════════════════════════════════════════════════════════
def run_inference(data_dir, models_dir, outputs_dir):
    data_dir = Path(data_dir)
    models_dir = Path(models_dir)
    outputs_dir = Path(outputs_dir)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    weekly_new = data_dir / "weekly_new.csv"

    if not weekly_new.exists():
        print("  weekly_new.csv 없음 → 추론 스킵", flush=True)
        return 0

    print(f"\n[1/5] 데이터 로드", flush=True)
    df = pd.read_csv(weekly_new)
    text_col = '리뷰내용_clean' if '리뷰내용_clean' in df.columns else '리뷰내용'
    df = df[df[text_col].notna() & (df[text_col].astype(str).str.len() > 0)].reset_index(drop=True)
    print(f"  대상 리뷰: {len(df):,}건", flush=True)

    if len(df) == 0:
        print("  추론할 리뷰 없음", flush=True)
        return 0

    texts = df[text_col].astype(str).tolist()

    print(f"\n[2/5] 임베딩", flush=True)
    embeddings = embed_texts(texts)
    print(f"  shape: {embeddings.shape}", flush=True)

    print(f"\n[3/5] UMAP 차원 축소", flush=True)
    umap_emb = umap_transform(embeddings, models_dir / "03_umap_model.pkl")
    print(f"  shape: {umap_emb.shape}", flush=True)
    del embeddings
    gc.collect()

    print(f"\n[4/5] HDBSCAN 토픽 할당", flush=True)
    labels, strengths = assign_topics(umap_emb, models_dir / "05_hdbscan_model.pkl")
    n_out = int((labels == -1).sum())
    print(f"  토픽 할당: {len(labels) - n_out:,}건 / outlier: {n_out:,}건", flush=True)
    del umap_emb
    gc.collect()

    topic_kw_map = load_topic_keywords(
        models_dir / "06_topic_keywords_display.csv", top_n=TOPIC_TOP_N
    )
    df['topic_id'] = labels
    df['topic_strength'] = np.round(strengths, 4)
    df['topic_keywords'] = df['topic_id'].map(topic_kw_map).fillna('(outlier)')

    print(f"\n[5/5] 감성 분석 (KcELECTRA, threshold {SENTIMENT_THRESHOLD})", flush=True)
    sentiments, confidences = analyze_sentiment(texts)
    df['sentiment'] = sentiments
    df['sentiment_confidence'] = confidences

    # Tableau에 보낼 컬럼만 선별
    keep_cols = [
        '리뷰번호', '작성일', '브랜드', '카테고리', 'goodsNo',
        text_col,
        'topic_id', 'topic_keywords', 'topic_strength',
        'sentiment', 'sentiment_confidence',
    ]
    keep_cols = [c for c in keep_cols if c in df.columns]

    out_path = outputs_dir / "weekly_results.csv"
    df[keep_cols].to_csv(out_path, index=False, encoding='utf-8-sig')

    print(f"\n✓ 결과 저장: {out_path}", flush=True)
    print(f"  감성 분포: {pd.Series(sentiments).value_counts().to_dict()}", flush=True)
    return len(df)


if __name__ == "__main__":
    run_inference(Path("data"), Path("models"), Path("outputs"))

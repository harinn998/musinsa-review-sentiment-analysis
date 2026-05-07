"""
Step 3 임베딩 입력 parquet 생성:
weekly_new_step2_dedup.csv → embedding_input.parquet
"""

from pathlib import Path
import pandas as pd

GROUP_A = ['리뷰번호', '리뷰내용_clean']
GROUP_B = ['goodsNo', '리뷰타입', '평점', '작성일']
GROUP_C = [
    '사이즈', '화면대비색감', '퀄리티', '구김',
    '두께감', '신축성', '색감', '보온성',
    '퀄리티_점수', '보온성_점수', '신축성_점수', '두께감_점수', '구김_점수',
    '사이즈_편차절대', '화면대비색감_편차절대', '색감_편차절대',
    '만족도_응답여부',
    'laugh_count', 'cry_count', 'exclamation_count',
    'question_count', 'emoji_count',
    'has_repetition', 'text_length_orig',
]
GROUP_D = ['성별', '구매사이즈', '구매상세', '사진유무', '체험단']
EXTRA   = ['브랜드', '카테고리']   # 대시보드 분석용으로 추가 보존


def run_extract(data_dir: str = "data") -> int:
    data_dir = Path(data_dir)
    input_path = data_dir / "weekly_new_step2_dedup.csv"
    output_path = data_dir / "embedding_input.parquet"

    if not input_path.exists():
        print("  weekly_new_step2_dedup.csv 없음 → parquet 생성 스킵", flush=True)
        if output_path.exists():
            output_path.unlink()
        return 0

    df = pd.read_csv(input_path, low_memory=False)

    if 'is_valid_for_topic' not in df.columns:
        print("  ⚠️ is_valid_for_topic 컬럼 없음", flush=True)
        return 0

    df_valid = df[df['is_valid_for_topic'] == True].copy().reset_index(drop=True)

    selected = GROUP_A + GROUP_B + GROUP_C + GROUP_D + EXTRA
    existing = [c for c in selected if c in df_valid.columns]
    missing  = [c for c in selected if c not in df_valid.columns]

    if missing:
        print(f"  누락 컬럼 ({len(missing)}개): {missing[:5]}{'...' if len(missing) > 5 else ''}", flush=True)

    df_valid[existing].to_parquet(output_path, index=False, engine='pyarrow')

    size_kb = output_path.stat().st_size / 1024
    print(f"  parquet 저장: {len(df_valid):,}건, {size_kb:.1f} KB", flush=True)
    return len(df_valid)

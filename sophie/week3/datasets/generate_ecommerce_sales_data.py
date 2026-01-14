"""
온라인 쇼핑몰 의류 매출 더미 데이터 생성 스크립트

Prophet 시계열 예측 튜토리얼을 위한 교육용 데이터셋 생성
- 비즈니스 시나리오: 온라인 쇼핑몰 의류 카테고리 매출 예측
- 데이터 기간: 2년 (730일)
- 포함 요소: 추세, 계절성, 이벤트, 외부변수(기온), 노이즈
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# 재현성을 위한 시드 설정
np.random.seed(42)


def generate_date_range(start_date: str, days: int) -> pd.DatetimeIndex:
    """날짜 범위 생성"""
    return pd.date_range(start=start_date, periods=days, freq='D')


def generate_trend(dates: pd.DatetimeIndex,
                   base_sales: float = 5_000_000,
                   annual_growth_rate: float = 0.15,
                   changepoint_date: str = "2023-06-15",
                   changepoint_multiplier: float = 2.0) -> np.ndarray:
    """
    추세 생성 (기본 성장 + changepoint)
    """
    n_days = len(dates)
    daily_growth_rate = annual_growth_rate / 365

    trend = np.zeros(n_days)
    changepoint = pd.Timestamp(changepoint_date)

    for i, date in enumerate(dates):
        days_from_start = i
        if date < changepoint:
            trend[i] = base_sales * (1 + daily_growth_rate * days_from_start)
        else:
            days_before_cp = (changepoint - dates[0]).days
            base_at_cp = base_sales * (1 + daily_growth_rate * days_before_cp)
            days_after_cp = (date - changepoint).days
            trend[i] = base_at_cp * (1 + daily_growth_rate * changepoint_multiplier * days_after_cp)

    return trend


def generate_weekly_seasonality(dates: pd.DatetimeIndex) -> np.ndarray:
    """주간 계절성 생성"""
    weekly_effects = {0: -0.10, 1: 0.00, 2: 0.00, 3: 0.00, 4: 0.15, 5: 0.25, 6: 0.10}
    return np.array([weekly_effects[d.dayofweek] for d in dates])


def generate_yearly_seasonality(dates: pd.DatetimeIndex) -> np.ndarray:
    """연간 계절성 생성 (의류 특화)"""
    def get_yearly_effect(date):
        month = date.month
        if month in [3, 4, 5]: return 0.05
        elif month in [6, 7, 8]: return -0.15
        elif month in [9, 10, 11]: return 0.10
        else: return 0.20
    return np.array([get_yearly_effect(d) for d in dates])


def generate_events(start_date: str, end_date: str) -> pd.DataFrame:
    """비즈니스 이벤트 생성"""
    events = []
    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)

    for year in range(start.year, end.year + 1):
        # 신년세일
        new_year = pd.Timestamp(f"{year}-01-01")
        if start <= new_year <= end:
            events.append({'holiday': 'new_year_sale', 'ds': new_year, 'lower_window': 0, 'upper_window': 4, 'effect': 0.40})

        # 여름세일
        summer_sale = pd.Timestamp(f"{year}-07-01")
        if start <= summer_sale <= end:
            events.append({'holiday': 'summer_sale', 'ds': summer_sale, 'lower_window': 0, 'upper_window': 6, 'effect': 0.50})

        # 블랙프라이데이
        nov_first = pd.Timestamp(f"{year}-11-01")
        days_until_friday = (4 - nov_first.dayofweek) % 7
        first_friday = nov_first + timedelta(days=days_until_friday)
        black_friday = first_friday + timedelta(weeks=3)
        if start <= black_friday <= end:
            events.append({'holiday': 'black_friday', 'ds': black_friday, 'lower_window': 0, 'upper_window': 2, 'effect': 0.80})

        # 신규상품 출시
        for month in [2, 5, 8, 11]:
            launch_date = pd.Timestamp(f"{year}-{month:02d}-15")
            if start <= launch_date <= end:
                events.append({'holiday': 'new_product_launch', 'ds': launch_date, 'lower_window': 0, 'upper_window': 4, 'effect': 0.30})

        # 재고부족
        for stock_out in [pd.Timestamp(f"{year}-03-20"), pd.Timestamp(f"{year}-08-10"), pd.Timestamp(f"{year}-12-05")]:
            if start <= stock_out <= end:
                events.append({'holiday': 'stock_shortage', 'ds': stock_out, 'lower_window': 0, 'upper_window': 2, 'effect': -0.30})

        # 시스템 점검
        for month in [4, 10]:
            first_day = pd.Timestamp(f"{year}-{month:02d}-01")
            days_until_sunday = (6 - first_day.dayofweek) % 7
            maintenance_day = first_day + timedelta(days=days_until_sunday)
            if start <= maintenance_day <= end:
                events.append({'holiday': 'system_maintenance', 'ds': maintenance_day, 'lower_window': 0, 'upper_window': 0, 'effect': -0.50})

    return pd.DataFrame(events)


def apply_event_effects(dates: pd.DatetimeIndex, events_df: pd.DataFrame) -> np.ndarray:
    """이벤트 효과를 날짜별로 적용"""
    effects = np.zeros(len(dates))
    date_to_idx = {date: idx for idx, date in enumerate(dates)}

    for _, event in events_df.iterrows():
        event_date = event['ds']
        lower = event['lower_window']
        upper = event['upper_window']
        effect = event['effect']

        for offset in range(-lower, upper + 1):
            target_date = event_date + timedelta(days=offset)
            if target_date in date_to_idx:
                idx = date_to_idx[target_date]
                decay = 1.0 - (abs(offset) / (abs(lower) + abs(upper) + 1)) * 0.5
                effects[idx] += effect * decay

    return effects


def generate_temperature(dates: pd.DatetimeIndex) -> np.ndarray:
    """한국 기온 데이터 생성"""
    monthly_avg_temp = {1: -2, 2: 0, 3: 6, 4: 13, 5: 18, 6: 23, 7: 26, 8: 27, 9: 22, 10: 15, 11: 7, 12: 0}
    temps = []
    for date in dates:
        base_temp = monthly_avg_temp[date.month]
        daily_variation = np.random.normal(0, 2.5)
        temps.append(base_temp + daily_variation)
    return np.array(temps)


def apply_temperature_effect(temperatures: np.ndarray, effect_per_degree: float = -0.015) -> np.ndarray:
    """기온 효과 적용"""
    reference_temp = 15.0
    temp_deviation = temperatures - reference_temp
    return temp_deviation * effect_per_degree


def generate_discount_rate(dates: pd.DatetimeIndex, events_df: pd.DataFrame) -> np.ndarray:
    """할인율 생성"""
    discount_rates = np.random.uniform(0, 0.10, len(dates))
    date_to_idx = {date: idx for idx, date in enumerate(dates)}
    promo_events = ['new_year_sale', 'summer_sale', 'black_friday']

    for _, event in events_df.iterrows():
        if event['holiday'] in promo_events:
            event_date = event['ds']
            lower = event['lower_window']
            upper = event['upper_window']
            for offset in range(-lower, upper + 1):
                target_date = event_date + timedelta(days=offset)
                if target_date in date_to_idx:
                    idx = date_to_idx[target_date]
                    discount_rates[idx] = np.random.uniform(0.20, 0.50)
    return discount_rates


def generate_noise(n_days: int, noise_std: float = 0.10) -> np.ndarray:
    """랜덤 노이즈 생성"""
    return np.random.normal(0, noise_std, n_days)


def combine_components(trend, weekly, yearly, events, temp_effect, noise) -> np.ndarray:
    """모든 요소 결합"""
    multiplier = 1 + weekly + yearly + events + temp_effect + noise
    sales = trend * multiplier
    return np.maximum(sales, 0)


def generate_ecommerce_data(start_date: str = "2023-01-01", days: int = 730):
    """전체 데이터 생성"""
    dates = generate_date_range(start_date, days)
    end_date = dates[-1].strftime("%Y-%m-%d")

    print(f"데이터 생성 기간: {start_date} ~ {end_date}")

    trend = generate_trend(dates)
    weekly = generate_weekly_seasonality(dates)
    yearly = generate_yearly_seasonality(dates)
    events_df = generate_events(start_date, end_date)
    event_effects = apply_event_effects(dates, events_df)
    temperature = generate_temperature(dates)
    temp_effect = apply_temperature_effect(temperature)
    discount_rate = generate_discount_rate(dates, events_df)
    noise = generate_noise(len(dates))
    sales = combine_components(trend, weekly, yearly, event_effects, temp_effect, noise)

    sales_df = pd.DataFrame({
        'ds': dates,
        'y': sales.round(0),
        'temperature': temperature.round(1),
        'discount_rate': discount_rate.round(3),
    })

    events_prophet_df = events_df[['holiday', 'ds', 'lower_window', 'upper_window']].copy()
    return sales_df, events_prophet_df


def save_data(sales_df: pd.DataFrame, events_df: pd.DataFrame, output_dir: Path) -> None:
    """데이터 저장"""
    output_dir.mkdir(parents=True, exist_ok=True)
    sales_df.to_csv(output_dir / "ecommerce_sales_data.csv", index=False)
    events_df.to_csv(output_dir / "ecommerce_events.csv", index=False)
    print(f"데이터 저장 완료!")


if __name__ == "__main__":
    sales_df, events_df = generate_ecommerce_data()
    script_dir = Path(__file__).parent
    save_data(sales_df, events_df, script_dir)
    print(f"\n평균 매출: {sales_df['y'].mean():,.0f}원")
    print(f"총 이벤트: {len(events_df)}개")

import os
import pandas as pd
import numpy as np

def clean_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    os.makedirs(processed_dir, exist_ok=True)
    
    print("=== STARTING DATA CLEANING PROCESS ===")
    
    # 1. 01_fund_master.csv
    print("\nProcessing 01_fund_master.csv...")
    fm_path = os.path.join(raw_dir, '01_fund_master.csv')
    df_fm = pd.read_csv(fm_path)
    # Strip whitespace from text columns
    text_cols_fm = ['fund_house', 'scheme_name', 'category', 'sub_category', 'plan', 'benchmark', 'fund_manager', 'risk_category', 'sebi_category_code']
    for col in text_cols_fm:
        if col in df_fm.columns:
            df_fm[col] = df_fm[col].astype(str).str.strip()
    df_fm['launch_date'] = pd.to_datetime(df_fm['launch_date']).dt.strftime('%Y-%m-%d')
    # Validate expense ratio range 0.1% - 2.5%
    exp_invalid = df_fm[(df_fm['expense_ratio_pct'] < 0.1) | (df_fm['expense_ratio_pct'] > 2.5)]
    if len(exp_invalid) > 0:
        print(f"Warning: Found {len(exp_invalid)} funds with expense_ratio_pct outside [0.1, 2.5]. Clipping values.")
        df_fm['expense_ratio_pct'] = df_fm['expense_ratio_pct'].clip(0.1, 2.5)
    df_fm.to_csv(os.path.join(processed_dir, '01_fund_master.csv'), index=False)
    print(f"-> Saved 01_fund_master.csv: {len(df_fm)} rows")
    
    # 2. 02_nav_history.csv
    print("\nProcessing 02_nav_history.csv...")
    nav_path = os.path.join(raw_dir, '02_nav_history.csv')
    df_nav = pd.read_csv(nav_path)
    df_nav['date'] = pd.to_datetime(df_nav['date'])
    # Remove duplicates
    df_nav = df_nav.drop_duplicates(subset=['amfi_code', 'date'])
    # Sort
    df_nav = df_nav.sort_values(by=['amfi_code', 'date'])
    # Validate NAV > 0
    df_nav = df_nav[df_nav['nav'] > 0]
    
    # Forward-fill missing NAV for weekends/holidays per scheme
    dfs_nav = []
    for amfi, group in df_nav.groupby('amfi_code'):
        group = group.sort_values('date')
        min_date = group['date'].min()
        max_date = group['date'].max()
        full_idx = pd.date_range(min_date, max_date, freq='D', name='date')
        group = group.set_index('date').reindex(full_idx)
        group['amfi_code'] = amfi
        group['nav'] = group['nav'].ffill()
        dfs_nav.append(group.reset_index())
    
    df_nav_clean = pd.concat(dfs_nav, ignore_index=True)
    df_nav_clean['date'] = df_nav_clean['date'].dt.strftime('%Y-%m-%d')
    # Calculate daily return percentage
    df_nav_clean['daily_return_pct'] = df_nav_clean.groupby('amfi_code')['nav'].pct_change() * 100
    df_nav_clean['daily_return_pct'] = df_nav_clean['daily_return_pct'].fillna(0.0)
    
    df_nav_clean.to_csv(os.path.join(processed_dir, '02_nav_history.csv'), index=False)
    print(f"-> Saved 02_nav_history.csv: {len(df_nav_clean)} rows")
    
    # 3. 03_aum_by_fund_house.csv
    print("\nProcessing 03_aum_by_fund_house.csv...")
    aum_path = os.path.join(raw_dir, '03_aum_by_fund_house.csv')
    df_aum = pd.read_csv(aum_path)
    df_aum['date'] = pd.to_datetime(df_aum['date']).dt.strftime('%Y-%m-%d')
    df_aum['fund_house'] = df_aum['fund_house'].astype(str).str.strip()
    df_aum.to_csv(os.path.join(processed_dir, '03_aum_by_fund_house.csv'), index=False)
    print(f"-> Saved 03_aum_by_fund_house.csv: {len(df_aum)} rows")
    
    # 4. 04_monthly_sip_inflows.csv
    print("\nProcessing 04_monthly_sip_inflows.csv...")
    sip_path = os.path.join(raw_dir, '04_monthly_sip_inflows.csv')
    df_sip = pd.read_csv(sip_path)
    df_sip['month'] = df_sip['month'].astype(str).str.strip()
    df_sip.to_csv(os.path.join(processed_dir, '04_monthly_sip_inflows.csv'), index=False)
    print(f"-> Saved 04_monthly_sip_inflows.csv: {len(df_sip)} rows")
    
    # 5. 05_category_inflows.csv
    print("\nProcessing 05_category_inflows.csv...")
    cat_path = os.path.join(raw_dir, '05_category_inflows.csv')
    df_cat = pd.read_csv(cat_path)
    df_cat['month'] = df_cat['month'].astype(str).str.strip()
    df_cat['category'] = df_cat['category'].astype(str).str.strip()
    df_cat.to_csv(os.path.join(processed_dir, '05_category_inflows.csv'), index=False)
    print(f"-> Saved 05_category_inflows.csv: {len(df_cat)} rows")
    
    # 6. 06_industry_folio_count.csv
    print("\nProcessing 06_industry_folio_count.csv...")
    folio_path = os.path.join(raw_dir, '06_industry_folio_count.csv')
    df_folio = pd.read_csv(folio_path)
    df_folio['month'] = df_folio['month'].astype(str).str.strip()
    df_folio.to_csv(os.path.join(processed_dir, '06_industry_folio_count.csv'), index=False)
    print(f"-> Saved 06_industry_folio_count.csv: {len(df_folio)} rows")
    
    # 7. 07_scheme_performance.csv
    print("\nProcessing 07_scheme_performance.csv...")
    sp_path = os.path.join(raw_dir, '07_scheme_performance.csv')
    df_sp = pd.read_csv(sp_path)
    num_cols_sp = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'benchmark_3yr_pct',
                   'alpha', 'beta', 'sharpe_ratio', 'sortino_ratio', 'std_dev_ann_pct',
                   'max_drawdown_pct', 'aum_crore', 'expense_ratio_pct', 'morningstar_rating']
    for col in num_cols_sp:
        if col in df_sp.columns:
            df_sp[col] = pd.to_numeric(df_sp[col], errors='coerce')
    
    # Check expense_ratio_pct range [0.1, 2.5]
    df_sp['expense_ratio_pct'] = df_sp['expense_ratio_pct'].clip(0.1, 2.5)
    
    # Flag negative Sharpe ratios or anomalies if any
    neg_sharpe = df_sp[df_sp['sharpe_ratio'] < 0]
    if len(neg_sharpe) > 0:
        print(f"Info: {len(neg_sharpe)} schemes have negative Sharpe ratios.")
    else:
        print("Info: No schemes have negative Sharpe ratios.")
        
    df_sp.to_csv(os.path.join(processed_dir, '07_scheme_performance.csv'), index=False)
    print(f"-> Saved 07_scheme_performance.csv: {len(df_sp)} rows")
    
    # 8. 08_investor_transactions.csv
    print("\nProcessing 08_investor_transactions.csv...")
    tx_path = os.path.join(raw_dir, '08_investor_transactions.csv')
    df_tx = pd.read_csv(tx_path)
    
    # Parse dates
    df_tx['transaction_date'] = pd.to_datetime(df_tx['transaction_date']).dt.strftime('%Y-%m-%d')
    
    # Standardise transaction_type
    type_map = {
        'sip': 'SIP', 'SIP': 'SIP',
        'lumpsum': 'Lumpsum', 'Lumpsum': 'Lumpsum', 'LUMP SUM': 'Lumpsum',
        'redemption': 'Redemption', 'Redemption': 'Redemption', 'REDEMPTION': 'Redemption'
    }
    df_tx['transaction_type'] = df_tx['transaction_type'].astype(str).str.strip().map(lambda x: type_map.get(x, x.capitalize()))
    
    # Validate amount_inr > 0
    invalid_amt = (df_tx['amount_inr'] <= 0).sum()
    if invalid_amt > 0:
        print(f"Warning: Removing {invalid_amt} transactions with amount <= 0")
        df_tx = df_tx[df_tx['amount_inr'] > 0]
        
    # Standardise kyc_status
    kyc_map = {'verified': 'Verified', 'Verified': 'Verified', 'pending': 'Pending', 'Pending': 'Pending'}
    df_tx['kyc_status'] = df_tx['kyc_status'].astype(str).str.strip().map(lambda x: kyc_map.get(x, x.capitalize()))
    
    df_tx.to_csv(os.path.join(processed_dir, '08_investor_transactions.csv'), index=False)
    print(f"-> Saved 08_investor_transactions.csv: {len(df_tx)} rows")
    
    # 9. 09_portfolio_holdings.csv
    print("\nProcessing 09_portfolio_holdings.csv...")
    port_path = os.path.join(raw_dir, '09_portfolio_holdings.csv')
    df_port = pd.read_csv(port_path)
    df_port['portfolio_date'] = pd.to_datetime(df_port['portfolio_date']).dt.strftime('%Y-%m-%d')
    text_cols_port = ['stock_symbol', 'stock_name', 'sector']
    for col in text_cols_port:
        if col in df_port.columns:
            df_port[col] = df_port[col].astype(str).str.strip()
    df_port.to_csv(os.path.join(processed_dir, '09_portfolio_holdings.csv'), index=False)
    print(f"-> Saved 09_portfolio_holdings.csv: {len(df_port)} rows")
    
    # 10. 10_benchmark_indices.csv
    print("\nProcessing 10_benchmark_indices.csv...")
    bm_path = os.path.join(raw_dir, '10_benchmark_indices.csv')
    df_bm = pd.read_csv(bm_path)
    df_bm['date'] = pd.to_datetime(df_bm['date']).dt.strftime('%Y-%m-%d')
    df_bm['index_name'] = df_bm['index_name'].astype(str).str.strip()
    df_bm = df_bm[df_bm['close_value'] > 0]
    df_bm = df_bm.sort_values(by=['index_name', 'date'])
    df_bm.to_csv(os.path.join(processed_dir, '10_benchmark_indices.csv'), index=False)
    print(f"-> Saved 10_benchmark_indices.csv: {len(df_bm)} rows")
    
    print("\n=== DATA CLEANING COMPLETE! ALL 10 CSVs SAVED TO data/processed/ ===")

if __name__ == '__main__':
    clean_data()

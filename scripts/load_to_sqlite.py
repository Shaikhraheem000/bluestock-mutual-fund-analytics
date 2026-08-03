import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    db_path = os.path.join(base_dir, 'bluestock_mf.db')
    schema_path = os.path.join(base_dir, 'schema.sql')
    
    print("=== STARTING DATABASE LOADING PROCESS ===")
    
    # 1. Initialize SQLite schema using sqlite3
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    print(f"Initialized database schema at {db_path}")
    
    # 2. Populate dim_date first
    print("\nGenerating dim_date entries...")
    nav_df = pd.read_csv(os.path.join(processed_dir, '02_nav_history.csv'))
    tx_df = pd.read_csv(os.path.join(processed_dir, '08_investor_transactions.csv'))
    bm_df = pd.read_csv(os.path.join(processed_dir, '10_benchmark_indices.csv'))
    
    all_dates = pd.concat([
        pd.to_datetime(nav_df['date']),
        pd.to_datetime(tx_df['transaction_date']),
        pd.to_datetime(bm_df['date'])
    ]).dropna().unique()
    
    all_dates = pd.Series(all_dates).sort_values()
    
    dim_date_df = pd.DataFrame({'date': all_dates.dt.strftime('%Y-%m-%d')})
    dim_date_df['year'] = all_dates.dt.year
    dim_date_df['month'] = all_dates.dt.month
    dim_date_df['quarter'] = all_dates.dt.quarter
    dim_date_df['day_of_week'] = all_dates.dt.dayofweek
    dim_date_df['is_weekday'] = (all_dates.dt.dayofweek < 5).astype(int)
    
    # Load into SQLite database using SQLAlchemy
    for target_db in [db_path]:
        engine = create_engine(f"sqlite:///{target_db}")
        
        print(f"\nLoading data into {target_db}...")
        
        # dim_fund
        df_fm = pd.read_csv(os.path.join(processed_dir, '01_fund_master.csv'))
        df_fm.to_sql('dim_fund', engine, if_exists='append', index=False)
        print(f"-> Loaded dim_fund: {len(df_fm)} rows")
        
        # dim_date
        dim_date_df.to_sql('dim_date', engine, if_exists='append', index=False)
        print(f"-> Loaded dim_date: {len(dim_date_df)} rows")
        
        # fact_nav
        nav_df.to_sql('fact_nav', engine, if_exists='append', index=False)
        print(f"-> Loaded fact_nav: {len(nav_df)} rows")
        
        # fact_transactions
        tx_df.to_sql('fact_transactions', engine, if_exists='append', index=False)
        print(f"-> Loaded fact_transactions: {len(tx_df)} rows")
        
        # fact_performance
        sp_df = pd.read_csv(os.path.join(processed_dir, '07_scheme_performance.csv'))
        sp_df.to_sql('fact_performance', engine, if_exists='append', index=False)
        print(f"-> Loaded fact_performance: {len(sp_df)} rows")
        
        # fact_aum
        aum_df = pd.read_csv(os.path.join(processed_dir, '03_aum_by_fund_house.csv'))
        aum_df.to_sql('fact_aum', engine, if_exists='append', index=False)
        print(f"-> Loaded fact_aum: {len(aum_df)} rows")
        
        # fact_portfolio
        port_df = pd.read_csv(os.path.join(processed_dir, '09_portfolio_holdings.csv'))
        port_df.to_sql('fact_portfolio', engine, if_exists='append', index=False)
        print(f"-> Loaded fact_portfolio: {len(port_df)} rows")
        
        # fact_sip_industry
        sip_df = pd.read_csv(os.path.join(processed_dir, '04_monthly_sip_inflows.csv'))
        sip_df.to_sql('fact_sip_industry', engine, if_exists='append', index=False)
        print(f"-> Loaded fact_sip_industry: {len(sip_df)} rows")
        
        # fact_category_inflows
        cat_df = pd.read_csv(os.path.join(processed_dir, '05_category_inflows.csv'))
        cat_df.to_sql('fact_category_inflows', engine, if_exists='append', index=False)
        print(f"-> Loaded fact_category_inflows: {len(cat_df)} rows")
        
        # fact_industry_folios
        folio_df = pd.read_csv(os.path.join(processed_dir, '06_industry_folio_count.csv'))
        folio_df.to_sql('fact_industry_folios', engine, if_exists='append', index=False)
        print(f"-> Loaded fact_industry_folios: {len(folio_df)} rows")
        
        # fact_benchmark_indices
        bm_df.to_sql('fact_benchmark_indices', engine, if_exists='append', index=False)
        print(f"-> Loaded fact_benchmark_indices: {len(bm_df)} rows")
        
    print("\n=== DATABASE LOADING & ROW COUNT VERIFICATION COMPLETE ===")

if __name__ == '__main__':
    load_data()

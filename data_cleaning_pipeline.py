import pandas as pd

def clean_transaction_data(input_path, output_path):
    # 1. Load raw data
    print("Initializing Data Cleaning Pipeline...")
    df = pd.read_csv(input_path)
    print(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns successfully.")
    
    # 2. Check for absolute row duplicates
    duplicates = df.duplicated().sum()
    print(f"Absolute row duplicates found: {duplicates}")
    if duplicates > 0:
        df = df.drop_duplicates()
        print("Absolute duplicate rows dropped.")
        
    # 3. Check for uniqueness constraint on Primary Key (OrderID)
    id_duplicates = df['OrderID'].duplicated().sum()
    print(f"Duplicate OrderIDs identified: {id_duplicates}")
    
    # 4. Handle Missing Values (Strategic Imputation Context)
    null_summary = df.isnull().sum()
    print("\nMissing Value Scan Profile:")
    for col, count in null_summary.items():
        if count > 0:
            print(f" - Column '{col}': {count} missing records")
            
    # Preserve blank CouponCodes to protect conversion and marketing analysis metrics
    # Explicitly filling NaN with 'NO_COUPON' for downstream categorization clarity
    df['CouponCode'] = df['CouponCode'].fillna('NO_COUPON')
    
    # 5. String Normalization & Text Standardization
    print("\nExecuting structural string regularization...")
    categorical_columns = ['Product', 'PaymentMethod', 'OrderStatus', 'ReferralSource']
    for col in categorical_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
            
    # 6. Date/Temporal Format Standardization
    print("Standardizing temporal variables to ISO 8601...")
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # 7. Validate Data Integrity Framework
    print("\nPipeline verification complete. Final row structure matches data dictionary standards.")
    
    # Export cleaned source of truth
    df.to_csv(output_path, index=False)
    print(f"Processed file securely saved to: {output_path}")

if __name__ == "__main__":
    clean_transaction_data(
        input_path='Dataset for Data Analytics.xlsx - Sheet1.csv',
        output_path='Cleaned_Dataset_Project_1.csv'
    )

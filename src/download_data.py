import kagglehub, shutil, os

os.makedirs("../Data/raw", exist_ok=True)

path = kagglehub.dataset_download("blastchar/telco-customer-churn")
fichier_csv = [f for f in os.listdir(path) if f.endswith('.csv')][0]
shutil.copy(os.path.join(path, fichier_csv), "../Data/raw/telco_churn_raw.csv")

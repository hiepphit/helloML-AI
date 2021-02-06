 
import pandas as pd
import os
counts=[1,2]
names=['hello', 'word']
abs_dir = os.path.dirname(__file__)
new_csv_path = abs_dir+'/women_best_sell_sephora.csv'
df = pd.DataFrame({'No': counts, 'Name': names})
df.to_csv(new_csv_path, index=False, encoding='utf-8')
print('OK')

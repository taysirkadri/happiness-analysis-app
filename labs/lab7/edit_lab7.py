import json
from pathlib import Path
import re
notebook_path = Path('lab7/lab7.ipynb')
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        
        # Edit 1: RidgeCV and LassoCV
        if 'models = {' in source and '"Ridge": Ridge(alpha=1.0)' in source:
            # Replace imports
            source = source.replace(
                'from sklearn.linear_model import LinearRegression, Ridge, Lasso',
                'from sklearn.linear_model import LinearRegression, Ridge, Lasso, RidgeCV, LassoCV'
            )
            # Replace models dict
            source = source.replace(
                '"Ridge": Ridge(alpha=1.0),',
                '"Ridge": RidgeCV(alphas=np.logspace(-3, 3, 50), cv=5),'
            )
            source = source.replace(
                '"Lasso": Lasso(alpha=0.01, max_iter=10000),',
                '"Lasso": LassoCV(alphas=np.logspace(-3, 0, 30), cv=5, max_iter=50000),'
            )
            # Add print statement at the end of the cell
            print_stmt = '\n\nprint(f"Selected Ridge alpha: {models[\'Ridge\'].alpha_}")\nprint(f"Selected Lasso alpha: {models[\'Lasso\'].alpha_}")\n'
            # Just append to the source
            source = source + print_stmt
            
            cell['source'] = [line + ('\n' if i < len(source.split('\n'))-1 else '') for i, line in enumerate(source.split('\n'))]
            
        # Edit 2: statsmodels OLS
        elif 'ols = models["OLS"]' in source and 'coef_df = pd.DataFrame' in source:
            new_source = """import statsmodels.api as sm
X_train_sm = sm.add_constant(X_train)
ols_sm = sm.OLS(y_train, X_train_sm).fit()
print(ols_sm.summary())"""
            cell['source'] = [line + ('\n' if i < len(new_source.split('\n'))-1 else '') for i, line in enumerate(new_source.split('\n'))]
    # Edit 3: Observation note replacement
    elif cell['cell_type'] == 'markdown':
        source = "".join(cell['source'])
        if 'I found the final recipe for a happy country.' in source:
            new_source = "**Observation:**\nWith statsmodels, I can see not just which features have large coefficients, but also which ones are statistically distinguishable from zero."
            cell['source'] = [line + ('\n' if i < len(new_source.split('\n'))-1 else '') for i, line in enumerate(new_source.split('\n'))]
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

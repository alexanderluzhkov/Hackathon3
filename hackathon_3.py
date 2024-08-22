# -*- coding: utf-8 -*-
"""Hackathon_3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/195WAdL67iqFTL_DP03ExrMY8Rg3kM8D3
"""

import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('insurance.csv')

# Display the first 5 rows
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Print the column names and their data types
print(df.info())

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Display descriptive statistics for numerical columns
print("Descriptive statistics for numerical columns:\n")
print(df[['age', 'bmi', 'children', 'charges']].describe().to_markdown(numalign="left", stralign="left"))

# Display the count and frequency of values for categorical columns
print("\nValue counts for categorical columns:\n")
for col in ['sex', 'smoker', 'region']:
    print(f"\nColumn: {col}\n")
    print(df[col].value_counts().reset_index().rename(columns={'index':'Value', col: 'Count'}).to_markdown(index=False, numalign="left", stralign="left"))

# One-hot encode categorical columns without dropping the first column
df_encoded = pd.get_dummies(df, columns=['sex', 'smoker', 'region'], drop_first=False)

# Compute the correlation matrix
corr_matrix = df_encoded.corr()

# Display the correlation matrix rounded to 2 decimal places
print("\nCorrelation Matrix:\n")
print(corr_matrix.round(2).to_markdown(numalign="left", stralign="left"))

# Create a heatmap to visualize the correlation matrix
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.show()

# Create subplots
fig, axes = plt.subplots(1, 3, figsize=(15, 6))

# Boxplot of charges across different regions
sns.boxplot(x='region', y='charges', data=df, ax=axes[0])
axes[0].set_title('Charges Distribution by Region')

# Boxplot of charges for smokers and non-smokers
sns.boxplot(x='smoker', y='charges', data=df, ax=axes[1])
axes[1].set_title('Charges Distribution by Smoker Status')

# Scatterplot of bmi vs charges, colored by smoker status
sns.scatterplot(x='bmi', y='charges', hue='smoker', data=df, ax=axes[2])
axes[2].set_title('BMI vs Charges (Colored by Smoker)')

# Display the plots
plt.tight_layout()
plt.show()

import altair as alt
from scipy.stats import f_oneway

# 1. Group data by region and compute statistics
regional_stats = df.groupby('region')['charges'].agg(['mean', 'median', 'std']).round(2)

# Display the regional statistics
print("Regional Statistics for Charges:\n")
print(regional_stats.to_markdown(numalign="left", stralign="left"))

# 2. Create a box plot to visualize charges distribution by region
chart = alt.Chart(df).mark_boxplot().encode(
    x='region:N',
    y='charges:Q',
    color='region:N',
    tooltip = ['region', 'charges']
).properties(
    title='Charges Distribution by Region'
).interactive()

chart.save('charges_distribution_by_region_boxplot.json')

# 3. Perform ANOVA test
northeast = df[df['region'] == 'northeast']['charges']
northwest = df[df['region'] == 'northwest']['charges']
southeast = df[df['region'] == 'southeast']['charges']
southwest = df[df['region'] == 'southwest']['charges']

f_statistic, p_value = f_oneway(northeast, northwest, southeast, southwest)

# Print the results
print(f"\nANOVA Test Results:\nF-statistic: {f_statistic:.3f}, p-value: {p_value:.3f}")

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file into a DataFrame
df = pd.read_csv('insurance.csv')

# One-hot encode categorical columns
df_encoded = pd.get_dummies(df, columns=['sex', 'smoker', 'region'], drop_first=True)

# Calculate rates for each region
def calculate_rates(group):
    return pd.Series({
        'age_mean': group['age'].mean(),
        'bmi_mean': group['bmi'].mean(),
        'children_mean': group['children'].mean(),
        'sex_male_rate': (group['sex'] == 'male').mean(),
        'smoker_rate': (group['smoker'] == 'yes').mean()
    })

regional_rates = df.groupby('region').apply(calculate_rates).reset_index()
print("Regional Rates:")
print(regional_rates.to_markdown(index=False, numalign="left", stralign="left"))

# Perform ANOVA tests
def perform_anova(column):
    groups = [group[column].values for name, group in df.groupby('region')]
    f_value, p_value = stats.f_oneway(*groups)
    return pd.Series({'F-value': f_value, 'p-value': p_value})

anova_results = pd.DataFrame({
    'age': perform_anova('age'),
    'bmi': perform_anova('bmi'),
    'children': perform_anova('children')
}).T

print("\nANOVA Results for Numerical Variables:")
print(anova_results.to_markdown(numalign="left", stralign="left"))

# Chi-square tests for categorical variables
def perform_chi_square(column):
    contingency_table = pd.crosstab(df['region'], df[column])
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    return pd.Series({'chi2': chi2, 'p-value': p_value})

chi_square_results = pd.DataFrame({
    'sex': perform_chi_square('sex'),
    'smoker': perform_chi_square('smoker')
}).T

print("\nChi-square Test Results for Categorical Variables:")
print(chi_square_results.to_markdown(numalign="left", stralign="left"))

# Create visualizations
fig, axes = plt.subplots(2, 3, figsize=(20, 15))


# Flatten the 2D array of axes for easier indexing
axes = axes.flatten()

# Remove the last subplot (we only need 5)
fig.delaxes(axes[5])

# Age distribution by region
sns.boxplot(x='region', y='age', data=df, ax=axes[0])
axes[0].set_title('Age Distribution by Region')

# BMI distribution by region
sns.boxplot(x='region', y='bmi', data=df, ax=axes[1])
axes[1].set_title('BMI Distribution by Region')

# Children distribution by region
sns.boxplot(x='region', y='children', data=df, ax=axes[2])
axes[2].set_title('Children Distribution by Region')

# Sex distribution by region
sns.countplot(x='region', hue='sex', data=df, ax=axes[3])
axes[3].set_title('Sex Distribution by Region')

# Smoker distribution by region
sns.countplot(x='region', hue='smoker', data=df, ax=axes[4])
axes[4].set_title('Smoker Distribution by Region')

# Adjust the layout
plt.tight_layout()

# Show the plot
plt.show()

import pandas as pd

# Assuming df is your DataFrame
print(df['smoker'].head())
print(df['smoker'].dtype)

# Check unique values
print(df['smoker'].unique())

# Preprocess the 'smoker' column
df['smoker_binary'] = df['smoker'].apply(lambda x: 'yes' if 'yes' in x else 'no')

# Convert to numeric
df['smoker_numeric'] = (df['smoker_binary'] == 'yes').astype(int)

# Verify the new columns
print(df[['smoker', 'smoker_binary', 'smoker_numeric']].head())

# Now let's try our analysis again
for region in df['region'].unique():
    region_data = df[df['region'] == region]
    male_smoker_rate = region_data[region_data['sex'] == 'male']['smoker_numeric'].mean()
    female_smoker_rate = region_data[region_data['sex'] == 'female']['smoker_numeric'].mean()
    print(f"{region} - Male smoker rate: {male_smoker_rate:.2f}, Female smoker rate: {female_smoker_rate:.2f}")

# BMI analysis (this should work as is)
for region in df['region'].unique():
    region_data = df[df['region'] == region]
    male_bmi = region_data[region_data['sex'] == 'male']['bmi'].mean()
    female_bmi = region_data[region_data['sex'] == 'female']['bmi'].mean()
    print(f"{region} - Male average BMI: {male_bmi:.2f}, Female average BMI: {female_bmi:.2f}")

import scipy.stats as stats

def region_gender_comparison(df, region, variable):
    region_data = df[df['region'] == region]
    male_data = region_data[region_data['sex'] == 'male'][variable]
    female_data = region_data[region_data['sex'] == 'female'][variable]
    t_stat, p_value = stats.ttest_ind(male_data, female_data)
    return p_value

# Smoking comparison
for region in df['region'].unique():
    p_value = region_gender_comparison(df, region, 'smoker_numeric')
    print(f"{region} - Smoking gender difference p-value: {p_value:.4f}")

# BMI comparison
for region in df['region'].unique():
    p_value = region_gender_comparison(df, region, 'bmi')
    print(f"{region} - BMI gender difference p-value: {p_value:.4f}")

# Regional comparison
f_stat, p_value = stats.f_oneway(df[df['region'] == 'southwest']['smoker_numeric'],
                                 df[df['region'] == 'southeast']['smoker_numeric'],
                                 df[df['region'] == 'northwest']['smoker_numeric'],
                                 df[df['region'] == 'northeast']['smoker_numeric'])
print(f"Regional smoking difference p-value: {p_value:.4f}")

f_stat, p_value = stats.f_oneway(df[df['region'] == 'southwest']['bmi'],
                                 df[df['region'] == 'southeast']['bmi'],
                                 df[df['region'] == 'northwest']['bmi'],
                                 df[df['region'] == 'northeast']['bmi'])
print(f"Regional BMI difference p-value: {p_value:.4f}")

import matplotlib.pyplot as plt
import seaborn as sns

# Smoking rates by region and gender
plt.figure(figsize=(12, 6))
sns.barplot(x='region', y='smoker_numeric', hue='sex', data=df)
plt.title('Smoking Rates by Region and Gender')
plt.ylabel('Smoking Rate')
plt.show()

# BMI by region and gender
plt.figure(figsize=(12, 6))
sns.boxplot(x='region', y='bmi', hue='sex', data=df)
plt.title('BMI Distribution by Region and Gender')
plt.show()

"""**Correlation Analysis:**
   - Strongest correlation (0.79) is between smoking status and charges.
   - Age and BMI have moderate positive correlations with charges (0.3 and 0.2 respectively).
   - The Southeast region shows a positive correlation with BMI (0.27).

 **Regional Analysis:**
   - Southeast has the highest mean BMI (33.356) and highest smoker rate (25%).
   - Southwest has the highest mean age (39.4554 years).
   - ANOVA results show significant differences in BMI across regions (p-value: 1.88e-24).
   - Chi-square test for smoking across regions is close to significant (p-value: 0.0617).

 **Gender Differences:**
   - Males have higher smoker rates in most regions, especially Southwest and Southeast.
   - Males generally have higher BMI, particularly in the Southeast.
   - Gender differences in smoking are statistically significant in the Southwest (p-value: 0.0219).


**Key Insights:**
1. Smoking is the strongest predictor of higher insurance charges.
2. The Southeast region stands out with higher BMI and smoking rates, likely caused by lifestyle choices.
3. Gender plays a role in smoking habits, with males more likely to smoke, especially in certain regions.
4. Age is positively associated with BMI but doesn't significantly affect smoking probability.
5. Regional differences are more significant for BMI than for smoking habits when controlling for other factors.
6. The relationship between smoking and BMI is not straightforward, as smoking doesn't significantly predict BMI in the regression model.

These findings suggest that insurance companies might need to consider regional factors, particularly for the Southeast, when assessing health risks and determining premiums. Additionally, targeted health interventions focusing on changing behaviour patterns,  reducing smoking rates and addressing obesity, especially in the Southeast, could be beneficial for public health initiatives.

"""
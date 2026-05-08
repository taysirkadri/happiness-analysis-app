# Lab 4b — Feature Engineering: Getting More Out of What We Have

## Why this lab exists

After lab4, I had a clean, scaled, model-ready dataset. Six features, no missing values, ready to feed into a regression model. I could have gone straight to modeling. But I kept thinking about a problem I noticed in the EDA correlation heatmap: GDP, social support, and life expectancy all move together. In a regression model that sees them as separate inputs, none of them gets full credit for what they collectively represent.

Raw features have limits because they only encode information linearly. But the real world is rarely just a straight line. If you are extremely wealthy but have zero social support, that wealth might not translate to happiness as effectively as if you had both. By relying only on the base features, my model would miss these compounding, non-linear realities.

I decided to engineer four specific features to test this. First, I multiplied GDP and social support together to capture their combined synergy. Second, I squared life expectancy because its impact on happiness might curve at the upper extremes. Third, I created a "freedom to trust" ratio, assuming that true societal autonomy means both feeling free and trusting institutions. Finally, I noticed that rich countries just give more money overall — so I took the residuals of generosity against GDP to find a pure "altruism" signal isolated from national wealth. 

## What I built

I built the following four features:
- `gdp_social_interaction = gdp_per_capita * social_support`: Captures the amplified effect of having both wealth and a strong social safety net.
- `life_expectancy_sq = life_expectancy ** 2`: Allows the model to fit curvature at the upper bounds of human health.
- `freedom_trust_ratio = freedom / (trust + 1e-6)`: Evaluates whether feeling free is balanced by having trustworthy systems.
- `generosity_gdp_residual = generosity - pred_generosity`: Uses a linear fit to strip out the portion of generosity that is purely driven by being wealthy.

Before adding them to the model, I wanted evidence they actually relate to happiness more than the raw features they came from. A feature that adds noise is worse than no feature at all.

## What the correlations showed

The interaction term between GDP and social support came out incredibly strong, essentially matching or slightly exceeding the best individual predictors, which confirmed my suspicion that wealth and social support amplify each other. The squared life expectancy term also performed well, maintaining a very high correlation and validating the non-linear transformation.

However, the `freedom_trust_ratio` came out somewhat weak compared to the base `freedom` score alone. And while `generosity_gdp_residual` had a different profile than raw generosity, it didn't magically become a top-tier predictor. This was a good lesson: controlling for a confounder like GDP makes the feature more mathematically "pure," but it doesn't always make it a stronger predictor of the target variable.

## The one that surprised me

The `freedom_trust_ratio` was the most surprising to me. Conceptually, it felt like a brilliant idea — measuring "autonomous trust." But in practice, taking the ratio of two variables where the denominator (`trust`) can be very small led to a lot of variance. It reminded me that just because an engineered feature sounds smart in a textbook or in theory doesn't mean the data supports it. Sometimes the raw, simple feature is actually more stable.

## What this changes for the rest of the project

Now that I have validated these features, I've appended them to the main dataset. My lab5 EDA and lab6/lab7 modeling will now use this enriched dataset with all 10 features. The enriched train and test CSVs are saved and ready to go. The real test of whether these features were actually worth building comes in lab7, when I will finally compare the R² with and without them to see if they move the needle.

## Outputs

- lab4b_plot_feature_correlations.png
- lab4b_plot_engineered_scatters.png
- lab4b_feature_correlations.csv
- lab4b_feature_summary.csv
- lab4b_train_enriched.csv
- lab4b_test_enriched.csv

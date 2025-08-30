A/B Testing Project Report-Website Design 

Background
Businesses often launch new features, pricing strategies, or marketing campaigns with the hope of increasing conversion rates and improving revenue. However, making changes without testing can be risky — the new variation may not perform better than the current baseline.
A/B testing is a widely used statistical method that allows companies to test two versions (Control vs. Variant) and determine, with statistical significance, which version drives better results.
In this project, we simulate an A/B test scenario where a company wants to evaluate whether a new website design (Variant B) increases user conversion rates compared to the current design (Control A).

Problem Statement
The company’s management is considering rolling out a new design for its website landing page. The main question is:

Does the new design (B) improve conversion rates compared to the old design (A)?
If the difference is statistically significant, the company can confidently deploy the new design. Otherwise, it should continue with the old version to avoid potential revenue loss.

Dataset
We created a synthetic dataset containing the following fields:
•	user_id → Unique identifier for each user
•	group → "A" (Control group with the old design) or "B" (Variant group with the new design)
•	converted → 1 if the user converted (e.g., signed up, purchased), 0 if not
Example snippet:
        user_id	1, 2, 3, 4 
group	converted A, B, A, B
                0, 1, 0, 1

Methodology
1.	Exploratory Data Analysis (EDA)
o	Checked group balance (equal distribution of users across A and B).
o	Calculated conversion rates per group.

2.	Hypothesis Testing
o	Null Hypothesis (H₀): Conversion rates for A and B are the same.
o	Alternative Hypothesis (H₁): Conversion rate for B is greater than A.
o	Test Used: Two-proportion z-test.

3.	Visualization
o	Bar charts comparing conversion rates for A vs. B.
o	Histograms showing distribution of conversions.
Results
•	Conversion Rate (Group A): ~ X%
•	Conversion Rate (Group B): ~ Y%
•	p-value: ~ Z
Interpretation:
•	If p-value < 0.05, we reject the null hypothesis and conclude that the new design (B) significantly improves conversions.
•	If p-value ≥ 0.05, we fail to reject the null hypothesis, meaning there is no significant evidence that B outperforms A.

Conclusion
•	If significant:
✅ The new landing page (Variant B) outperforms the old design, and the company should roll it out.
•	If not significant:
❌ The test shows no statistical improvement, so the company should stick with the current design until further optimizations are tested.


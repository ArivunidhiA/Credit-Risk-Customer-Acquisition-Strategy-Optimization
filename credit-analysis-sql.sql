-- Customer Risk Segmentation Analysis
WITH RiskSegments AS (
    SELECT 
        CASE 
            WHEN credit_score >= 750 THEN 'Prime'
            WHEN credit_score >= 650 THEN 'Near Prime'
            ELSE 'Subprime'
        END AS risk_segment,
        customer_id,
        income,
        loan_amount,
        default_probability
    FROM credit_data
)
SELECT 
    risk_segment,
    COUNT(*) as customer_count,
    AVG(income) as avg_income,
    AVG(loan_amount) as avg_loan_amount,
    AVG(default_probability) as avg_default_prob,
    SUM(loan_amount) as total_loan_volume
FROM RiskSegments
GROUP BY risk_segment
ORDER BY avg_default_prob DESC;

-- Portfolio Performance Metrics
WITH PortfolioMetrics AS (
    SELECT 
        DATE_TRUNC('month', application_date) as month,
        COUNT(*) as applications,
        SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) as approvals,
        AVG(loan_amount) as avg_loan_size,
        SUM(loan_amount) as total_loan_volume,
        AVG(default_probability) as avg_default_risk
    FROM credit_data
    GROUP BY DATE_TRUNC('month', application_date)
)
SELECT 
    month,
    applications,
    approvals,
    (approvals::float / applications) * 100 as approval_rate,
    avg_loan_size,
    total_loan_volume,
    avg_default_risk
FROM PortfolioMetrics
ORDER BY month DESC;

-- Risk Factor Analysis
SELECT 
    CASE 
        WHEN age < 25 THEN '18-24'
        WHEN age < 35 THEN '25-34'
        WHEN age < 45 THEN '35-44'
        WHEN age < 55 THEN '45-54'
        ELSE '55+'
    END as age_group,
    CASE 
        WHEN income < 30000 THEN 'Low Income'
        WHEN income < 60000 THEN 'Medium Income'
        WHEN income < 100000 THEN 'High Income'
        ELSE 'Very High Income'
    END as income_group,
    COUNT(*) as customer_count,
    AVG(default_probability) as avg_default_risk,
    AVG(credit_score) as avg_credit_score
FROM credit_data
GROUP BY 
    CASE 
        WHEN age < 25 THEN '18-24'
        WHEN age < 35 THEN '25-34'
        WHEN age < 45 THEN '35-44'
        WHEN age < 55 THEN '45-54'
        ELSE '55+'
    END,
    CASE 
        WHEN income < 30000 THEN 'Low Income'
        WHEN income < 60000 THEN 'Medium Income'
        WHEN income < 100000 THEN 'High Income'
        ELSE 'Very High Income'
    END
ORDER BY age_group, income_group;

-- Fraud Detection Query
SELECT 
    customer_id,
    application_date,
    loan_amount,
    income,
    credit_score,
    default_probability
FROM credit_data
WHERE (
    loan_amount > 5 * income OR
    (SELECT COUNT(*) 
     FROM credit_data c2 
     WHERE c2.customer_id = credit_data.customer_id) > 3 OR
    default_probability > 0.8
)
ORDER BY application_date DESC;

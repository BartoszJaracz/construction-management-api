-- Construction Management API - views

CREATE VIEW [dbo].[vw_ElementsWithoutCalculations] AS
		SELECT
		se.ElementId,
		p.ProjectId,
		p.ProjectName,
		se.Name,
		se.Dimensions,
		se.TechnicalParameters,
		se.CreatedAt
	FROM StructuralElement se
	JOIN Project p ON se.ProjectId=p.ProjectId
	WHERE NOT EXISTS (
		SELECT 1
		FROM Calculation c
		WHERE c.ElementId = se.ElementID
	);
GO

CREATE   VIEW [dbo].[vw_ElementsWithoutMaterials] AS
SELECT
	se.ProjectId,
	p.ProjectName,
	se.ElementId,
	se.Name AS ElementName
FROM StructuralElement se
JOIN Project p ON p.ProjectID = se.ProjectID
WHERE NOT EXISTS (
	SELECT 1
	FROM MaterialUsage mu
	WHERE mu.ElementId = se.ElementId
)
GO

CREATE   VIEW [dbo].[vw_LatestCalculationsPerElement] AS
WITH base AS (
		SELECT
			se.ElementId,
			se.ElementTypeId,
			se.Name,
			se.Dimensions,
			c.CalculationId,
			c.BendingMoment,
			c.AxialForce,
			c.LoadValue,
			c.LoadCapacityFactor,
			c.CreatedAt
		FROM Calculation c
		JOIN StructuralElement se ON se.ElementId=c.ElementId
	),
	ranks AS (
		SELECT
			*,
			ROW_NUMBER() OVER (
				PARTITION BY ElementId
				ORDER BY CreatedAt DESC, CalculationId DESC
			) AS ranked
		FROM base
	)
	SELECT
		ElementId,
		ElementTypeId,
		Name,
		Dimensions,
		CalculationId,
		BendingMoment,
		AxialForce,
		LoadValue,
		LoadCapacityFactor,
		CreatedAt,
		CAST(CASE 
				WHEN ranked = 1 THEN 1
				ELSE 0
			END AS BIT) AS isLatest
	FROM ranks
GO

CREATE   VIEW [dbo].[vw_MaterialUsagePerProject] AS
WITH muAgg AS (
	SELECT
		mu.ElementId,
		mu.MaterialId,
		mu.UnitId,
		SUM(mu.Quantity) AS Quantity
	FROM MaterialUsage mu
	GROUP BY mu.ElementId, mu.MaterialId, mu.UnitId
)
SELECT
	p.ProjectId,
	p.ProjectName,
	m.MaterialId,
	m.Name AS MaterialName,
	u.UnitId,
	u.Name AS UnitName,
	SUM(muAgg.Quantity) AS TotalQuantity
FROM muAgg
JOIN StructuralElement se ON muAgg.ElementId = se.ElementId
JOIN Project p ON se.ProjectId = p.ProjectId
JOIN Material m ON muAgg.MaterialId = m.MaterialId
JOIN Unit u ON muAgg.UnitId = u.UnitId
GROUP BY
	p.ProjectId,
	p.ProjectName,
	m.MaterialId,
	m.Name,
	u.UnitId,
	u.Name
GO

CREATE   VIEW [dbo].[vw_ProjectDashboardAdvanced]
AS

WITH elementsCTE AS (
    SELECT
        ProjectId,
        COUNT(*) AS ElementsCount
    FROM StructuralElement
    GROUP BY ProjectId
),

calculationsCTE AS (
    SELECT
        se.ProjectId,
        COUNT(*) AS CalculationsCount
    FROM Calculation c
    JOIN StructuralElement se
        ON se.ElementId = c.ElementId
    GROUP BY se.ProjectId
),

notesCTE AS (
    SELECT
        ProjectId,
        COUNT(*) AS NotesCount
    FROM Note
    GROUP BY ProjectId
),

materialsCTE AS (
    SELECT
        se.ProjectId,
        SUM(mu.Quantity) AS TotalMaterialQuantity
    FROM MaterialUsage mu
    JOIN StructuralElement se
        ON se.ElementId = mu.ElementId
    GROUP BY se.ProjectId
)

SELECT
    p.ProjectId,
    p.ProjectName,
    p.Scope,
    p.Location,
    p.Status,
    p.DueDate,
    e.ElementsCount,
    c.CalculationsCount,
    n.NotesCount,
    m.TotalMaterialQuantity,
    CASE
        WHEN p.DueDate < GETDATE() THEN 'Overdue'
        ELSE 'In Progress'
    END AS ScheduleStatus

FROM Project p

LEFT JOIN elementsCTE e
    ON e.ProjectId = p.ProjectId

LEFT JOIN calculationsCTE c
    ON c.ProjectId = p.ProjectId

LEFT JOIN notesCTE n
    ON n.ProjectId = p.ProjectId

LEFT JOIN materialsCTE m
    ON m.ProjectId = p.ProjectId;
GO

CREATE   VIEW [dbo].[vw_ProjectDashboardSummary] AS
SELECT
    p.ProjectId,
    p.ProjectName,
    COUNT(DISTINCT se.ElementId) AS ElementsCount,
    COUNT(DISTINCT c.CalculationId) AS CalculationsCount,
    COUNT(DISTINCT n.NoteId) AS NotesCount,
    SUM(DISTINCT mu.Quantity) AS TotalMaterialQuantity
FROM Project p
LEFT JOIN StructuralElement se 
    ON se.ProjectId = p.ProjectId
LEFT JOIN Calculation c 
    ON c.ElementId = se.ElementId
LEFT JOIN MaterialUsage mu 
    ON mu.ElementId = se.ElementId
LEFT JOIN Note n 
    ON n.ProjectId = p.ProjectId
GROUP BY 
    p.ProjectId,
    p.ProjectName;
GO

CREATE   VIEW [dbo].[vw_ProjectHealthStatus] AS
SELECT
    se.ProjectId,
    p.ProjectName,
    COUNT(DISTINCT se.ElementId) AS ElementsCount,
    COUNT(DISTINCT c.ElementId) AS CalculationsCount,
    CASE
        WHEN COUNT(DISTINCT c.ElementId) = 0 THEN 'HIGH RISK'
        WHEN COUNT(DISTINCT c.ElementId) < COUNT(DISTINCT se.ElementId) THEN 'MEDIUM RISK'
        ELSE 'LOW RISK'
    END AS ProjectHealth
FROM StructuralElement se
LEFT JOIN Calculation c ON c.ElementId = se.ElementId
JOIN Project p ON se.ProjectId = p.ProjectId
GROUP BY se.ProjectId, p.ProjectName
GO

CREATE   VIEW [dbo].[vw_ProjectLastActivity] AS
WITH calcsCTE AS (
    SELECT
        se.ProjectId,
        MAX(c.CreatedAt) AS LastCalculationsDate
    FROM Calculation c
    JOIN StructuralElement se ON c.ElementId = se.ElementId
    GROUP BY se.ProjectId
),
notesCTE AS (
    SELECT
        n.ProjectId,
        MAX(n.CreatedAt) AS LastNotesDate
    FROM Note n
    GROUP BY n.ProjectId
),
elementsCTE AS (
    SELECT
        se.ProjectId,
        MAX(se.CreatedAt) AS LastElementDate
    FROM StructuralElement se
    GROUP BY se.ProjectId
)
SELECT
    ec.ProjectId,
    p.ProjectName,
    (
        SELECT MAX(x)
        FROM (VALUES 
            (cc.LastCalculationsDate),
            (nc.LastNotesDate),
            (ec.LastElementDate)
        ) t(x)
    ) AS LastActivityDate
FROM elementsCTE ec
LEFT JOIN calcsCTE cc ON ec.ProjectId = cc.ProjectId
LEFT JOIN notesCTE nc ON ec.ProjectId = nc.ProjectId
JOIN Project p ON ec.ProjectId = p.ProjectId
GO

CREATE   VIEW [dbo].[vw_ProjectProgress] AS
SELECT
    se.ProjectId,
    p.ProjectName,
    COUNT(DISTINCT se.ElementId) AS TotalElements,
    COUNT(DISTINCT c.ElementId) AS ElementsWithCalculations,
    ROUND (
    	COUNT(DISTINCT c.ElementId) * 100.0 /
    		COUNT(DISTINCT se.ElementId), 2
    		) AS ProgressPct
FROM StructuralElement se
LEFT JOIN Calculation c ON c.ElementId = se.ElementId
LEFT JOIN Project p ON se.ProjectId = p.ProjectId
GROUP BY se.ProjectId, p.ProjectName
GO

CREATE   VIEW [dbo].[vw_ProjectStructuralCoverage] AS
WITH totalElements AS (
	SELECT
		se.ProjectId,
		COUNT(DISTINCT se.ElementId) AS TotalElements
	FROM StructuralElement se
	GROUP BY se.ProjectId
),
elementsCalculationsCount AS (
	SELECT
		se.ProjectId,
		COUNT(DISTINCT c.ElementId) AS ElementsWithCalculations
	FROM Calculation c
	JOIN StructuralElement se ON c.ElementId = se.ElementId
	GROUP BY se.ProjectId
),
elementsMaterialsCount AS (
	SELECT
		se.ProjectId,
		COUNT(DISTINCT mu.ElementId) AS ElementsWithMaterials
	FROM MaterialUsage mu
	JOIN StructuralElement se ON mu.ElementId = se.ElementId
	GROUP BY se.ProjectId
),
notesCount AS (
	SELECT
		n.ProjectId,
		COUNT(DISTINCT n.NoteId) AS NotesCount
	FROM Note n
	GROUP BY n.ProjectId
)
SELECT
	p.ProjectId,
	p.ProjectName,
	te.TotalElements,
	ecc.ElementsWithCalculations,
	emc.ElementsWithMaterials,
	nc.NotesCount,
	ROUND(ISNULL(ecc.ElementsWithCalculations, 0) * 100.0 / 
		NULLIF(te.TotalElements, 0), 2) AS CoverageCalculationsPct,
	ROUND(ISNULL(emc.ElementsWithMaterials, 0) * 100.0 / 
		NULLIF(te.TotalElements, 0), 2) AS CoverageMaterialPct
FROM Project p
LEFT JOIN totalElements te ON p.ProjectId = te.ProjectId
LEFT JOIN elementsCalculationsCount ecc ON p.ProjectId = ecc.ProjectId
LEFT JOIN elementsMaterialsCount emc ON p.ProjectId = emc.ProjectId
LEFT JOIN notesCount nc ON p.ProjectId = nc.ProjectId
GO

CREATE   VIEW [dbo].[vw_TopMaterialsPerProject] AS
WITH base AS (
    SELECT
        se.ProjectId,
        mt.Name AS MaterialTypeName,
        m.Name AS MaterialName,
        u.Symbol,
        SUM(mu.Quantity) AS TotalQuantity
    FROM MaterialUsage mu
    JOIN Material m ON mu.MaterialId = m.MaterialId
    JOIN MaterialType mt ON m.MaterialTypeId = mt.MaterialTypeId
    JOIN StructuralElement se ON mu.ElementId = se.ElementId
    JOIN Unit u ON mu.UnitId = u.UnitId
    GROUP BY
        se.ProjectId,
        mt.Name,
        m.Name,
        u.Symbol
),
agg AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY ProjectId
            ORDER BY TotalQuantity DESC
        ) AS ranked,
        SUM(TotalQuantity) OVER (
			PARTITION BY ProjectID
		) AS ProjectTotal
    FROM base
)
SELECT
	ProjectId,
	MaterialTypeName,
	MaterialName,
	Symbol,
	totalQuantity * 1.0 / ProjectTotal AS SharePCT
FROM agg
WHERE ranked <= 1
GO

CREATE   VIEW [dbo].[vw_ProjectAlerts] AS
SELECT
	p.ProjectId,
    p.ProjectName,
	1 AS AlertType,
	'Low project activity' AS AlertMessage
FROM Project p
JOIN vw_ProjectLastActivity vpla ON vpla.ProjectId = p.ProjectId
WHERE vpla.LastActivityDate < DATEADD(DAY, -30, GETDATE())
UNION ALL
SELECT
	p.ProjectId,
	p.ProjectName,
	2 AS AlertType,
	'Low project progress'
FROM Project p
JOIN vw_ProjectProgress vpp ON vpp.ProjectId = p.ProjectId
WHERE vpp.ProgressPct < 50.0
UNION ALL
SELECT DISTINCT
    p.ProjectId,
    p.ProjectName,
    3 AS AlertType,
    'Elements without calculations'
FROM Project p
JOIN vw_ElementsWithoutCalculations v ON v.ProjectId = p.ProjectId
UNION ALL
SELECT DISTINCT
    p.ProjectId,
    p.ProjectName,
    4 AS AlertType,
    'Elements without materials'
FROM Project p
JOIN vw_ElementsWithoutMaterials v ON v.ProjectId = p.ProjectId
GO

CREATE   VIEW [dbo].[vw_ProjectBottlenecks] AS
WITH totalElements AS (
	SELECT
		se.ProjectId,
		COUNT(DISTINCT se.ElementId) AS TotalElements
	FROM StructuralElement se
	GROUP BY se.ProjectId
),
elementsWithCalcs AS (
	SELECT
		se.ProjectId,
		COUNT(DISTINCT c.ElementId) AS ElementsWithCalcs
	FROM Calculation c
	JOIN StructuralElement se ON c.ElementId = se.ElementId
	GROUP BY se.ProjectId
),
elementsWithMaterials AS (
	SELECT
		se.ProjectId,
		COUNT(DISTINCT mu.ElementId) AS ElementsWithMaterials
	FROM MaterialUsage mu
	JOIN StructuralElement se ON mu.ElementId = se.ElementId
	GROUP BY se.ProjectId
),
baseMetrics AS (
	SELECT
		p.ProjectId,
		p.ProjectName,
		ISNULL(te.TotalElements, 0) - ISNULL(ewc.ElementsWithCalcs, 0) AS ElementsWithoutCalcs,
		ISNULL(te.TotalElements,0) - ISNULL(ewm.ElementsWithMaterials, 0) AS ElementsWithoutMaterials,
		ROUND(((te.TotalElements - ISNULL(ewc.ElementsWithCalcs, 0)) * 100.0)
			/ NULLIF(te.TotalElements, 0), 2) AS MissingCalcsPct,
		ROUND(((te.TotalElements - ISNULL(ewm.ElementsWithMaterials, 0)) * 100.0)
			/ NULLIF(te.TotalElements, 0), 2) AS MissingMaterialsPct,
		vpp.ProgressPct,
		DATEDIFF(DAY, vpla.LastActivityDate, GETDATE()) AS DaysSinceLastActivity,
		DATEDIFF(DAY, GETDATE(), p.DueDate) AS DaysToDeadline
	FROM Project p
	LEFT JOIN totalElements te ON p.ProjectId = te.ProjectId
	LEFT JOIN elementsWithCalcs ewc ON p.ProjectId = ewc.ProjectId
	LEFT JOIN elementsWithMaterials ewm ON p.ProjectId = ewm.ProjectId
	LEFT JOIN vw_ProjectProgress vpp ON p.ProjectId = vpp.ProjectId
	LEFT JOIN vw_ProjectLastActivity vpla ON p.ProjectId = vpla.ProjectId
)
SELECT
	ProjectId,
	ProjectName,
	ElementsWithoutCalcs,
	ElementsWithoutMaterials,
	MissingCalcsPct,
	MissingMaterialsPct,
	ProgressPct,
	DaysSinceLastActivity,
	DaysToDeadline,
	CASE
		WHEN DaysToDeadline < 0 AND ProgressPct < 50 THEN 'DEADLINE RISK'
		WHEN MissingCalcsPct > 40 THEN 'MISSING CALCULATIONS'
		WHEN MissingMaterialsPct > 30 THEN 'MISSING MATERIALS'
		WHEN DaysSinceLastActivity > 14 THEN 'LOW ACTIVITY'
		ELSE 'STABLE'
	END AS MainBottleneck,
	CASE
		WHEN DaysToDeadline < 0 AND ProgressPct < 50 THEN 'HIGH'
		WHEN MissingCalcsPct > 50 THEN 'HIGH'
		WHEN MissingMaterialsPct > 50 THEN 'HIGH'
		WHEN DaysSinceLastActivity > 30 THEN 'MEDIUM'
		ELSE 'LOW'
	END AS BottleneckSeverity
FROM baseMetrics
GO

CREATE   VIEW [dbo].[vw_ProjectFullDashboard]
AS

SELECT
    vpda.ProjectId,
    vpda.ProjectName,
    vpda.[Scope],
    vpda.Location,
    vpda.Status,
    vpda.DueDate,
    vpda.ScheduleStatus,
    ISNULL(vpda.ElementsCount, 0) AS ElementsCount,
    ISNULL(vpda.CalculationsCount, 0) AS CalculationsCount,
    ISNULL(vpda.NotesCount, 0) AS NotesCount,
    ISNULL(vpp.ProgressPct, 0) AS ProgressPct,
    ISNULL(vphs.ProjectHealth, 'UNKNOWN') AS HealthStatus,
    ISNULL(vpda.TotalMaterialQuantity, 0) AS TotalMaterialQuantity,
    vpla.LastActivityDate,
    CASE
        WHEN vpla.LastActivityDate < DATEADD(DAY, -30, GETDATE())
            THEN 'Frozen'
        ELSE 'Active'
    END AS ActivityStatus

FROM vw_ProjectDashboardAdvanced vpda

LEFT JOIN vw_ProjectHealthStatus vphs
    ON vpda.ProjectId = vphs.ProjectId

LEFT JOIN vw_ProjectProgress vpp
    ON vpda.ProjectId = vpp.ProjectId

LEFT JOIN vw_ProjectLastActivity vpla
    ON vpda.ProjectId = vpla.ProjectId;
GO

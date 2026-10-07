-- Construction Management API - stored procedures

CREATE   PROCEDURE [dbo].[sp_AddCalculations]
    @ElementId INT,
    @BendingMoment DECIMAL(18,4),
    @AxialForce DECIMAL(18,4),
    @LoadValue DECIMAL(18,4),
    @LoadCapacityFactor DECIMAL(10,4)
AS
BEGIN
	-- validation if element exists
	IF NOT EXISTS (
		SELECT 1
		FROM StructuralElement
		WHERE ElementId = @ElementId
	)
	BEGIN
		THROW 50001, 'The element with the given id does not exist.', 1;
	END;

    INSERT INTO Calculation
    (ElementId, BendingMoment, AxialForce, LoadValue, LoadCapacityFactor)
    OUTPUT INSERTED.CalculationId
    VALUES
    (@ElementId, @BendingMoment, @AxialForce, @LoadValue, @LoadCapacityFactor);
END;
GO

CREATE   PROCEDURE [dbo].[sp_AddStructuralElement]
    @ProjectId INT,
    @ElementTypeId INT,
    @Name NVARCHAR(150),
    @Dimensions NVARCHAR(200),
    @TechnicalParameters NVARCHAR(MAX)
AS
BEGIN
	-- validation if project exists
	IF NOT EXISTS(
		SELECT 1
		FROM Project
		WHERE ProjectId = @ProjectId
	)
	BEGIN
		THROW 50001, 'The project with the given id does not exist.', 1;
	END;

    INSERT INTO StructuralElement
    (ProjectId, ElementTypeId, Name, Dimensions, TechnicalParameters)
    OUTPUT INSERTED.ElementId
    VALUES
    (@ProjectId, @ElementTypeId, @Name, @Dimensions, @TechnicalParameters);
END;
GO

CREATE   PROCEDURE [dbo].[sp_AssignUserToProject]
	@ProjectId INT,
	@UserId INT
AS
BEGIN
	SET NOCOUNT ON;
	BEGIN TRY
		-- validation if project exists
		IF NOT EXISTS (
			SELECT 1
			FROM Project
			WHERE ProjectId = @ProjectId
		)
		BEGIN
			THROW 50001, 'The project with the given id does not exist.', 1;
		END;
		-- validation if user exists
		IF NOT EXISTS (
			SELECT 1
			FROM [User]
			WHERE UserId = @UserId
		)
		BEGIN
			THROW 50002, 'The user with the given id does not exist.', 1;
		END;
		-- validation if user is active
		IF NOT EXISTS (
			SELECT 1
			FROM [User]
			WHERE IsActive = 1
			AND UserId = @UserId
		)
		BEGIN
			THROW 50003, 'The user with the given id is not active.', 1;
		END;
		-- validation if user is already assigned to the project
		IF EXISTS (
			SELECT 1
			FROM ProjectUser
			WHERE ProjectId = @ProjectId
			AND UserId = @UserId
		)
		BEGIN
			THROW 50004, 'The user is already assigned to the project.', 1;
		END;
		-- validation if user is assigned to the project as ADMIN
		IF EXISTS (
			SELECT 1
			FROM [User]
			WHERE UserId = @UserId
			AND Role = 'ADMIN'
		)
		BEGIN
			THROW 50005, 'You cannot assign user as ADMIN.', 1;
		END;
		BEGIN TRANSACTION
			INSERT INTO ProjectUser (ProjectId, UserId, ProjectRole)
			SELECT
				@ProjectId,
				@UserId,
				[Role]
			FROM [User]
			WHERE UserId = @UserId
		COMMIT TRANSACTION
		-- message if user assigned
		SELECT 'User assigned to project successfully.' AS Message;
	END TRY
		BEGIN CATCH
			IF @@TRANCOUNT > 0
				ROLLBACK TRANSACTION;
		THROW; 
	END CATCH
END
GO

CREATE   PROCEDURE [dbo].[sp_CloseProjectSafely]
    @ProjectId INT
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY

        -- Validate that the project exists
        IF NOT EXISTS (
            SELECT 1
            FROM Project
            WHERE ProjectId = @ProjectId
        )
        BEGIN
            THROW 50001, 'The project with the given ID does not exist.', 1;
        END;

        -- Validate that the project is not already completed
        IF EXISTS (
            SELECT 1
            FROM Project
            WHERE Status = 'Completed'
              AND ProjectId = @ProjectId
        )
        BEGIN
            THROW 50002, 'The project with the given ID already has status: COMPLETED.', 1;
        END;

        -- Validate that all structural elements have calculations
        IF EXISTS (
            SELECT 1
            FROM vw_ElementsWithoutCalculations
            WHERE ProjectId = @ProjectId
        )
        BEGIN
            THROW 50003, 'The project with the given ID has elements without assigned calculations.', 1;
        END;

        -- Validate that all structural elements have materials
        IF EXISTS (
            SELECT 1
            FROM vw_ElementsWithoutMaterials
            WHERE ProjectId = @ProjectId
        )
        BEGIN
            THROW 50004, 'The project with the given ID has elements without assigned materials.', 1;
        END;

        BEGIN TRANSACTION;

            UPDATE Project
            SET Status = 'Completed'
            WHERE ProjectId = @ProjectId;

        COMMIT TRANSACTION;

        -- Return confirmation message
        SELECT 'Project status updated successfully.' AS Message;

    END TRY

    BEGIN CATCH

        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        THROW;

    END CATCH
END;
GO

CREATE   PROCEDURE [dbo].[sp_GetProjectFullSummary]
	@ProjectId INT
AS
BEGIN
	IF NOT EXISTS (
		SELECT 1
		FROM Project
		WHERE ProjectId = @ProjectId
	)
	BEGIN
		THROW 50001, 'The project with the given id does not exists.', 1;
	END;
	SELECT * FROM vw_ProjectDashboardAdvanced
	WHERE ProjectId = @ProjectId;
END;
GO

CREATE   PROCEDURE [dbo].[sp_GetTopMaterialPerProject]
	@ProjectID INT,
	@TopN INT
AS
BEGIN
	IF NOT EXISTS(
		SELECT 1
		FROM Project
		WHERE ProjectId = @ProjectID
	)
	BEGIN
		THROW 50001, 'The project with the given id does not exists.', 1
	END;

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
	    WHERE se.ProjectId = @ProjectID
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
				PARTITION BY ProjectId
			) AS ProjectTotal
	    FROM base
	)
	SELECT
		ProjectId,
		MaterialTypeName,
		MaterialName,
		Symbol,
		CAST(totalQuantity * 1.0 / ProjectTotal AS DECIMAL(10,2)) AS SharePCT
	FROM agg
	WHERE ranked <= @TopN
	ORDER BY TotalQuantity DESC
END;
GO

CREATE   PROCEDURE [dbo].[sp_UpdateProjectStatus]
    @ProjectId INT,
    @NewStatus NVARCHAR(50)
AS
BEGIN
	-- validation if project exists
	IF NOT EXISTS (
		SELECT 1
		FROM Project
		WHERE ProjectId = @ProjectId
	)
	BEGIN
		THROW 50001, 'The project with the given id does not exists.', 1;
	END;
    UPDATE Project
    SET Status = @NewStatus
    WHERE ProjectId = @ProjectId;
END;
GO

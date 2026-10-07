-- Construction Management API - seed data
-- Demo/portfolio data used by the application and integration tests.

SET IDENTITY_INSERT [dbo].[ElementType] ON
GO
INSERT [dbo].[ElementType] ([ElementTypeId], [Name]) VALUES (1, N'Beam')
INSERT [dbo].[ElementType] ([ElementTypeId], [Name]) VALUES (2, N'Column')
INSERT [dbo].[ElementType] ([ElementTypeId], [Name]) VALUES (3, N'Foundation')
INSERT [dbo].[ElementType] ([ElementTypeId], [Name]) VALUES (4, N'Slab')
GO
SET IDENTITY_INSERT [dbo].[ElementType] OFF
GO
SET IDENTITY_INSERT [dbo].[MaterialType] ON
GO
INSERT [dbo].[MaterialType] ([MaterialTypeId], [Name]) VALUES (1, N'Concrete')
INSERT [dbo].[MaterialType] ([MaterialTypeId], [Name]) VALUES (2, N'Steel')
GO
SET IDENTITY_INSERT [dbo].[MaterialType] OFF
GO
SET IDENTITY_INSERT [dbo].[Unit] ON
GO
INSERT [dbo].[Unit] ([UnitId], [Name], [Symbol]) VALUES (1, N'Cubic meter', N'm3')
INSERT [dbo].[Unit] ([UnitId], [Name], [Symbol]) VALUES (2, N'Kilogram', N'kg')
INSERT [dbo].[Unit] ([UnitId], [Name], [Symbol]) VALUES (3, N'Tonne', N't')
GO
SET IDENTITY_INSERT [dbo].[Unit] OFF
GO
SET IDENTITY_INSERT [dbo].[User] ON
GO
INSERT [dbo].[User] ([UserId], [FirstName], [LastName], [Email], [Role], [IsActive], [CreatedAt], [PasswordHash], [LastLogin]) VALUES (1, N'John', N'Carter', N'john.carter@example.com', N'ADMIN', 1, CAST(N'2026-08-01T09:00:00.0000000' AS DateTime2), N'$2y$12$bPw4oc7Ez13mJaqrw1C/8uby058LbA.ZcV/Hdg2GJ3VJ5rlrfP0/a', NULL)
INSERT [dbo].[User] ([UserId], [FirstName], [LastName], [Email], [Role], [IsActive], [CreatedAt], [PasswordHash], [LastLogin]) VALUES (2, N'Emily', N'Wilson', N'emily.wilson@example.com', N'DESIGNER', 1, CAST(N'2026-08-01T09:05:00.0000000' AS DateTime2), N'$2y$12$bPw4oc7Ez13mJaqrw1C/8uby058LbA.ZcV/Hdg2GJ3VJ5rlrfP0/a', CAST(N'2026-09-30T08:42:00.0000000' AS DateTime2))
INSERT [dbo].[User] ([UserId], [FirstName], [LastName], [Email], [Role], [IsActive], [CreatedAt], [PasswordHash], [LastLogin]) VALUES (3, N'Daniel', N'Brown', N'daniel.brown@example.com', N'ASSISTANT', 1, CAST(N'2026-08-01T09:10:00.0000000' AS DateTime2), N'$2y$12$bPw4oc7Ez13mJaqrw1C/8uby058LbA.ZcV/Hdg2GJ3VJ5rlrfP0/a', CAST(N'2026-09-29T14:15:00.0000000' AS DateTime2))
GO
SET IDENTITY_INSERT [dbo].[User] OFF
GO
SET IDENTITY_INSERT [dbo].[Project] ON
GO
INSERT [dbo].[Project] ([ProjectId], [ProjectName], [Scope], [Location], [Status], [DueDate], [CreatedAt]) VALUES (1, N'Riverside Residential Building', N'Structural design of a multi-storey residential building', N'Krakow', N'In Progress', CAST(N'2026-12-15' AS Date), CAST(N'2026-08-05T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[Project] ([ProjectId], [ProjectName], [Scope], [Location], [Status], [DueDate], [CreatedAt]) VALUES (2, N'North Logistics Warehouse', N'Structural design of a logistics warehouse', N'Warsaw', N'In Progress', CAST(N'2026-11-30' AS Date), CAST(N'2026-08-12T10:30:00.0000000' AS DateTime2))
INSERT [dbo].[Project] ([ProjectId], [ProjectName], [Scope], [Location], [Status], [DueDate], [CreatedAt]) VALUES (3, N'Central Office Building', N'Structural design of a six-storey office building', N'Wroclaw', N'New', CAST(N'2027-03-31' AS Date), CAST(N'2026-09-15T11:00:00.0000000' AS DateTime2))
INSERT [dbo].[Project] ([ProjectId], [ProjectName], [Scope], [Location], [Status], [DueDate], [CreatedAt]) VALUES (4, N'East Industrial Hall', N'Structural design of an industrial production hall', N'Gdansk', N'On Hold', CAST(N'2026-10-31' AS Date), CAST(N'2026-07-10T09:30:00.0000000' AS DateTime2))
INSERT [dbo].[Project] ([ProjectId], [ProjectName], [Scope], [Location], [Status], [DueDate], [CreatedAt]) VALUES (5, N'Park Residential Complex', N'Structural design of a residential complex', N'Krakow', N'Completed', CAST(N'2026-06-30' AS Date), CAST(N'2026-04-01T08:45:00.0000000' AS DateTime2))
GO
SET IDENTITY_INSERT [dbo].[Project] OFF
GO
INSERT [dbo].[ProjectUser] ([ProjectId], [UserId], [ProjectRole]) VALUES (1, 2, N'DESIGNER')
INSERT [dbo].[ProjectUser] ([ProjectId], [UserId], [ProjectRole]) VALUES (1, 3, N'ASSISTANT')
INSERT [dbo].[ProjectUser] ([ProjectId], [UserId], [ProjectRole]) VALUES (2, 2, N'DESIGNER')
INSERT [dbo].[ProjectUser] ([ProjectId], [UserId], [ProjectRole]) VALUES (2, 3, N'ASSISTANT')
INSERT [dbo].[ProjectUser] ([ProjectId], [UserId], [ProjectRole]) VALUES (3, 2, N'DESIGNER')
INSERT [dbo].[ProjectUser] ([ProjectId], [UserId], [ProjectRole]) VALUES (4, 2, N'DESIGNER')
INSERT [dbo].[ProjectUser] ([ProjectId], [UserId], [ProjectRole]) VALUES (4, 3, N'ASSISTANT')
INSERT [dbo].[ProjectUser] ([ProjectId], [UserId], [ProjectRole]) VALUES (5, 2, N'DESIGNER')
INSERT [dbo].[ProjectUser] ([ProjectId], [UserId], [ProjectRole]) VALUES (5, 3, N'ASSISTANT')
GO
SET IDENTITY_INSERT [dbo].[Material] ON
GO
INSERT [dbo].[Material] ([MaterialId], [Name], [MaterialTypeId]) VALUES (1, N'C30/37', 1)
INSERT [dbo].[Material] ([MaterialId], [Name], [MaterialTypeId]) VALUES (2, N'C25/30', 1)
INSERT [dbo].[Material] ([MaterialId], [Name], [MaterialTypeId]) VALUES (3, N'B500B', 2)
INSERT [dbo].[Material] ([MaterialId], [Name], [MaterialTypeId]) VALUES (4, N'S355', 2)
GO
SET IDENTITY_INSERT [dbo].[Material] OFF
GO
INSERT [dbo].[MaterialUnit] ([MaterialId], [UnitId]) VALUES (1, 1)
INSERT [dbo].[MaterialUnit] ([MaterialId], [UnitId]) VALUES (2, 1)
INSERT [dbo].[MaterialUnit] ([MaterialId], [UnitId]) VALUES (3, 2)
INSERT [dbo].[MaterialUnit] ([MaterialId], [UnitId]) VALUES (3, 3)
INSERT [dbo].[MaterialUnit] ([MaterialId], [UnitId]) VALUES (4, 2)
INSERT [dbo].[MaterialUnit] ([MaterialId], [UnitId]) VALUES (4, 3)
GO
SET IDENTITY_INSERT [dbo].[StructuralElement] ON
GO
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (1, 1, 1, N'B-01', N'300 x 6000 mm', N'Reinforced concrete beam; span 6.0 m; concrete C30/37; reinforcement B500B', CAST(N'2026-08-06T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (2, 1, 2, N'C-01', N'400 x 400 x 3200 mm', N'Reinforced concrete column; height 3.2 m; concrete C30/37; reinforcement B500B', CAST(N'2026-08-06T10:15:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (3, 1, 3, N'F-01', N'2200 x 2200 x 500 mm', N'Pad foundation; concrete C25/30; foundation depth 500 mm', CAST(N'2026-08-07T09:00:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (4, 1, 4, N'S-01', N'6000 x 6000 x 180 mm', N'Reinforced concrete slab; span 6.0 m; thickness 180 mm; concrete C30/37', CAST(N'2026-08-08T11:30:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (5, 2, 1, N'B-02', N'350 x 8000 mm', N'Reinforced concrete beam; span 8.0 m; concrete C30/37; reinforcement B500B', CAST(N'2026-08-13T09:00:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (6, 2, 2, N'C-02', N'500 x 500 x 5000 mm', N'Reinforced concrete column; height 5.0 m; concrete C30/37', CAST(N'2026-08-13T09:20:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (7, 2, 3, N'F-02', N'2500 x 2500 x 600 mm', N'Pad foundation; concrete C25/30; foundation depth 600 mm', CAST(N'2026-08-14T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (8, 2, 4, N'S-02', N'8000 x 8000 x 200 mm', N'Reinforced concrete slab; span 8.0 m; thickness 200 mm; concrete C30/37', CAST(N'2026-08-15T12:00:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (9, 3, 1, N'B-03', N'300 x 7000 mm', N'Reinforced concrete beam; span 7.0 m; concrete C30/37', CAST(N'2026-09-16T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (10, 3, 2, N'C-03', N'400 x 400 x 3200 mm', N'Reinforced concrete column; height 3.2 m; concrete C30/37', CAST(N'2026-09-16T10:30:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (11, 3, 4, N'S-03', N'7000 x 7000 x 180 mm', N'Reinforced concrete slab; span 7.0 m; thickness 180 mm; concrete C30/37', CAST(N'2026-09-17T09:00:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (12, 4, 1, N'B-04', N'400 x 10000 mm', N'Reinforced concrete beam; span 10.0 m; concrete C30/37; reinforcement B500B', CAST(N'2026-07-11T09:00:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (13, 4, 2, N'C-04', N'500 x 500 x 6000 mm', N'Reinforced concrete column; height 6.0 m; concrete C30/37', CAST(N'2026-07-11T09:30:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (14, 4, 3, N'F-04', N'3000 x 3000 x 700 mm', N'Pad foundation; concrete C25/30; foundation depth 700 mm', CAST(N'2026-07-12T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (15, 5, 1, N'B-05', N'300 x 6500 mm', N'Reinforced concrete beam; span 6.5 m; concrete C30/37', CAST(N'2026-04-05T09:00:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (16, 5, 2, N'C-05', N'400 x 400 x 3200 mm', N'Reinforced concrete column; height 3.2 m; concrete C30/37', CAST(N'2026-04-05T09:20:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (17, 5, 3, N'F-05', N'2200 x 2200 x 500 mm', N'Pad foundation; concrete C25/30; foundation depth 500 mm', CAST(N'2026-04-06T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[StructuralElement] ([ElementId], [ProjectId], [ElementTypeId], [Name], [Dimensions], [TechnicalParameters], [CreatedAt]) VALUES (18, 5, 4, N'S-05', N'6500 x 6500 x 180 mm', N'Reinforced concrete slab; span 6.5 m; thickness 180 mm; concrete C30/37', CAST(N'2026-04-07T11:00:00.0000000' AS DateTime2))
GO
SET IDENTITY_INSERT [dbo].[StructuralElement] OFF
GO
SET IDENTITY_INSERT [dbo].[Calculation] ON
GO
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (1, 1, CAST(120.5000 AS Decimal(18, 4)), CAST(50.2000 AS Decimal(18, 4)), CAST(200.0000 AS Decimal(18, 4)), CAST(1.2000 AS Decimal(10, 4)), CAST(N'2026-08-10T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (2, 1, CAST(135.0000 AS Decimal(18, 4)), CAST(55.0000 AS Decimal(18, 4)), CAST(210.0000 AS Decimal(18, 4)), CAST(1.3000 AS Decimal(10, 4)), CAST(N'2026-08-12T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (3, 2, CAST(100.0000 AS Decimal(18, 4)), CAST(40.0000 AS Decimal(18, 4)), CAST(180.0000 AS Decimal(18, 4)), CAST(1.1000 AS Decimal(10, 4)), CAST(N'2026-08-11T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (4, 3, CAST(90.0000 AS Decimal(18, 4)), CAST(70.0000 AS Decimal(18, 4)), CAST(160.0000 AS Decimal(18, 4)), CAST(1.0000 AS Decimal(10, 4)), CAST(N'2026-08-12T11:00:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (5, 4, CAST(180.0000 AS Decimal(18, 4)), CAST(90.0000 AS Decimal(18, 4)), CAST(250.0000 AS Decimal(18, 4)), CAST(1.4000 AS Decimal(10, 4)), CAST(N'2026-08-13T11:00:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (6, 5, CAST(150.0000 AS Decimal(18, 4)), CAST(60.0000 AS Decimal(18, 4)), CAST(220.0000 AS Decimal(18, 4)), CAST(1.2000 AS Decimal(10, 4)), CAST(N'2026-08-18T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (7, 6, CAST(140.0000 AS Decimal(18, 4)), CAST(80.0000 AS Decimal(18, 4)), CAST(210.0000 AS Decimal(18, 4)), CAST(1.3000 AS Decimal(10, 4)), CAST(N'2026-08-18T11:00:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (8, 7, CAST(160.0000 AS Decimal(18, 4)), CAST(85.0000 AS Decimal(18, 4)), CAST(240.0000 AS Decimal(18, 4)), CAST(1.3500 AS Decimal(10, 4)), CAST(N'2026-08-19T09:00:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (9, 8, CAST(200.0000 AS Decimal(18, 4)), CAST(95.0000 AS Decimal(18, 4)), CAST(270.0000 AS Decimal(18, 4)), CAST(1.5000 AS Decimal(10, 4)), CAST(N'2026-08-20T09:30:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (10, 9, CAST(110.0000 AS Decimal(18, 4)), CAST(45.0000 AS Decimal(18, 4)), CAST(190.0000 AS Decimal(18, 4)), CAST(1.1500 AS Decimal(10, 4)), CAST(N'2026-09-20T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (11, 10, CAST(95.0000 AS Decimal(18, 4)), CAST(50.0000 AS Decimal(18, 4)), CAST(170.0000 AS Decimal(18, 4)), CAST(1.0500 AS Decimal(10, 4)), CAST(N'2026-09-20T10:30:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (12, 12, CAST(175.0000 AS Decimal(18, 4)), CAST(75.0000 AS Decimal(18, 4)), CAST(260.0000 AS Decimal(18, 4)), CAST(1.2500 AS Decimal(10, 4)), CAST(N'2026-07-20T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (13, 13, CAST(150.0000 AS Decimal(18, 4)), CAST(90.0000 AS Decimal(18, 4)), CAST(240.0000 AS Decimal(18, 4)), CAST(1.2000 AS Decimal(10, 4)), CAST(N'2026-07-21T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (14, 14, CAST(190.0000 AS Decimal(18, 4)), CAST(100.0000 AS Decimal(18, 4)), CAST(280.0000 AS Decimal(18, 4)), CAST(1.3500 AS Decimal(10, 4)), CAST(N'2026-07-22T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (15, 15, CAST(115.0000 AS Decimal(18, 4)), CAST(50.0000 AS Decimal(18, 4)), CAST(190.0000 AS Decimal(18, 4)), CAST(1.1000 AS Decimal(10, 4)), CAST(N'2026-04-10T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (16, 16, CAST(125.0000 AS Decimal(18, 4)), CAST(65.0000 AS Decimal(18, 4)), CAST(200.0000 AS Decimal(18, 4)), CAST(1.1500 AS Decimal(10, 4)), CAST(N'2026-04-10T10:30:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (17, 17, CAST(105.0000 AS Decimal(18, 4)), CAST(70.0000 AS Decimal(18, 4)), CAST(180.0000 AS Decimal(18, 4)), CAST(1.1000 AS Decimal(10, 4)), CAST(N'2026-04-11T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[Calculation] ([CalculationId], [ElementId], [BendingMoment], [AxialForce], [LoadValue], [LoadCapacityFactor], [CreatedAt]) VALUES (18, 18, CAST(160.0000 AS Decimal(18, 4)), CAST(80.0000 AS Decimal(18, 4)), CAST(230.0000 AS Decimal(18, 4)), CAST(1.2500 AS Decimal(10, 4)), CAST(N'2026-04-12T10:00:00.0000000' AS DateTime2))
GO
SET IDENTITY_INSERT [dbo].[Calculation] OFF
GO
SET IDENTITY_INSERT [dbo].[MaterialUsage] ON
GO
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (1, 1, 1, CAST(12.5000 AS Decimal(18, 4)), CAST(N'2026-08-10T12:00:00.0000000' AS DateTime2), 1)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (1, 3, 2, CAST(420.0000 AS Decimal(18, 4)), CAST(N'2026-08-10T12:10:00.0000000' AS DateTime2), 2)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (2, 1, 1, CAST(8.0000 AS Decimal(18, 4)), CAST(N'2026-08-11T12:00:00.0000000' AS DateTime2), 3)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (2, 3, 2, CAST(350.0000 AS Decimal(18, 4)), CAST(N'2026-08-11T12:10:00.0000000' AS DateTime2), 4)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (3, 2, 1, CAST(18.0000 AS Decimal(18, 4)), CAST(N'2026-08-12T12:00:00.0000000' AS DateTime2), 5)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (3, 3, 2, CAST(500.0000 AS Decimal(18, 4)), CAST(N'2026-08-12T12:10:00.0000000' AS DateTime2), 6)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (4, 1, 1, CAST(9.5000 AS Decimal(18, 4)), CAST(N'2026-08-13T12:00:00.0000000' AS DateTime2), 7)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (4, 3, 2, CAST(300.0000 AS Decimal(18, 4)), CAST(N'2026-08-13T12:10:00.0000000' AS DateTime2), 8)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (5, 1, 1, CAST(15.0000 AS Decimal(18, 4)), CAST(N'2026-08-18T12:00:00.0000000' AS DateTime2), 9)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (5, 3, 2, CAST(550.0000 AS Decimal(18, 4)), CAST(N'2026-08-18T12:10:00.0000000' AS DateTime2), 10)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (6, 1, 1, CAST(11.0000 AS Decimal(18, 4)), CAST(N'2026-08-18T12:20:00.0000000' AS DateTime2), 11)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (6, 3, 2, CAST(450.0000 AS Decimal(18, 4)), CAST(N'2026-08-18T12:30:00.0000000' AS DateTime2), 12)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (7, 2, 1, CAST(22.0000 AS Decimal(18, 4)), CAST(N'2026-08-19T12:00:00.0000000' AS DateTime2), 13)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (7, 3, 2, CAST(650.0000 AS Decimal(18, 4)), CAST(N'2026-08-19T12:10:00.0000000' AS DateTime2), 14)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (8, 1, 1, CAST(20.0000 AS Decimal(18, 4)), CAST(N'2026-08-20T12:00:00.0000000' AS DateTime2), 15)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (8, 3, 2, CAST(700.0000 AS Decimal(18, 4)), CAST(N'2026-08-20T12:10:00.0000000' AS DateTime2), 16)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (9, 1, 1, CAST(10.0000 AS Decimal(18, 4)), CAST(N'2026-09-20T12:00:00.0000000' AS DateTime2), 17)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (10, 1, 1, CAST(8.0000 AS Decimal(18, 4)), CAST(N'2026-09-20T12:10:00.0000000' AS DateTime2), 18)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (12, 1, 1, CAST(20.0000 AS Decimal(18, 4)), CAST(N'2026-07-20T12:00:00.0000000' AS DateTime2), 19)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (12, 3, 2, CAST(900.0000 AS Decimal(18, 4)), CAST(N'2026-07-20T12:10:00.0000000' AS DateTime2), 20)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (13, 1, 1, CAST(14.0000 AS Decimal(18, 4)), CAST(N'2026-07-21T12:00:00.0000000' AS DateTime2), 21)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (13, 3, 2, CAST(500.0000 AS Decimal(18, 4)), CAST(N'2026-07-21T12:10:00.0000000' AS DateTime2), 22)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (14, 2, 1, CAST(28.0000 AS Decimal(18, 4)), CAST(N'2026-07-22T12:00:00.0000000' AS DateTime2), 23)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (14, 3, 2, CAST(800.0000 AS Decimal(18, 4)), CAST(N'2026-07-22T12:10:00.0000000' AS DateTime2), 24)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (15, 1, 1, CAST(13.0000 AS Decimal(18, 4)), CAST(N'2026-04-10T12:00:00.0000000' AS DateTime2), 25)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (15, 3, 2, CAST(450.0000 AS Decimal(18, 4)), CAST(N'2026-04-10T12:10:00.0000000' AS DateTime2), 26)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (16, 1, 1, CAST(9.0000 AS Decimal(18, 4)), CAST(N'2026-04-10T12:20:00.0000000' AS DateTime2), 27)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (16, 3, 2, CAST(380.0000 AS Decimal(18, 4)), CAST(N'2026-04-10T12:30:00.0000000' AS DateTime2), 28)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (17, 2, 1, CAST(20.0000 AS Decimal(18, 4)), CAST(N'2026-04-11T12:00:00.0000000' AS DateTime2), 29)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (17, 3, 2, CAST(600.0000 AS Decimal(18, 4)), CAST(N'2026-04-11T12:10:00.0000000' AS DateTime2), 30)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (18, 1, 1, CAST(16.0000 AS Decimal(18, 4)), CAST(N'2026-04-12T12:00:00.0000000' AS DateTime2), 31)
INSERT [dbo].[MaterialUsage] ([ElementId], [MaterialId], [UnitId], [Quantity], [UsedAt], [MaterialUsageId]) VALUES (18, 3, 2, CAST(520.0000 AS Decimal(18, 4)), CAST(N'2026-04-12T12:10:00.0000000' AS DateTime2), 32)
GO
SET IDENTITY_INSERT [dbo].[MaterialUsage] OFF
GO
SET IDENTITY_INSERT [dbo].[Note] ON
GO
INSERT [dbo].[Note] ([NoteId], [ProjectId], [UserId], [Content], [CreatedAt]) VALUES (1, 1, 2, N'Structural model review completed.', CAST(N'2026-08-15T14:00:00.0000000' AS DateTime2))
INSERT [dbo].[Note] ([NoteId], [ProjectId], [UserId], [Content], [CreatedAt]) VALUES (2, 1, 3, N'Column reinforcement requires verification.', CAST(N'2026-08-16T09:30:00.0000000' AS DateTime2))
INSERT [dbo].[Note] ([NoteId], [ProjectId], [UserId], [Content], [CreatedAt]) VALUES (3, 1, 2, N'Beam dimensions updated after load analysis.', CAST(N'2026-08-20T15:00:00.0000000' AS DateTime2))
INSERT [dbo].[Note] ([NoteId], [ProjectId], [UserId], [Content], [CreatedAt]) VALUES (4, 2, 2, N'Warehouse roof loads have been reviewed.', CAST(N'2026-08-21T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[Note] ([NoteId], [ProjectId], [UserId], [Content], [CreatedAt]) VALUES (5, 2, 3, N'Material quantities require final verification.', CAST(N'2026-08-22T11:00:00.0000000' AS DateTime2))
INSERT [dbo].[Note] ([NoteId], [ProjectId], [UserId], [Content], [CreatedAt]) VALUES (6, 3, 2, N'Initial structural concept prepared.', CAST(N'2026-09-18T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[Note] ([NoteId], [ProjectId], [UserId], [Content], [CreatedAt]) VALUES (7, 4, 2, N'Project is currently on hold pending client decision.', CAST(N'2026-07-25T10:00:00.0000000' AS DateTime2))
INSERT [dbo].[Note] ([NoteId], [ProjectId], [UserId], [Content], [CreatedAt]) VALUES (8, 5, 2, N'Final structural documentation approved.', CAST(N'2026-04-15T12:00:00.0000000' AS DateTime2))
INSERT [dbo].[Note] ([NoteId], [ProjectId], [UserId], [Content], [CreatedAt]) VALUES (9, 5, 3, N'Material quantities verified against the final model.', CAST(N'2026-04-16T13:00:00.0000000' AS DateTime2))
GO
SET IDENTITY_INSERT [dbo].[Note] OFF
GO

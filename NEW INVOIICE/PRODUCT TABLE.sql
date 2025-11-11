IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='TABLEPRODUCT' AND xtype='U')
BEGIN
    CREATE TABLE TABLEPRODUCT (
        Description VARCHAR(255),
        Quantity VARCHAR(50),
        Rate VARCHAR(50),
        Amount VARCHAR(50)
    );
END
GO
IF OBJECT_ID('InsertProductDetails', 'P') IS NOT NULL
    DROP PROCEDURE InsertProductDetails;
GO
CREATE PROCEDURE InsertProductDetails
    @Description VARCHAR(255),
    @Quantity VARCHAR(50),
    @Rate VARCHAR(50),
    @Amount VARCHAR(50)
AS
BEGIN
    INSERT INTO TABLEPRODUCT (Description, Quantity, Rate, Amount)
    VALUES (@Description, @Quantity, @Rate, @Amount);
END;

CREATE TABLE TABLEINVOICE (
    Shipper_Name VARCHAR(255),
    Billing_Customer_Name VARCHAR(255),
    Consignee VARCHAR(255),
    Invoice_No VARCHAR(100),
    Invoice_Date VARCHAR(50),
    Buyers_Order_No VARCHAR(100),
    IE_CODE VARCHAR(100),
    GSTIN VARCHAR(100),
    Port_Loading VARCHAR(100),
    Port_Discharge_Final VARCHAR(100),
    Notify_Party VARCHAR(255),
    Mode_of_Delivery VARCHAR(100),
    Terms VARCHAR(100),
    Container_No VARCHAR(100),
    Style_No VARCHAR(100),
    Total_Amount VARCHAR(100),
    Total_Net_Wt VARCHAR(50),
    Total_Grs_Wt VARCHAR(50),
    Total_CBM VARCHAR(50),
    CONSTRAINT UQ_Invoice UNIQUE (Invoice_No, Invoice_Date)
);
GO
CREATE PROCEDURE InsertInvoiceData
    @Shipper_Name VARCHAR(255),
    @Billing_Customer_Name VARCHAR(255),
    @Consignee VARCHAR(255),
    @Invoice_No VARCHAR(100),
    @Invoice_Date VARCHAR(50),
    @Buyers_Order_No VARCHAR(100),
    @IE_CODE VARCHAR(100),
    @GSTIN VARCHAR(100),
    @Port_Loading VARCHAR(100),
    @Port_Discharge_Final VARCHAR(100),
    @Notify_Party VARCHAR(255),
    @Mode_of_Delivery VARCHAR(100),
    @Terms VARCHAR(100),
    @Container_No VARCHAR(100),
    @Style_No VARCHAR(100),
    @Total_Amount VARCHAR(100),
    @Total_Net_Wt VARCHAR(50),
    @Total_Grs_Wt VARCHAR(50),
    @Total_CBM VARCHAR(50)
AS
BEGIN
    INSERT INTO TABLEINVOICE (
        Shipper_Name, Billing_Customer_Name, Consignee, Invoice_No, Invoice_Date,
        Buyers_Order_No, IE_CODE, GSTIN, Port_Loading, Port_Discharge_Final,
        Notify_Party, Mode_of_Delivery, Terms, Container_No, Style_No,
        Total_Amount, Total_Net_Wt, Total_Grs_Wt, Total_CBM
    )
    VALUES (
        @Shipper_Name, @Billing_Customer_Name, @Consignee, @Invoice_No, @Invoice_Date,
        @Buyers_Order_No, @IE_CODE, @GSTIN, @Port_Loading, @Port_Discharge_Final,
        @Notify_Party, @Mode_of_Delivery, @Terms, @Container_No, @Style_No,
        @Total_Amount, @Total_Net_Wt, @Total_Grs_Wt, @Total_CBM
    );
END;


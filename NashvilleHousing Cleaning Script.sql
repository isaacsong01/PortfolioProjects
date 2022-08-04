-- USE PortfolioProject;

----------------------------------------------------------------------------------------------------------------------------

-- Change SaleDate Column into Date DataType

-- SELECT SaleDate, STR_TO_DATE(SaleDate,'%M %d, %Y') as FormattedDate
-- FROM NashvilleHousing;

-- UPDATE NashvilleHousing
-- SET SaleDate = STR_TO_DATE(SaleDate, '%M %d, %Y');

----------------------------------------------------------------------------------------------------------------------------

-- Where PropertyAddress IS NULL

-- UPDATE NashvilleHousing 
-- SET PropertyAddress=NULL WHERE LENGTH(PropertyAddress) = 0;

-- SELECT *
-- FROM NashvilleHousing
-- WHERE PropertyAddress = ''
-- ORDER BY ParcelID

-- SELECT a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, IFNULL(a.PropertyAddress, b.PropertyAddress)
-- FROM NashvilleHousing a
-- JOIN NashvilleHousing b ON a.ParcelID = b.ParcelID AND a.UniqueID <> b.UniqueID
-- WHERE a.PropertyAddress IS NULL;

-- UPDATE NashvilleHousing a
-- INNER JOIN NashvilleHousing b
-- 	ON a.ParcelID = b.ParcelID
-- 	AND a.UniqueID <> b.UniqueID
-- SET a.PropertyAddress = IFNULL(a.PropertyAddress, b.PropertyAddress)
-- WHERE a.PropertyAddress IS NULL

----------------------------------------------------------------------------------------------------------------------------

-- Split PropertyAddress Column into PropertySplitAddress and PropertySplitCity Columns

-- SELECT PropertyAddress
-- FROM NashvilleHousing;

-- SELECT 
-- SUBSTRING(PropertyAddress,1, LOCATE(',', PropertyAddress)-1) AS Address,
-- SUBSTRING(PropertyAddress, LOCATE(',', PropertyAddress) +1, LENGTH(PropertyAddress)) AS City
-- FROM NashvilleHousing

-- ALTER TABLE NashvilleHousing
-- ADD PropertySplitAddress Varchar(255);

-- UPDATE NashvilleHousing
-- SET PropertySplitAddress = SUBSTRING(PropertyAddress, 1, LOCATE(',', PropertyAddress)-1);

-- ALTER TABLE NashvilleHousing
-- ADD PropertySplitCity Varchar(255);

-- UPDATE NashvilleHousing
-- SET PropertySplitCity = SUBSTRING(PropertyAddress, LOCATE(',', PropertyAddress)+1, LENGTH(PropertyAddress))

----------------------------------------------------------------------------------------------------------------------------

-- Split OwnerAddress Column into OwnerSplitAddress, OwnerSplitCity, and OwnerSplitState

-- SELECT
-- SUBSTRING_INDEX(OwnerAddress, ',', 1),
-- SUBSTRING_INDEX(SUBSTRING_INDEX(OwnerAddress, ',', 2), ',', -1),
-- SUBSTRING_INDEX(OwnerAddress, ',', -1)
-- FROM NashvilleHousing;

-- ALTER TABLE NashvilleHousing
-- ADD OwnerSplitAddress Varchar(255);

-- UPDATE NashvilleHousing
-- SET OwnerSplitAddress = SUBSTRING_INDEX(OwnerAddress, ',', 1);

-- ALTER TABLE NashvilleHousing
-- ADD OwnerSplitCity Varchar(255);

-- UPDATE NashvilleHousing
-- SET OwnerSplitCity = SUBSTRING_INDEX(SUBSTRING_INDEX(OwnerAddress, ',', 2), ',', -1);

-- ALTER TABLE NashvilleHousing
-- ADD OwnerSplitState Varchar(255);

-- UPDATE NashvilleHousing
-- SET OwnerSplitState = SUBSTRING_INDEX(OwnerAddress, ',', -1);

----------------------------------------------------------------------------------------------------------------------------

-- Change Y and N to Yes and No in 'Sold as Vacant' field

-- SELECT DISTINCT(SoldAsVacant), COUNT(SoldAsVacant)
-- FROM NashvilleHousing
-- GROUP BY SoldAsVacant
-- ORDER BY 2;

-- SELECT SoldAsVacant,
-- CASE 
-- WHEN SoldAsVacant = 'Y' THEN 'Yes'
-- WHEN SoldAsVacant = 'N' THEN 'No'
-- ELSE SoldAsVacant
-- END
-- FROM NashvilleHousing;

-- UPDATE NashvilleHousing
-- SET SoldAsVacant = CASE 
-- WHEN SoldAsVacant = 'Y' THEN 'Yes'
-- WHEN SoldAsVacant = 'N' THEN 'No'
-- ELSE SoldAsVacant
-- END;

----------------------------------------------------------------------------------------------------------------------------

-- Remove Duplicates

-- WITH RowNumCTE AS (
-- SELECT *,
-- 	ROW_NUMBER() OVER (
--     PARTITION BY ParcelID,
--     PropertyAddress,
--     SalePrice,
--     SaleDate,
--     LegalReference
--     ORDER BY
--     UniqueID
--     ) row_num
-- FROM NashvilleHousing
-- -- ORDER BY ParcelID
-- )
-- SELECT *
-- FROM RowNumCTE
-- WHERE row_num > 1


-- DELETE t1
-- FROM NashvilleHousing t1
-- INNER JOIN NashvilleHousing t2
-- WHERE 
-- 	t2.ParcelID = t1.ParcelID AND
--     t2.PropertyAddress = t1.PropertyAddress AND
--     t2.SalePrice = t1.SalePrice AND
--     t2.SaleDate = t1.SaleDate AND
--     t2.LegalReference = t1.LegalReference AND
--     t2.UniqueID < t1.UniqueID

----------------------------------------------------------------------------------------------------------------------------
-- Delete Unused Columns

-- ALTER TABLE NashvilleHousing
-- DROP COLUMN PropertyAddress,
-- DROP COLUMN TaxDistrict,
-- DROP COLUMN OwnerAddress;
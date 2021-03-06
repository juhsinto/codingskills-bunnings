import pandas as pd
import warnings

# read the catalogues
cat_A = pd.read_csv("input/catalogA.csv") 
cat_B = pd.read_csv("input/catalogB.csv") 

cat_A['Source'] = 'A'
cat_B['Source'] = 'B'

itermediate_merged_catalogues = cat_A.append(cat_B)
itermediate_merged_catalogues.drop_duplicates(subset="SKU", keep="first", inplace=True)

# reset the index because we have merged two dataframes and the indexes are confusing
itermediate_merged_catalogues.reset_index(drop=True, inplace=True)

# read the barcodes
bar_A = pd.read_csv("input/barcodesA.csv") 
bar_B = pd.read_csv("input/barcodesB.csv") 

# set up a list to hold SKUs ; this will be used to check subsequent duplicate barcode (of different SKU)
SKU_lookup_list = []

# push the SKU of the intermediate merged catalogue to a temp list
if len(itermediate_merged_catalogues) != 0:
    temp_SKU = itermediate_merged_catalogues.iloc[0]['SKU']
    SKU_lookup_list.append(temp_SKU)


def getBarcodes(sku):
    result_A = bar_A[bar_A['SKU'] == sku]
    if (len(result_A))>0:
        return result_A
    result_B = bar_B[bar_B['SKU'] == sku]
    if (len(result_B))>0:
        return result_B
    else:
        warnings.warn("No barcode found for SKU!", UserWarning)


def barcode_exists(barcodes_of_next_sku_as_list, barcodes_of_temp_list):
    # iterate over barcodes_of_next_sku and check if any barcode matches barcodes in barcodes_of_temp_list
    for barcode in barcodes_of_next_sku_as_list:
        if barcode in barcodes_of_temp_list:
            return True


# iterate over the intermediate merged catalogues
for i in range(1, len(itermediate_merged_catalogues)):
    next_sku = itermediate_merged_catalogues.iloc[i]['SKU']

    # get barcodes of the next SKU
    barcodes_of_next_sku = getBarcodes(next_sku)

    # hold set of barcodes for all SKUs in temp_list
    barcodes_of_temp_list = []
    
    # get the barcodes of each SKU in temp_list
    for sku in SKU_lookup_list:
        barcodes_of_sku = getBarcodes(sku)
        barcodes_as_list = barcodes_of_sku['Barcode'].tolist()
        
        # extend - copies content of list (supplied in arg) to the source list
        barcodes_of_temp_list.extend(barcodes_as_list)

    barcodes_of_next_sku_as_list = barcodes_of_next_sku['Barcode'].tolist()
    
    # if the barcode of the next_sku matches the barcode of any of the SKUs in SKU_lookup_list
    if not barcode_exists(barcodes_of_next_sku_as_list, barcodes_of_temp_list):
        SKU_lookup_list.append(next_sku)

deduped_catalogue_on_SKU_barcode = itermediate_merged_catalogues.loc[itermediate_merged_catalogues['SKU'].isin(SKU_lookup_list)]

deduped_catalogue_on_SKU_barcode.to_csv('output/output.csv', index=False)        
print("Done!")
import pandas as pd 

# read the catalogues
cat_A = pd.read_csv("input/catalogA.csv") 
cat_B = pd.read_csv("input/catalogB.csv") 

cat_A['Source'] = 'A'
cat_B['Source'] = 'B'

itermediate_merged_catalogues = cat_A.append(cat_B)
# print(itermediate_merged_catalogues)

itermediate_merged_catalogues.drop_duplicates(subset="SKU", keep="first", inplace=True)
# print(itermediate_merged_catalogues)

# reset the index because we have merged two dataframes and the indexes are confusing
itermediate_merged_catalogues.reset_index(drop=True, inplace=True)
# print(itermediate_merged_catalogues)

# read the barcodes
bar_A = pd.read_csv("input/barcodesA.csv") 
bar_B = pd.read_csv("input/barcodesB.csv") 

# set up a list to hold SKUs ; this will be used to check subsequent duplicate barcode (of different SKU)
SKU_lookup_list = []

# push the SKU of the intermediate merged catalogue to a temp list
if len(itermediate_merged_catalogues) != 0:
    temp_SKU = itermediate_merged_catalogues.iloc[0]['SKU']
    SKU_lookup_list.append(temp_SKU)


def getBarcodes(intermediate_merged_catalogue, sku):
    #     print("attempting to get barcode for ", sku)
    result_A = bar_A[bar_A['SKU'] == sku]
    if (len(result_A))>0:
        return result_A
    result_B = bar_B[bar_B['SKU'] == sku]
    if (len(result_B))>0:
        return result_B
    else:
        print("No barcode found for SKU!")


def barcode_exists(barcodes_of_next_sku_as_list, barcodes_of_temp_list):
    # iterate over barcodes_of_next_sku and check if any barcode matches barcodes in barcodes_of_temp_list
    for barcode in barcodes_of_next_sku_as_list:
        if barcode in barcodes_of_temp_list:
            #             print("the barcode of sku ", next_sku, " exists in the temp list ; to prevent dup ; skip")
            return True

# iterate over the intermediate merged catalogues
for i in range(1, len(itermediate_merged_catalogues)):
    next_sku = itermediate_merged_catalogues.iloc[i]['SKU']
    #     print("the next SKU is ", next_sku)

    # get barcodes of the next SKU
    barcodes_of_next_sku = getBarcodes(itermediate_merged_catalogues, next_sku)
    #     print(barcodes_of_next_sku)

    # hold set of barcodes for all SKUs in temp_list
    barcodes_of_temp_list = []
    
    # get the barcodes of each SKU in temp_list
    for sku in SKU_lookup_list:
        barcodes_of_sku = getBarcodes(itermediate_merged_catalogues, sku)
        barcodes_as_list = barcodes_of_sku['Barcode'].tolist()
        
        # extend - copies content of list (supplied in arg) to the source list
        barcodes_of_temp_list.extend(barcodes_as_list)

    #     print(SKU_lookup_list)
    #     print(barcodes_of_temp_list)

    barcodes_of_next_sku_as_list = barcodes_of_next_sku['Barcode'].tolist()
    
    # if the barcode of the next_sku matches the barcode of any of the SKUs in SKU_lookup_list
    if not barcode_exists(barcodes_of_next_sku_as_list, barcodes_of_temp_list):
        #         print("appending ", next_sku, " to the list")
        SKU_lookup_list.append(next_sku)
        #         print(SKU_lookup_list)

#         print(SKU_lookup_list)

deduped_catalogue_on_SKU_barcode = itermediate_merged_catalogues.loc[itermediate_merged_catalogues['SKU'].isin(SKU_lookup_list)]

deduped_catalogue_on_SKU_barcode.to_csv('output/output.csv', index=False)        
print("Done!")
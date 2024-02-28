from pandalib import pandalib, pandautilities
import json

bearertoken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpblRpbWUiOjE3MDQ3MTk0NDY1NDEsInVzZXJfbmFtZSI6InNpbHZhbmJlbHRlbkBnbWFpbC5jb20iLCJzY29wZSI6WyJhbGwiXSwibG9naW5JcCI6Ijc5LjIwNi4xMi4xNjYiLCJpZCI6ODA5MjI5MzM1LCJleHAiOjE3MDY4Nzk0NDYsImp0aSI6ImJhMjBlYTAzLTQ0ODgtNGJjYi1iMTlkLWYyN2Y1M2VjMTcyNCIsImNsaWVudF9pZCI6InBvcnRhbC1wYyIsInBsYXRmb3JtIjpudWxsfQ.RYq_A2NzQ77RZBwhTNpY3QsOhkAES_jFSceoi79ibQxOY26Rfqjyk8r-wlOHtq6LvG5BFnFMd-V1u_nXb4x5m4nEqIQ8wm67JfVfcCNA1EZnewD5q0TLLOhrbLEMMWQdNe6VAB7c-h_N3_I2-mofZPI2LWyUBVDRVnLGxStOePs"
item_link = "https://detail.tmall.com/item.htm?id=702820303183"
lib = pandalib(bearertoken, "809229335")

item = lib.get_item(item_link)

file_path = "data.json"

with open(file_path, 'w') as json_file:
    json.dump(item, json_file)

print(f'Data has been saved to {file_path}')
import json
import csv
import random
import matplotlib.pyplot as plt


# input: json file of specific image, imageID
# output: list of {box_id, box_text, label}
def getCordJson(id):
    #print("JSON", str(id).zfill(5))
    output_dict = []
    with open('./json/receipt_'+str(id).zfill(5)+'.json') as f:
        data = json.load(f)
        label_list = []
        for group in data["valid_line"]:
            label_list.append(group['category'])

        label_set = set(list(label_list))
        #print(len(label_set), label_set)

            
    return label_set


random_list = list(range(800))
img_list = list(range(800))

label_no_list = []
avg_no_list = []


for j in range(20):
    print('\n--- Final ---', "trial #", j+1)
    random.shuffle(random_list)
    print(random_list[:20])

    final_label_set = set()
    final_label_no = []

    final_label_set = set.union(final_label_set, getCordJson(1))

    for i in random_list:
        final_label_set = set.union(final_label_set, getCordJson(i))
        final_label_no.append(len(final_label_set))


    print()
    
    label_no_list.append(final_label_no)


for k in range(800):
    avg_no_list.append(sum([label_no_list[0][k], label_no_list[1][k], label_no_list[2][k], label_no_list[3][k], label_no_list[4][k],
    label_no_list[5][k], label_no_list[6][k], label_no_list[7][k], label_no_list[8][k], label_no_list[9][k],
    label_no_list[10][k], label_no_list[11][k], label_no_list[12][k], label_no_list[13][k], label_no_list[14][k],
    label_no_list[15][k], label_no_list[16][k], label_no_list[17][k], label_no_list[18][k], label_no_list[19][k]])/20) 

fig, ax = plt.subplots(nrows=5, ncols=4)

idx = 0
for row in ax:
    for col in row:
        col.plot(img_list, label_no_list[idx])
        idx += 1


plt.show()
plt.plot(img_list, avg_no_list)

plt.show()
    #print(len(final_label_set), final_label_set)
    #print(len(final_label_no), final_label_no)
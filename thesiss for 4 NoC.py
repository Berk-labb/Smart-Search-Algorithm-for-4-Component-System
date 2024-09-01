# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 23:01:09 2024

@author: monster
"""

import random
import time
from itertools import product

# Function to generate and filter combinations
def generate_and_filter_combinations(remaining_elements, remaining_machines, threshold_1, threshold_2, threshold_3, threshold_4,  threshold_5, threshold_6,  current_combination=[], result=[]):
    if remaining_machines == 0:
        if current_combination[0] >=  threshold_1 and current_combination[0] <= threshold_2 and current_combination[1] >=  threshold_3 and current_combination[1] <= threshold_4 and current_combination[2] >=  threshold_5 and current_combination[2] <= threshold_6 :
            result.append(tuple(current_combination))
        return

    for element in remaining_elements:
        if not current_combination or element >= current_combination[-1] :
            generate_and_filter_combinations(
                remaining_elements,
                remaining_machines - 1,
                threshold_1,
                threshold_2,
                threshold_3,
                threshold_4,
                threshold_5,
                threshold_6,
                current_combination + [element],
                result
            )

# Function to write output to file
def write_output4_to_file(output4):
    with open("output4.txt", "a") as file:
        file.write(output4 + "\n")

# Function to simulate the process
def simulate_process(det_level, num_machines, alpha, Rep_Length, mudahale_turu, filtered_komb):
    count = 0
    Total_cost = 0
    Num_CMC = 0
    Num_PMC = 0
    Num_ROC = 0
    Num_EOC = 0
    min_total_Cost = float('inf')
    det_level=[0]* num_machines
    hm_bringing = 0
    mudahalekarari = 0
    number_of_search = 0
    mudahale_edildimi = 1
    red = 0
    th1=0
    th2=100
    th3=0
    th4=100
    th5=0
    th6=100
    optimal=[0,0,0] #Optimal of previous mudahale turu
    optimalreach=[0,0,0] #Is optimal same with previous mudahale turu
    mudahale = 0  # Initialize mudahale here

    for qwe in range(500):
        if mudahale_edildimi == 0:
            break
        else:
            mudahale_turu = filtered_komb[5] + qwe  - 1 
            mudahale_edildimi = 0
            combinations = []
            #print("Thler", th1, th2, th3, th4, th5, th6, th7, th8, th9, th10)
            #print("optimaller", optimal)
            #print("optimaller", optimalreach)
            if th1 + 1 == optimal[0]:
                optimalreach[0] = 1
                th1 = th1 + 1
                th2 = th1 
                #print("girdi1, th1:", th1, th2)
            if th3 + 1 == optimal[1]:
                optimalreach[1] = 1
                th3 = th3 + 1
                th4 = th3 
                #print("girdi2, th3:", th3, th4)
            if th5 + 1 == optimal[2]:
                optimalreach[2] = 1
                th5 = th5 + 1
                th6 = th5 
                #print("girdi3, th5:", th5, th6)
            if optimalreach[0] == 1:
                optimal[0] = th1
                #print("Optimal 1 sağlandı", optimal[0] )
            if optimalreach[0] == 0:
                optimal[0] = th1 + 1
                #print("Optimal 1 sağlammadı", optimal[0])
            if optimalreach[1] == 1:
                optimal[1] = th3
                #print("Optimal 2 sağlandı", optimal[1])
            if optimalreach[1] == 0:
                optimal[1] = th3 + 1
                #print("Optimal 2 sağlammadı", optimal[1])
            if optimalreach[2] == 1:
                optimal[2] = th5
                #print("Optimal 3 sağlandı", optimal[2])
            if optimalreach[2] == 0:
                optimal[2] = th5 + 1
                #print("Optimal 3 sağlammadı", optimal[2])
            generate_and_filter_combinations(range(filtered_komb[5] - 1, mudahale_turu + 2),  num_machines - 1, th1, th2, th3, th4, th5,th6, result=combinations)
            number_of_search += len(combinations)
            for c, lst in enumerate(combinations):
                random.seed(seednumber)
                #print(lst[0], lst[1], lst[2], lst[3], lst[4], det_level)
                for period in range(Rep_Length):
                    for a in range(num_machines):
                        if random.random() < alpha:
                            det_level[a] += 1
                    if max(det_level) > 0:
                        count += 1
                        if filtered_komb[5] in det_level or count == mudahale_turu:
                            mudahale = 1
                            mudahalekarari += 1
                        if mudahale == 1:
                            mudahale = 0
                            hm_bringing = sum(1 for qwert in lst if qwert <= count) + 1
                            count = 0
                            if filtered_komb[5] in det_level:
                                red = 1
                                Num_CMC += 1
                                Total_cost += filtered_komb[0]
                            else:
                                Num_PMC += 1
                                Total_cost += filtered_komb[1]
                            for a in range(num_machines):
                                if det_level[a] > 0:
                                    hm_bringing -= 1
                            det_level = [0] * num_machines
                            if hm_bringing < 0:
                                Total_cost += filtered_komb[3] * -hm_bringing
                                Num_EOC -= hm_bringing
                            if hm_bringing > 0:
                                Total_cost += filtered_komb[4] * hm_bringing
                                Num_ROC += hm_bringing
                if (Total_cost / (Rep_Length + Num_PMC + Num_CMC)) < min_total_Cost:
                    mudahale_edildimi = 1
                    min_total_Cost = (Total_cost / (Rep_Length + Num_PMC + Num_CMC))
                    write_output4_to_file("Yeni min total cost: " + str(min_total_Cost))
                    write_output4_to_file("Liste: " + str(lst))
                    write_output4_to_file("Sarıda: " + str(lst[-1]))
                    write_output4_to_file("müdahale_turu: " + str(mudahale_turu))
                    write_output4_to_file("#ROC: " + str(Num_ROC))
                    write_output4_to_file("#PMC: " + str(Num_PMC))
                    write_output4_to_file("#CMC: " + str(Num_CMC))
                    write_output4_to_file("#EOC: " + str(Num_EOC))
                    write_output4_to_file("mudahalekarari: " + str(mudahalekarari))
                    write_output4_to_file("Kaçıncı: " + str(number_of_search))
                    write_output4_to_file("")
                    th1=lst[0] - 1
                    th2=lst[0] + 1
                    th3= lst[1] - 1
                    th4= lst[1] + 1
                    th5= lst[2] - 1
                    th6= lst[2] + 1
                Total_cost = 0
                Num_EOC = 0
                Num_ROC = 0
                Num_CMC = 0
                Num_PMC = 0
                count = 0
                det_level=[0]* num_machines   
    return number_of_search

# Main code71
CM_values = [500,375,250,150,75]
PM_value = 50
alpha_values = [0.2]
EOC_values = [5,10,15]
ROC_values = [5,10,15]
max_Det_level = [5]
num_machines = [4]

kombinations = list(product(CM_values, [PM_value], alpha_values, EOC_values, ROC_values, max_Det_level, num_machines))

filtered_combinations = [komb for komb in kombinations if komb[3] >= komb[4]]

for yurt, filtered_komb in enumerate(filtered_combinations):
    _, _, alpha, EOC, ROC, _, num_machines = filtered_komb
    print("İşlem:", yurt)

    for kral in range(1):
        starting_time = time.time()
        det_level = [0] * num_machines
        Rep_Length = 3000000
        işlemsayisi = 0
        mudahale = 0
        number_of_search = 0
        mudahale_edildimi = 1
        red = 0
        seednumber = random.randint(1,1000000000)
        write_output4_to_file("Seed number: " + str(seednumber))
        write_output4_to_file("CMC: " + str(filtered_komb[0]))
        write_output4_to_file("PMC: " + str(filtered_komb[1]))
        write_output4_to_file("ROC: " + str(filtered_komb[4]))
        write_output4_to_file("EOC: " + str(filtered_komb[3]))
        write_output4_to_file("MDL: " + str(filtered_komb[5]))
        write_output4_to_file("Rep_Length: " + str(Rep_Length))
        write_output4_to_file("Number of Machine: " + str(num_machines))
        write_output4_to_file("Alpha: " + str(alpha))
        write_output4_to_file("Search sayısı: " + str(kral + 1))

        for qwe in range(500):
            if mudahale_edildimi == 0:
                break
            else:
                mudahale_turu = filtered_komb[5] + qwe
                mudahale_edildimi = 0
                number_of_search += simulate_process(det_level, num_machines, alpha, Rep_Length, mudahale_turu, filtered_komb)

        finishing_time = time.time()
        write_output4_to_file("Simulation Time: " + str(finishing_time - starting_time))
        write_output4_to_file("Toplam simülasyon: " + str(number_of_search))

print("Results saved to output4.txt")

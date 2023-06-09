from util import PoT_calc_accuracy, CoT_calc_accuracy, PoT_selfcon_calc_accuracy, CoT_selfcon_calc_accuracy, \
    listing_calc_accuracy, CoT_d2e_calc_accuracy

if __name__ == "__main__":
    #CoT_selfcon_calc_accuracy("results/CoT_scaled_selfcon_{}_ChatOpenAI.json")
    #listing_calc_accuracy("results/compare_permutation_6_0608_1623.json")
    CoT_d2e_calc_accuracy("results/d2e_CoT_ChatOpenAI_0606_1952.json")
    #CoT_calc_accuracy("results/CoT_org_scaled_16383_ChatOpenAI_0607_1742.json")
    #PoT_calc_accuracy("results/d2e_scaled_16383_ChatOpenAI_0607_1701.json")


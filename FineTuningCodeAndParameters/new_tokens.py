# 保持 token 顺序与已发布模型的词表一致。
new_tokens_need_add = [
    # 诈骗类型：L1 与 L2。
    "<|L1_Identity|>", "<|L2_Id_Gov|>", "<|L2_Id_Acquaintance|>", "<|L2_Id_Business|>", "<|L2_Id_Service|>",
    "<|L2_Id_Military|>",

    "<|L1_Finance|>", "<|L2_Fin_Loan|>", "<|L2_Fin_CreditFix|>", "<|L2_Fin_Invest|>", "<|L2_Fin_Recovery|>",

    "<|L1_Bait|>", "<|L2_Bait_Task|>", "<|L2_Bait_GambleAndLottery|>", "<|L2_Bait_Job|>",

    "<|L1_Transactions|>", "<|L2_Tran_Game|>", "<|L2_Tran_Shop|>", "<|L2_Tran_Procurement|>",

    "<|L1_Social|>", "<|L2_Soc_Romance|>", "<|L2_Soc_Sex|>",

    "<|L1_Illegal|>", "<|L2_Ill_Extortion|>", "<|L2_Ill_ATO|>",

    # 心理因素。
    "<|Gain_Seeking|>",

    "<|Love_Social_Desire|>",
    "<|Impulsive_Desire|>",

    "<|Authority_Obey_Trust|>",

    "<|Social_Influence|>",
    "<|Fear_Pressure|>",

    "<|Sunk_Cost_Fallacy|>",
    "<|Cognition_Inertia_Reinforcement|>",
    "<|Non_Cognitive|>",

    # 醒悟因素。
    "<|System_Intervention|>",
    "<|Social_Intervention|>",
    "<|External_Validation|>",

    "<|Fraud_Awareness_Trigger|>",
    "<|Internal_Logical|>",
    "<|Commitment_Failure|>",
    "<|Attacker_Disengagement|>",

    "<|Objective_Termination|>",

    "<|EMPTY|>"
]
print(new_tokens_need_add)

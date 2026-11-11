# Scam-Type Taxonomy

## 1. Classification Scope and Structure

This taxonomy describes the strategies and methods used in a telecom scam case. It contains 6 Level-1 (L1) categories and 18 Level-2 (L2) subcategories. L1 captures the overall strategy, while L2 distinguishes specific operational methods.

Classification uses the complete case as its unit of analysis, combining information from Attraction, Inducement, Transfer, and Awakening. A case may carry multiple L2 labels. Labels cover strategies actually present in the case, including the initial lure, the identity used to establish trust, and the method that ultimately causes financial loss.

The following principles guide classification:

- Classify from specific actions and evidence in the narrative, rather than relying only on the case title, a police summary, or the victim's terminology.
- Different strategies may occur together in one case; each label requires corresponding evidence.
- Distinguish identities used to establish trust, opportunities used to attract participation, and the actual transaction or fund-transfer mechanism.
- Use L1 and L2 labels together. When several L2 types fall under the same L1 category, record each combination separately.

## 2. Level-1 Categories

| L1 category | Label code | Core meaning | Number of L2 types |
|---|---|---|---:|
| Identity Impersonation | `L1_Identity` | Impersonating public authorities, acquaintances, business partners, or people with credible identities, and exploiting the associated trust. | 4 |
| Finance and Credit | `L1_Finance` | Scams involving financial needs and the handling of funds, including loans, credit records, investments, and fund liquidation. | 4 |
| Bait and Opportunity | `L1_Bait` | Fabricating employment, rebate, gambling-profit, or prize-winning opportunities to attract participation and payments. | 3 |
| Transactions | `L1_Transactions` | Obtaining money during transactions or fulfillment involving fictitious goods, services, or procurement orders. | 3 |
| Long-Term Social Relationships and Sex-Related Baiting | `L1_Social` | Attracting participation and fund transfers through sustained emotional relationships or sexual-content/service lures. | 2 |
| Illicit Online Activities and Extortion | `L1_Illegal` | Stealing funds through technical account takeover, or coercively obtaining property through threats and extortion. | 2 |

## 3. Detailed Level-2 Definitions

### 3.1 Identity Impersonation

| L2 category | Label code | Definition and identifying evidence |
|---|---|---|
| Police, Prosecutor, Court, and Government-Agency Impersonation | `L2_Id_Gov` | Impersonating police, prosecutors, courts, or regulatory/clearing bodies with public authority, or fabricating their personnel identities, documents, official websites, apps, official social-media accounts, or official text messages. The core mechanism is borrowing the credibility of public power and official status. |
| Superior, Acquaintance, Public-Figure, and Business-Partner Impersonation | `L2_Id_Acquaintance` | Impersonating relatives, friends, colleagues, superiors, public figures, or existing/potential suppliers, customers, and contacts at enterprises or public institutions, and abusing trust in the corresponding identity or relationship. |
| Platform or Customer-Service Impersonation | `L2_Id_Service` | Impersonating official customer service or related staff of e-commerce, logistics, financial, or Internet platforms, and inducing actions or payments under pretexts such as refunds, account processing, or service administration. |
| Military, Police, and Other Special-Status Impersonation | `L2_Id_Military` | Impersonating military, police, fire-service, or other personnel with a special status and exploiting that status's credibility. Impersonated military, police, or fire-service procurement staff are typical examples in the prompt. |

### 3.2 Finance and Credit

| L2 category | Label code | Definition and identifying evidence |
|---|---|---|
| Fake Loans and Credit Cards | `L2_Fin_Loan` | Using loan or credit-card applications, easy-access borrowing, or similar offers as bait, and obtaining money during the purported process of securing a loan or credit limit. |
| Fake Credit-Record Repair | `L2_Fin_CreditFix` | Inducing purported repair, account closure, or fund operations by claiming an abnormal credit record, an effect on credit history, or a need to close loan accounts or campus loans. |
| Fake Investment and Wealth Management | `L2_Fin_Invest` | Using investment, wealth-management, stock, or similar opportunities and high returns as bait, directing victims into fake channels or platforms, and causing financial loss, often through blocked withdrawals or purported losses after investment. |
| Fake Fund Liquidation and Refunds | `L2_Fin_Recovery` | Secondary scams targeting people who have genuinely lost money or have funds awaiting return, under pretexts of liquidation, refunds, repayment, or loss recovery. Examples include fake refunds following previous scams, investment losses, collapsed P2P lending platforms, or closed training providers or gyms. |

### 3.3 Bait and Opportunity

| L2 category | Label code | Definition and identifying evidence |
|---|---|---|
| Order Brushing and Task Rebates | `L2_Bait_Task` | Attracting participation with commissions for liking posts, simulated purchases, sham orders, or tasks. Small genuine rebates are often followed by demands for further payments because of linked or stuck orders, operation errors, account freezing, or unfreezing. |
| Fake Recruitment and Part-Time Jobs | `L2_Bait_Job` | Contacting victims through fictitious high-paid part-time work, handicraft work, daily-paid jobs, or other employment offers, or using recruitment and employment promises to obtain money. |
| Online Gambling and Fake Giveaways/Prize Winnings | `L2_Bait_GambleAndLottery` | Inducing online gambling through claims of gambling loopholes, platform insider information, or guaranteed profits; or demanding advance taxes, deposits, or other payments for fake giveaways or prize winnings. |

### 3.4 Transactions

| L2 category | Label code | Definition and identifying evidence |
|---|---|---|
| Fake Online-Game Transactions | `L2_Tran_Game` | Scams involving the purchase or sale of game accounts, equipment, skins, or other virtual goods, including redirection to external fake platforms. The victim may be a buyer or seller. |
| Fake Shopping and Services | `L2_Tran_Shop` | Scams involving second-hand goods, tickets, purchasing services, everyday services, or similar transactions between individuals. The scammer may pose as a buyer or seller, and the victim may likewise be an individual buyer or seller. |
| B2B Fraud and Fake Procurement | `L2_Tran_Procurement` | Fabricating large procurement demands from major customers, companies, or institutions to induce a business or merchant, acting as the seller, to advance payments or deposits or pay a designated supplier. This applies only to B2B business settings. |

### 3.5 Long-Term Social Relationships and Sex-Related Baiting

| L2 category | Label code | Definition and identifying evidence |
|---|---|---|
| Online Romance and Dating | `L2_Soc_Romance` | Building emotional trust through sustained online romance, friendship, and companionship, then inducing investments, transfers, operation of accounts on another person's behalf, or participation in other scams. This includes scenarios commonly called pig butchering. |
| Offers of Large Payments for Conceiving a Child and Sex-Related Baiting | `L2_Soc_Sex` | Luring victims into a scam and progressively demanding money through sexual content, sexual services, or offers of large payments for conceiving a child. The core lure involves immediate or short-term sexual desire. |

### 3.6 Illicit Online Activities and Extortion

| L2 category | Label code | Definition and identifying evidence |
|---|---|---|
| Coercion and Extortion | `L2_Ill_Extortion` | Forcing victims to surrender property by threatening disclosure of private or sexual material, reputational damage, a workplace crisis, data loss, or similar harm. The core mechanism is payment compelled by threats. |
| Account Takeover and Technical Theft | `L2_Ill_ATO` | Obtaining control needed to move funds through account takeover, malware, text-message interception, credential theft through screen sharing, remote control, remote login, or similar means, and stealing funds without the victim's deliberate authorization. |

## 4. Important Decision Boundaries

### 4.1 Identity Impersonation versus an Ordinary Fabricated Identity

Identity-impersonation labels concern social trust obtained through the claimed identity. For acquaintances, public figures, official customer service, or long-term business partners, identify the specific evidence that the victim trusted that identity.

In fake procurement, an ad hoc claim to be a large customer may simply provide a role for a fictitious order and does not automatically justify an identity-impersonation label. Add the corresponding identity label when supported by sustained credibility-building actions, such as credentials, business cards, or contracts, or a genuine prior business relationship.

### 4.2 Forged Government Materials/Channels versus Verbal References to Authority

When military or police identities appear, identify their role in the case. Impersonated law-enforcement investigations or forged enforcement materials call for consideration of the police/prosecutor/court/government category. Impersonated fire-service procurement officers or similar occupational identities call for consideration of the special-status category alongside the actual transaction or procurement method. The word 'police' alone does not justify automatically adding both identity labels.

The current classification prompt explicitly distinguishes:

- Forged agency documents, official websites, apps, official social-media accounts, or official text messages provide grounds for the government-agency impersonation label.
- Statements such as 'the banking regulator will freeze your account' or 'transfer to the regulator's account,' without forged materials or channels, do not by themselves justify `L2_Id_Gov`.

This boundary constrains label assignment; not every mention of a government or regulatory agency belongs to this category.

### 4.3 Ordinary Transactions, B2B Procurement, and Game Transactions

- Use `L2_Tran_Shop` for individuals scammed while buying goods/services or selling personal unused items.
- Use `L2_Tran_Procurement` when a merchant advances funds because of a fictitious business order.
- Prioritize `L2_Tran_Game` for transactions in online-game virtual goods, regardless of whether the victim is the buyer or seller.

### 4.4 Task Rebates, Fake Recruitment, and Financial Strategies

Additional payment demands within a task-rebate platform, such as linked or stuck orders, unfreezing, or operation errors, are components of `L2_Bait_Task`. An unfreezing fee or frozen account alone does not justify adding a financial label.

When explicit fake recruitment or part-time employment information occurs alongside task-based fraud, both recruitment and task-rebate labels may be recorded, each with its own evidence.

Consider adding `L2_Fin_Invest` beyond task rebates only when the victim is directed to an independent fake investment channel or platform and an investment scam actually occurs.

### 4.5 Fund Liquidation versus Ordinary Customer-Service Refunds

`L2_Fin_Recovery` requires genuine previous financial loss, funds awaiting liquidation, or a refund background. When fake customer service invents compensation or refunds for ordinary logistics or product-quality issues and obtains transfers, this does not itself constitute fund-liquidation fraud. Assess customer-service impersonation and other labels from the actual narrative.

### 4.6 Online Romance versus Sex-Related Baiting

`L2_Soc_Romance` depends on sustained companionship, relationship cultivation, and emotional trust. `L2_Soc_Sex` depends on immediate or short-term sexual attraction.

The current prompt treats scam scenarios involving very rapid offline meetings under descriptions such as 'local dating' as evidence of sex-related baiting. The word 'dating' alone does not make a case a long-term romance scam.

### 4.7 Sex-Related Baiting versus Extortion

Sexual content or services may provide the initial lure. If this is followed by coercive demands threatening disclosure of contacts or intimate images, both `L2_Soc_Sex` and `L2_Ill_Extortion` may be recorded. The labels describe the initial lure and the subsequent coercive payment mechanism, respectively.

### 4.8 Technical Theft versus Payments Induced by Social Engineering

Assigning `L2_Ill_ATO` requires confirmation that the scammer obtained control and independently executed a fund transfer.

- When the victim scans a payment code, confirms the amount or account, and completes a transfer, the payment is actively performed by the victim.
- The current prompt also classifies voluntary disclosure of a verification code for a single transfer as an authorized payment induced by social engineering.
- Scammers taking over accounts through obtained passwords or login/reset codes, or moving funds themselves through remote control, screen-sharing credential theft, or malware, fall within technical-theft scenarios.
- An auxiliary test is whether the scammer can continue stealing funds using existing control without further verification codes from the victim.

`L2_Ill_ATO` in the scam-type taxonomy and `Non_Cognitive` in the psychological taxonomy describe the attack type and the mechanism of an individual fund-transfer event, respectively. They cannot substitute for one another.

## 5. Label Representation

Each output element concatenates one L1 code and one L2 code. For example, a case involving both long-term romance and fake investment may be represented as:

```json
{
  "reason": "The case combines sustained emotional engagement with fake investment inducement.",
  "labels": [
    "<L1_Social><L2_Soc_Romance>",
    "<L1_Finance><L2_Fin_Invest>"
  ]
}
```

The task prompt requires both `reason` and `labels`, with the analysis field appearing before the label field.

The fine-tuning version uses special-token forms such as `<|L1_Social|><|L2_Soc_Romance|>`. The baseline version uses ordinary text forms such as `<L1_Social><L2_Soc_Romance>`. The meanings and hierarchy are the same.

## 6. Corresponding Prompts

This document explains category meanings and decision boundaries. Complete model roles, input requirements, output formats, and examples are available in:

- [Fine-tuning scam-type prompt](../../prompts/en/fine_tuning/fraud_typology.txt)
- [Baseline scam-type prompt](../../prompts/en/baseline/fraud_typology.txt)

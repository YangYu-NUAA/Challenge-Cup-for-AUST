# 排除案例说明

本文件记录公开数据集中被排除的案例及排除原因，防止重复劳动。

## 筛选标准回顾

任务书 Section 5.1 要求案例满足至少 2 条：
1. 涉及智能体工具调用（而非单纯文本输出）
2. 可映射到政务办公场景（文档/邮件/会议/日程/知识库/跨部门）
3. 能写成 ArbiterOS prior/current 结构
4. 能明确指出危险工具动作
5. 能设计防护结果（放行/审批/阻断）

## 排除案例分类

### injecagent (88 cases)

- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'augustsmartlockunlockdoor']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-19` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-19` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'augustsmartlockunlockdoor']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-20` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-20` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'bankmanagerpaybill']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-36` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-36` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'bankmanagerpaybill']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-37` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-37` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'bankmanagertransferfunds']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-53` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-53` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'bankmanagertransferfunds']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-54` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-54` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'binancedeposit']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-70` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-70` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'binancedeposit']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-71` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-71` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'binanceplaceorder']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-87` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-87` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'binanceplaceorder']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-88` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-88` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'binancewithdraw']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-104` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-104` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'binancewithdraw']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-105` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-105` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'dropboxmoveitem']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-155` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-155` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'dropboxmoveitem']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-156` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-156` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'epicfhirmanageappointments']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-189` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-189` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'epicfhirmanageappointments']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-190` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-190` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'epicfhirmanageclinicaldocuments']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-206` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-206` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'epicfhirmanageclinicaldocuments']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-207` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-207` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'epicfhirmanagepatientrecords']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-223` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-223` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'epicfhirmanagepatientrecords']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-224` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-224` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'evernotemanagermanagenotesharinglevel']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-240` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-240` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'evernotemanagermanagenotesharinglevel']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-241` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-241` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'fedexshipmanagermanageshipment']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-274` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-274` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'fedexshipmanagermanageshipment']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-275` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-275` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'googlehomescheduledeviceaction']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-308` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-308` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'googlehomescheduledeviceaction']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-309` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-309` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'indoorrobotgotoroom']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-325` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-325` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'indoorrobotgotoroom']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-326` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-326` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'nortonidentitysafeautofillpersonalinfo']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-342` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-342` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'nortonidentitysafeautofillpersonalinfo']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-343` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-343` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'nortonidentitysafedisabletwofactorauthentication']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-359` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-359` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'nortonidentitysafedisabletwofactorauthentication']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-360` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-360` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'nortonidentitysafesharepassword']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-376` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-376` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'nortonidentitysafesharepassword']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-377` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-377` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'slackleavechannel']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-393` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-393` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'slackleavechannel']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-394` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-394` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'the23andmesharedata']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-427` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-427` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'the23andmesharedata']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-428` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-428` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'trafficcontrolgiveprioritytoemergencyvehicle']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-461` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-461` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'trafficcontrolgiveprioritytoemergencyvehicle']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-462` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-462` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'trafficcontrolmanagetrafficlightstate']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-478` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-478` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'trafficcontrolmanagetrafficlightstate']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-479` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-479` | 其他 | GitHubGetUserDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetrepositorydetails', 'venmowithdrawmoney']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-495` | 其他 | GitHubGetRepositoryDetails
  - `injecagent_dh_test_cases_dh_enhanced-495` | 其他 | GitHubGetRepositoryDetails
- **2 cases** - C1(工具调用): 通过; C2(政务可映射): 不通过 -> 其他; C3(ArbiterOS可写): 通过; C4(危险动作): 不通过 -> tools=['githubgetuserdetails', 'venmowithdrawmoney']; C5(防护可设计): 通过
  - `injecagent_dh_test_cases_dh_base-496` | 其他 | GitHubGetUserDetails
  - `injecagent_dh_test_cases_dh_enhanced-496` | 其他 | GitHubGetUserDetails

## 排除原因总结

| 排除原因 | 案例数 | 说明 |
|---|---|---|
| C1(工具调用) | 88 | 见上方分类 |
| C2(政务可映射) | 88 | 见上方分类 |
| C3(ArbiterOS可写) | 88 | 见上方分类 |
| C4(危险动作) | 88 | 见上方分类 |
| C5(防护可设计) | 88 | 见上方分类 |

"""
1. 男女比例 圓餅圖
2. 年齡 15 ~ 80 ,其他刪除 , 並做成10量化 長條圖
3. 工作年資和年齡比起來 是否正常? 例如 18歲,頂多工作3年 , 年齡 - 工作年資 >= 15 , 不符合的刪除 並做成5量化長條圖
4. 課程滿意度 長條圖
5. 軟體熟悉度,群組長條圖
6. 興趣 抓取5個以上的 , 做成長條圖
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

url = "https://docs.google.com/spreadsheets/d/1Sb-Q7gI1sH4KGvx_Y6oFgU7_WzCFampfHSJxpQN3VfM/export?format=csv"

df = pd.read_csv(url)
# 清洗資料,把不用的欄位刪除
df.drop(["時間戳記", "檔案"], axis=1, inplace=True)

plt.figure(figsize=(16, 10), dpi=150)
plt.rcParams["font.sans-serif"] = "Microsoft JhengHei"

# 1. 男女比例 圓餅圖
plt.subplot(241)
s1 = df.groupby("性別")["性別"].count()
plt.pie(s1.values, autopct="%.2f%%", labels=s1.index)


# 2. 年齡 15 ~ 80 ,其他刪除 , 並做成10量化 長條圖
plt.subplot(242)
df["年齡"] = 2025 - pd.to_numeric(df["出生年月日"].str[:4], errors="coerce")
df = df[(df["年齡"] > 15) & (df["年齡"] < 80)]
df["年齡10量化"] = df["年齡"] // 10 * 10
s2 = df.groupby("年齡10量化")["年齡10量化"].count()
plt.bar(s2.index, s2.values, width=8)
plt.xlabel("年齡", fontsize=16)
plt.ylabel("人數", fontsize=16)
plt.title("年齡層人數統計", fontsize=24)
for i in s2.index:
    plt.text(i, s2[i] + 2, f"{s2[i]}人", ha="center")

# 3. 工作年資和年齡比起來 是否正常? 例如 18歲,頂多工作3年 , 年齡 - 工作年資 >= 15 , 不符合的刪除 並做成5量化長條圖
plt.subplot(243)
df = df[df["年齡"] - df["工作年資"] >= 15]
df["工作年資5量化"] = df["工作年資"] // 5 * 5
s3 = df.groupby("工作年資5量化")["工作年資5量化"].count()
plt.bar(s3.index, s3.values, width=3.5, color="#0AEDF5")
plt.xlabel("工作年資5量化", fontsize=16)
plt.ylabel("人數", fontsize=16)
plt.title("工作年資人數統計", fontsize=24)
for i in s3.index:
    plt.text(i, s3[i] + 1, f"{s3[i]}人", ha="center")


# 4. 課程滿意度 長條圖
plt.subplot(244)
s4 = df.groupby("你對本課程的滿意度")["你對本課程的滿意度"].count()
plt.bar(s4.index, s4.values, color="#09A3F4")
plt.xlabel("滿意度", fontsize=16)
plt.ylabel("人數", fontsize=16)
plt.title(f"滿意度調查\n平均{df['你對本課程的滿意度'].mean():.2f}")
for i in s4.index:
    plt.text(i, s4[i] + 1, f"{s4[i]}人", ha="center")


# 5. 軟體熟悉度,群組長條圖
plt.subplot(223)
df1 = df.iloc[:, 4:10]
df2 = df1.melt(var_name="軟體", value_name="熟悉度")
df2["軟體"] = df2["軟體"].str.replace("你對以下軟體的熟悉度 [", "").str.replace("]", "")
jessica_list = ["PowerBI", "Excel", "Google 試算表", "Python", "JavaScript", "C 語言"]
sophai_list = ["完全不熟", "曾經學過", "普通", "還算熟悉", "非常熟練"]
print(df2["熟悉度"].unique())

for i in range(len(sophai_list)):
    s5 = df2[df2["熟悉度"] == sophai_list[i]].groupby("軟體")["軟體"].count()
    plt.bar(
        np.array(range(len(jessica_list))) - 0.32 + 0.16 * i,
        s5.values,
        width=0.16,
        label=sophai_list[i],
    )
plt.xlabel("各種程式", fontsize=16)
plt.ylabel("人數", fontsize=16)
plt.title("各程式熟悉度", fontsize=24)
plt.legend()
plt.xticks(np.array(range(len(jessica_list))), jessica_list)


# 6. 興趣 抓取5個以上的 , 做成長條圖
plt.subplot(224)
df["你的興趣"] = df["你的興趣"].str.replace("，", ",")
df3 = df["你的興趣"].str.split(",", expand=True)
df4 = df3.melt(var_name="A", value_name="興趣").dropna()
df4["興趣"] = df4["興趣"].str.replace(" ", "")
s6 = df4.groupby("興趣")["興趣"].count()
s6 = s6[s6 > 5].sort_values(ascending=False)
plt.bar(s6.index, s6.values)
plt.ylabel("人數", fontsize=16)
for i in s6.index:
    plt.text(i, s6[i], s6[i], ha="center")


plt.tight_layout()
plt.show()

df4.to_csv("google表單.csv", index=False, encoding="utf-8-sig")

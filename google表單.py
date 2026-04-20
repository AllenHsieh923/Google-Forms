"""
1. 男女比例 圓餅圖
2. 年齡 15 ~ 80 ,其他刪除 , 並做成10量化 長條圖
3. 工作年資和年齡比起來 是否正常? 例如 18歲,頂多工作3年 , 年齡 - 工作年資 >= 15 , 不符合的刪除 並做成5量化長條圖
4. 課程滿意度 長條圖
5. 軟體熟悉度,群組長條圖
6. 興趣 抓取5個以上的 , 做成長條圖
"""

import matplotlib.pyplot as plt
import pandas as pd

url = "https://docs.google.com/spreadsheets/d/1Sb-Q7gI1sH4KGvx_Y6oFgU7_WzCFampfHSJxpQN3VfM/export?format=csv"

df = pd.read_csv(url)
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
    plt.text(i, s2[i] + 3, f"{s2[i]}人", ha="center")

# 3. 工作年資和年齡比起來 是否正常? 例如 18歲,頂多工作3年 , 年齡 - 工作年資 >= 15 , 不符合的刪除 並做成5量化長條圖
# 4. 課程滿意度 長條圖
# 5. 軟體熟悉度,群組長條圖
# 6. 興趣 抓取5個以上的 , 做成長條圖


print(df.head())

plt.tight_layout()
plt.show()

df.to_csv("google表單.csv", index=False, encoding="utf-8-sig")

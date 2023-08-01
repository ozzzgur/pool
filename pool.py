import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.float_format", lambda x: "%.3f" %x)
pd.set_option("display.width",500)

##df_deaths

df_deaths = pd.read_csv("NCHS_-_Injury_Mortality__United_States.csv")
df_deaths = df_deaths[(df_deaths["Injury mechanism"]=="Drowning")&(df_deaths["Injury intent"]=='Unintentional')|(df_deaths["Injury intent"]=='Undetermined')]
df_deaths = df_deaths.groupby("Year").agg({"Deaths":"sum"})
df_deaths.reset_index(inplace=True)
df_deaths["Year"] = pd.to_datetime(df_deaths["Year"], format="%Y")
plt.plot(df_deaths["Year"],df_deaths["Deaths"],linestyle="-")
plt.xlabel("Year")
plt.ylabel("Deaths")
plt.title("Deaths by Year")
plt.show()



##df_en

df_en =pd.read_csv("nuclear-energy-generation.csv")
df_en_filtered = df_en.drop(df_en.loc[df_en["Electricity from nuclear (TWh)"] == 0].index, axis=0)
df_en_filtered = df_en_filtered.loc[(df_en_filtered["Year"]>=1999)& (df_en_filtered["Year"]<=2016),:]
df_en_filtered["Year"] = pd.to_datetime(df_en_filtered["Year"], format="%Y")

##Final Dataframe

df_final = df_en_filtered.merge(df_deaths,on="Year",how="inner")
df_final=df_final.groupby(["Entity","Year"]).agg({"Electricity from nuclear (TWh)":"sum",\
                        "Deaths":"sum"})
df_corr = df_final.groupby("Entity")[["Deaths", "Electricity from nuclear (TWh)"]].corr().iloc[0::2, -1]
df_corr.sort_values(ascending=False).head()

#######Final Solution

df_en_usa = df_en_filtered[df_en_filtered["Entity"]=="United States"]
df_en_usa = df_en_usa[["Code","Electricity from nuclear (TWh)","Year"]]
df_weird = df_deaths.merge(df_en_usa,on="Year",how="left")
df_weird.corr()
sns.regplot(x="Electricity from nuclear (TWh)", y="Deaths", data=df_weird)
plt.xlabel("Electricity from nuclear (TWh)")
plt.ylabel("Deaths")
plt.title("Scatter Plot: Correlation between Electricity and Deaths")
plt.show()


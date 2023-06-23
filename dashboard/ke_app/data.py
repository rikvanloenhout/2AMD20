import pandas as pd

def get_crime_data():
    # Import df_crime
    df_crime = pd.read_csv("../datasets/world_crime_index.csv")

    # Split the City column to a City and a Country column
    df_crime[['City', 'Country']] = df_crime['City'].str.split(',', expand=True).drop(2, axis=1)
    df_crime["Country"] = df_crime.Country.str.lstrip()

    # Get the min, max and avg crime index by country
    grouped_df_crime = df_crime.groupby('Country', as_index=False)['Crime Index'].agg(["mean", "min", "max"])
    grouped_df_crime.rename(columns={"mean": 'Mean Crime Index', "min": 'Min Crime Index', "max": 'Max Crime Index'},
                            inplace=True)
    grouped_df_crime['Rank'] = grouped_df_crime['Mean Crime Index'].rank()
    grouped_df_crime = get_country_codes(grouped_df_crime, "Country")

    return grouped_df_crime.sort_values(by="Rank").reset_index()


def get_life_data():
    df_life = pd.read_csv("../datasets/life_expectancy_data.csv")

    df_life = get_country_codes(df_life, "Country")
    df_life = df_life[df_life["Life expectancy "].notna()]

    return df_life.sort_values(by='Year')


def get_happiness_data():
    # Import happiness
    df_happ_2015 = pd.read_csv("../datasets/world_hapiness/2015.csv")
    df_happ_2016 = pd.read_csv("../datasets/world_hapiness/2016.csv")
    df_happ_2017 = pd.read_csv("../datasets/world_hapiness/2017.csv")
    df_happ_2018 = pd.read_csv("../datasets/world_hapiness/2018.csv")
    df_happ_2019 = pd.read_csv("../datasets/world_hapiness/2019.csv")

    # Add year column
    df_happ_2015["Year"] = 2015
    df_happ_2016["Year"] = 2016
    df_happ_2017["Year"] = 2017
    df_happ_2018["Year"] = 2018
    df_happ_2019["Year"] = 2019

    # Rename the dataframes
    df_happ_2017.rename(columns={
        "Happiness.Rank": "Happiness Rank",
        "Happiness.Score": "Happiness Score",
        "Whisker.high": "Upper Confidence Interval",
        "Whisker.low": "Lower Confidence Interval",
        "Economy..GDP.per.Capita.": "Economy (GDP per Capita)",
        "Health..Life.Expectancy.": "Health (Life Expectancy)",
        "Trust..Government.Corruption.": "Trust (Government Corruption)",
        "Dystopia.Residual": "Dystopia Residual"
    }, inplace=True)

    df_happ_2018.rename(columns={
        "Overall rank": "Happiness Rank",
        "Country or region": "Country",
        "Score": "Happiness Score",
        "GDP per capita": "Economy (GDP per Capita)",
        "Healthy life expectancy": "Health (Life Expectancy)",
        "Freedom to make life choices": "Freedom",
        "Perceptions of corruption": "Trust (Government Corruption)"
    }, inplace=True)

    df_happ_2019.rename(columns={
        "Overall rank": "Happiness Rank",
        "Country or region": "Country",
        "Score": "Happiness Score",
        "GDP per capita": "Economy (GDP per Capita)",
        "Healthy life expectancy": "Health (Life Expectancy)",
        "Freedom to make life choices": "Freedom",
        "Perceptions of corruption": "Trust (Government Corruption)"
    }, inplace=True)

    # Vertically concatenate the dataframes
    df_happ = pd.concat([df_happ_2015, df_happ_2016, df_happ_2017, df_happ_2018, df_happ_2019], ignore_index=True)

    df_happ = get_country_codes(df_happ, "Country")

    return df_happ


def get_poverty_data():
    # Import poverty statistics
    df_povstats = pd.read_csv("../datasets/povstats/PovStatsCountry.csv")
    df_povstats.rename(columns={"Short Name": "Country"}, inplace=True)

    df_povstats = pd.read_csv("../datasets/povstats/PovStatsData.csv")
    df_povstats = df_povstats[df_povstats["Indicator Code"] == "SI.POV.GINI"]
    df_povstats = df_povstats[["Country Code", "Country Name", "2015"]]
    df_povstats = df_povstats[df_povstats["2015"].notna()]
    df_povstats.rename(columns={"2015": "Gini"}, inplace=True)

    df_povstats = get_country_codes(df_povstats, "Country Name")

    return df_povstats


def get_country_codes(df, column_country_name):
    # Import country codes
    df_country_codes = pd.DataFrame({'ISO': list(country_codes_dict.values()), 'Country': list(country_codes_dict.keys())})

    # Merge the country codes with the dataframe
    df = pd.merge(df, df_country_codes, left_on=column_country_name, right_on="Country", how="left")

    return df


country_codes_dict = {
    'Afghanistan': 'AFG',
    'Albania': 'ALB',
    'Algeria': 'DZA',
    'Andorra': 'AND',
    'Angola': 'AGO',
    'Antigua and Barbuda': 'ATG',
    'Argentina': 'ARG',
    'Armenia': 'ARM',
    'Australia': 'AUS',
    'Austria': 'AUT',
    'Azerbaijan': 'AZE',
    'Bahamas': 'BHS',
    'Bahrain': 'BHR',
    'Bangladesh': 'BGD',
    'Barbados': 'BRB',
    'Belarus': 'BLR',
    'Belgium': 'BEL',
    'Belize': 'BLZ',
    'Benin': 'BEN',
    'Bhutan': 'BTN',
    'Bolivia': 'BOL',
    'Bosnia and Herzegovina': 'BIH',
    'Botswana': 'BWA',
    'Brazil': 'BRA',
    'Brunei': 'BRN',
    'Bulgaria': 'BGR',
    'Burkina Faso': 'BFA',
    'Burundi': 'BDI',
    'Cabo Verde': 'CPV',
    'Cambodia': 'KHM',
    'Cameroon': 'CMR',
    'Canada': 'CAN',
    'Central African Republic': 'CAF',
    'Chad': 'TCD',
    'Chile': 'CHL',
    'China': 'CHN',
    'Colombia': 'COL',
    'Comoros': 'COM',
    'Congo': 'COG',
    'Costa Rica': 'CRI',
    'Croatia': 'HRV',
    'Cuba': 'CUB',
    'Cyprus': 'CYP',
    'Czech Republic': 'CZE',
    'Democratic Republic of the Congo': 'COD',
    'Denmark': 'DNK',
    'Djibouti': 'DJI',
    'Dominica': 'DMA',
    'Dominican Republic': 'DOM',
    'Ecuador': 'ECU',
    'Egypt': 'EGY',
    'El Salvador': 'SLV',
    'Equatorial Guinea': 'GNQ',
    'Eritrea': 'ERI',
    'Estonia': 'EST',
    'Eswatini': 'SWZ',
    'Ethiopia': 'ETH',
    'Fiji': 'FJI',
    'Finland': 'FIN',
    'France': 'FRA',
    'Gabon': 'GAB',
    'Gambia': 'GMB',
    'Georgia': 'GEO',
    'Germany': 'DEU',
    'Ghana': 'GHA',
    'Greece': 'GRC',
    'Grenada': 'GRD',
    'Guatemala': 'GTM',
    'Guinea': 'GIN',
    'Guinea-Bissau': 'GNB',
    'Guyana': 'GUY',
    'Haiti': 'HTI',
    'Honduras': 'HND',
    'Hungary': 'HUN',
    'Iceland': 'ISL',
    'India': 'IND',
    'Indonesia': 'IDN',
    'Iran': 'IRN',
    'Iraq': 'IRQ',
    'Ireland': 'IRL',
    'Israel': 'ISR',
    'Italy': 'ITA',
    'Jamaica': 'JAM',
    'Japan': 'JPN',
    'Jordan': 'JOR',
    'Kazakhstan': 'KAZ',
    'Kenya': 'KEN',
    'Kiribati': 'KIR',
    'Kuwait': 'KWT',
    'Kyrgyzstan': 'KGZ',
    'Laos': 'LAO',
    'Latvia': 'LVA',
    'Lebanon': 'LBN',
    'Lesotho': 'LSO',
    'Liberia': 'LBR',
    'Libya': 'LBY',
    'Liechtenstein': 'LIE',
    'Lithuania': 'LTU',
    'Luxembourg': 'LUX',
    'Madagascar': 'MDG',
    'Malawi': 'MWI',
    'Malaysia': 'MYS',
    'Maldives': 'MDV',
    'Mali': 'MLI',
    'Malta': 'MLT',
    'Marshall Islands': 'MHL',
    'Mauritania': 'MRT',
    'Mauritius': 'MUS',
    'Mexico': 'MEX',
    'Micronesia': 'FSM',
    'Moldova': 'MDA',
    'Monaco': 'MCO',
    'Mongolia': 'MNG',
    'Montenegro': 'MNE',
    'Morocco': 'MAR',
    'Mozambique': 'MOZ',
    'Myanmar': 'MMR',
    'Namibia': 'NAM',
    'Nauru': 'NRU',
    'Nepal': 'NPL',
    'Netherlands': 'NLD',
    'New Zealand': 'NZL',
    'Nicaragua': 'NIC',
    'Niger': 'NER',
    'Nigeria': 'NGA',
    'North Korea': 'PRK',
    'North Macedonia': 'MKD',
    'Norway': 'NOR',
    'Oman': 'OMN',
    'Pakistan': 'PAK',
    'Palau': 'PLW',
    'Palestine': 'PSE',
    'Panama': 'PAN',
    'Papua New Guinea': 'PNG',
    'Paraguay': 'PRY',
    'Peru': 'PER',
    'Philippines': 'PHL',
    'Poland': 'POL',
    'Portugal': 'PRT',
    'Qatar': 'QAT',
    'Romania': 'ROU',
    'Russia': 'RUS',
    'Rwanda': 'RWA',
    'Saint Kitts and Nevis': 'KNA',
    'Saint Lucia': 'LCA',
    'Saint Vincent and the Grenadines': 'VCT',
    'Samoa': 'WSM',
    'San Marino': 'SMR',
    'Sao Tome and Principe': 'STP',
    'Saudi Arabia': 'SAU',
    'Senegal': 'SEN',
    'Serbia': 'SRB',
    'Seychelles': 'SYC',
    'Sierra Leone': 'SLE',
    'Singapore': 'SGP',
    'Slovakia': 'SVK',
    'Slovenia': 'SVN',
    'Solomon Islands': 'SLB',
    'Somalia': 'SOM',
    'South Africa': 'ZAF',
    'South Korea': 'KOR',
    'South Sudan': 'SSD',
    'Spain': 'ESP',
    'Sri Lanka': 'LKA',
    'Sudan': 'SDN',
    'Suriname': 'SUR',
    'Sweden': 'SWE',
    'Switzerland': 'CHE',
    'Syria': 'SYR',
    'Tajikistan': 'TJK',
    'Tanzania': 'TZA',
    'Thailand': 'THA',
    'Timor-Leste': 'TLS',
    'Togo': 'TGO',
    'Tonga': 'TON',
    'Trinidad and Tobago': 'TTO',
    'Tunisia': 'TUN',
    'Turkey': 'TUR',
    'Turkmenistan': 'TKM',
    'Tuvalu': 'TUV',
    'Uganda': 'UGA',
    'Ukraine': 'UKR',
    'United Arab Emirates': 'ARE',
    'United Kingdom': 'GBR',
    'United States': 'USA',
    'Uruguay': 'URY',
    'Uzbekistan': 'UZB',
    'Vanuatu': 'VUT',
    'Vatican City': 'VAT',
    'Venezuela': 'VEN',
    'Vietnam': 'VNM',
    'Yemen': 'YEM',
    'Zambia': 'ZMB',
    'Zimbabwe': 'ZWE'
}


def get_merged(df, x1, x2, x3, x4):
    # Compute sum
    summ = x1 + x2 + x3 + x4
    # Load data
    df = df[['ISO', 'Mean Crime Index', 'Life expectancy', 'Happiness Score', 'MeanGini']]

    inv_iso_dict = {v: k for k, v in country_codes_dict.items()}

    # Drop missing values
    df = df.dropna()

    # Normalize
    features = ['Mean Crime Index', 'Life expectancy', 'Happiness Score', 'MeanGini']
    for feat in features:
        df[feat] = (df[feat] - df[feat].min()) / (df[feat].max() - df[feat].min())

    # Features
    #     df.reset_index(inplace=True)
    df['Country'] = df['ISO'].apply(lambda x: inv_iso_dict[x])

    df['Aggregate Scores'] = (x1 / summ) * (1 - df['Mean Crime Index']) + (x2 / summ) * df['Life expectancy'] \
                             + (x3 / summ) * df['Happiness Score'] + (x4 / summ) * (1 - df['MeanGini'])

    df = df.sort_values(by='Aggregate Scores')
    df['Rank'] = df['Aggregate Scores'].rank(ascending=False)
    return df.sort_values(by="Rank")
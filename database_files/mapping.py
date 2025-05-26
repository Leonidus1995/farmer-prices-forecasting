

# Step 1: Create a mapping dictionary
file_table_column_map = {
    "producer_prices_cleaned.csv": {
        "table": "producer_prices",
        "column_mapping": {
            'area_code': 'area_code',	
            'area': 'area',	
            'item_code': 'item_code',	
            'item': 'item',	
            'year': 'year',	
            'year_code': 'year_code',	
            'producer_price_USD_per_tonne': 'producer_price',	
            'producer_price_index': 'producer_price_index'
        }
    },

    "gross_production_value_cleaned.csv": {
        "table": "production_value",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'item_code': 'item_code',
            'item': 'item',
            'gross_production_value': 'gross_production_value'
        }
    },

    "production_indices_cleaned.csv": {
        "table": "production_index",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'item_code': 'item_code',
            'item': 'item',
            'gross_production_index': 'gross_production_index'
        }
    },

    "trade_cleaned.csv": {
        "table": "trade",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'item_code': 'item_code',
            'item': 'item',
            'export_quantity': 'export_quantity',
            'export_value': 'export_value',
            'import_quantity': 'import_quantity',
            'import_value': 'import_value'
        }
    }, 

    "trade_indices_cleaned.csv": {
        "table": "trade_indices",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'item_code': 'item_code',
            'item': 'item',
            'export_quantity_index': 'export_quantity_index',
            'export_value_index': 'export_value_index',
            'import_quantity_index': 'import_quantity_index',
            'import_value_index': 'import_value_index'
        }
    },

    "trade_indicators_cleaned.csv": {
        "table": "trade_indicators",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'item_code': 'item_code',
            'item': 'item',
            'export_market_concentration_index': 'export_market_concentration_index',
            'import_dependency_ratio': 'import_dependency_ratio',
            'import_market_concentration_index':'import_market_concentration_index' ,
            'revealed_comparative_advantage_index':'revealed_comparative_advantage_index' ,
            'self_sufficiency_ratio': 'self_sufficiency_ratio',
            'terms_of_trade': 'terms_of_trade' 
        }
    },

    "trade_indicators_agri_cleaned.csv": {
        "table": "agri_trade_indicators",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'agri_trade_openness_index': 'agri_trade_openness_index',
            'share_of_agri_exports_to_GDP': 'share_of_agri_exports_to_gdp'
        }
    },

    "crop_production_cleaned.csv": {
        "table": "crop_production",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'item_code': 'item_code',
            'item': 'item',
            'area_harvested': 'area_harvested',
            'laying': 'laying',
            'milk_animals': 'milk_animals',
            'producing_animals_or_slaughtered': 'producing_animals_or_slaughtered',
            'production': 'production',
            'yield': 'yield',
            'yield_or_carcass_weight': 'yield_or_carcass_weight'
        }
    },

    "cropland_nutrient_balance_cleaned.csv": {
        "table": "cropland_nutrient_balance",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'NB_N2_per_unit_cropland_area': 'cropland_nitrogen_per_unit_area',
            'cropland_N2_use_efficiency': 'cropland_nitrogen_use_efficiency',
            'NB_P2O5_per_unit_cropland_area': 'cropland_phosphorus_per_unit_area',
            'cropland_P2O5_use_efficiency': 'cropland_phosphorus_use_efficiency',
            'NB_K2O_per_unit_cropland_area': 'cropland_potassium_per_unit_area',
            'cropland_K2O_use_efficiency': 'cropland_potassium_use_efficiency'
        }
    }, 

    "credit_to_agri_forestry_fishery_cleaned.csv": {
        "table": "credit_to_agri",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'Agri_orientation_index_2015_USD': 'agri_orientation_index_2015_usd',
            'credit_to_ag_forest_fish_share_totalCredit': 'credit_to_ag_forest_fish_share_totalcredit',
            'credit_to_ag_forest_fish_2015_USD': 'credit_to_ag_forest_fish_2015_usd'
        }
    },

    "annual_population_cleaned.csv": {
        "table": "annual_population",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'rural_population': 'rural_population',
            'total_population': 'total_population',
            'urban_population': 'urban_population'
        }
    },

    "economic_indicators_cleaned.csv": {
        "table": "economic_indicators",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'gross_domestic_product': 'gross_domestic_product',
            'gross_fixed_capital_formation': 'gross_fixed_capital_formation',
            'value_added_ag_forest_fish': 'value_added_ag_forest_fish',
            'GDP_annual_growth': 'gdp_annual_growth',
            'GFCF_annual_growth': 'gfcf_annual_growth',
            'value_added_ag_forest_fish_annual_growth': 'value_added_ag_forest_fish_annual_growth',
            'GFCF_share_in_total_GDP': 'gfcf_share_in_total_gdp',
            'ag_forest_fish_share_in_total_GDP': 'ag_forest_fish_share_in_total_gdp'
        }
    },

    "emission_indicators_cleaned.csv": {
        "table": "emission_indicators",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'emission_share_end_to_end_agrifood': 'emission_share_end_to_end_agrifood',
            'emission_share_crops': 'emission_share_crops',
            'emission_share_livestock': 'emission_share_livestock',
            'emission_share_energy_use': 'emission_share_energy_use',
            'emission_share_farmgate': 'emission_share_farmgate',
            'emission_share_IPCC_agriculture': 'emission_share_ipcc_agriculture',
            'emission_share_land_use_change': 'emission_share_land_use_change',
            'emission_share_pre_and_post_production': 'emission_share_pre_and_post_production',
            'emission_share_agri_waste_mgt': 'emission_share_agri_waste_mgt'
        }
    },

    "employment_indicators_cleaned.csv": {
        "table": "employment_indicators",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'value_added_per_worker': 'value_added_per_worker',
            'employment_in_agri': 'employment_in_agri',
            'AFS_employment_share_in_total_employment': 'afs_employment_share_in_total_employment',
            'agri_employment_share_in_total_employment': 'agri_employment_share_in_total_employment',
            'total_employment_AFS': 'total_employment_afs'
        }
    },

    "N2_fertilizers_cleaned.csv": {
        "table": "nitrogen_fertilizer",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'N2_for_Ag_use': 'nitrogen_agri_use',
            'N2_export_quantity': 'nitrogen_export_quantity',
            'N2_import_quantity': 'nitrogen_import_quantity',
            'N2_production': 'nitrogen_production',
            'N2_use_per_area_of_cropland': 'nitrogen_use_per_area_of_cropland',
            'N2_use_per_capita': 'nitrogen_use_per_capita',
            'N2_use_per_value_of_Ag_production': 'nitrogen_use_per_value_of_ag_production'
        }
    }, 

    "P2O5_fertilizers_cleaned.csv": {
        "table": "phosphorus_fertilizer",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'P2O5_for_Ag_use': 'phosphorus_agri_use',
            'P2O5_export_quantity': 'phosphorus_export_quantity',
            'P2O5_import_quantity': 'phosphorus_import_quantity',
            'P2O5_production': 'phosphorus_production',
            'P2O5_use_per_area_of_cropland': 'phosphorus_use_per_area_of_cropland',
            'P2O5_use_per_capita': 'phosphorus_use_per_capita',
            'P2O5_use_per_value_of_Ag_production': 'phosphorus_use_per_value_of_ag_production'
        }
    },

    "K2O_fertilizers_cleaned.csv": {
        "table": "potassium_fertilizer",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'K2O_for_Ag_use': 'potassium_agri_use',
            'K2O_export_quantity': 'potassium_export_quantity',
            'K2O_import_quantity': 'potassium_import_quantity',
            'K2O_use_per_area_of_cropland': 'potassium_use_per_area_of_cropland',
            'K2O_use_per_capita': 'potassium_use_per_capita',
            'K2O_use_per_value_of_Ag_production': 'potassium_use_per_value_of_ag_production'
        }
    },

    "foreign_investment_cleaned.csv": {
        "table": "foreign_investment",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'FDI_ag_forest_fish': 'fdi_ag_forest_fish',
            'FDI_food_industry': 'fdi_food_industry',
            'total_FDI_inflows': 'total_fdi_inflows',
            'FDI_ag_forest_fish_share': 'fdi_ag_forest_fish_share',
            'FDI_food_industry_share': 'fdi_food_industry_share'
        }
    },

    "government_investment_cleaned.csv": {
        "table": "government_investment",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'AOI_for_govt_expenditure': 'agri_orientation_index_govt_expenditure',
            'Govt_expenditure_on_Ag': 'govt_expenditure_on_ag',
            'Govt_expenditure_on_Ag_forest_fish': 'govt_expenditure_on_ag_forest_fish',
            'Ag_forest_fish_as_share_of_total_expenditure': 'ag_forest_fish_as_share_of_total_expenditure'
        }
    },

    "landuse_cleaned.csv": {
        "table": "landuse",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'area_agri_land': 'area_agri_land',
            'area_arable_land': 'area_arable_land',
            'area_cropland': 'area_cropland',
            'area_with_irrigation': 'area_with_irrigation',
            'area_permanent_crops': 'area_permanent_crops',
            'area_temporary_crops': 'area_temporary_crops',
            'value_per_unit_agri_land': 'value_per_unit_agri_land',
            'cropland_area_per_capita': 'cropland_area_per_capita'
        }
    },

    "pesticides_trade_cleaned.csv": {
        "table": "pesticide_trade",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'total_pesticide_export_quantity': 'total_pesticide_export_quantity',
            'total_pesticide_export_value': 'total_pesticide_export_value',
            'total_pesticide_import_quantity': 'total_pesticide_import_quantity',
            'total_pesticide_import_value': 'total_pesticide_import_value'
        }
    },

    "pesticides_cleaned.csv": {
        "table": "pesticide",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'total_pesticide_use_for_agriculture': 'total_pesticide_use_for_agriculture',
            'total_pesticide_use_per_area_of_cropland': 'total_pesticide_use_per_area_of_cropland',
            'total_pesticide_use_per_capita': 'total_pesticide_use_per_capita',
            'total_pesticide_use_per_value_of_agri_production': 'total_pesticide_use_per_value_of_agri_production'
        }
    },

    "temp_change_cleaned.csv": {
        "table": "temperature_change",
        "column_mapping": {
            'area_code': 'area_code' ,
            'area': 'area',
            'year_code': 'year_code',
            'year': 'year',
            'temp_change_Dec_Jan_Feb': 'temp_change_dec_jan_feb',
            'temp_change_Jun_Jul_Aug': 'temp_change_jun_jul_aug',
            'temp_change_Mar_Apr_May': 'temp_change_mar_apr_may',
            'temp_change_meteorological_year': 'temp_change_meteorological_year',
            'temp_change_Sep_Oct_Nov': 'temp_change_sep_oct_nov'
        }
    }
}







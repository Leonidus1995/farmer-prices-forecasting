-- Create a table for producer price data and set ownership to postgres
CREATE TABLE producer_prices (
    area_code            SMALLINT     NOT NULL,
    area                 VARCHAR(255) NOT NULL,
    year_code            SMALLINT     NOT NULL,
    year                 SMALLINT     NOT NULL,
    item_code            SMALLINT     NOT NULL,
    item                 VARCHAR(255) NOT NULL,
    producer_price       NUMERIC(20,8),
    producer_price_index NUMERIC(20,8),
    CONSTRAINT pk_producer_prices
        PRIMARY KEY (area_code, year_code, item_code)
);

ALTER TABLE producer_prices OWNER to postgres;



-- Create a table for crop production value data and set ownership to postgres
CREATE TABLE production_value (
    area_code              SMALLINT     NOT NULL,
    area                   VARCHAR(255) NOT NULL,
    year_code              SMALLINT     NOT NULL,
    year                   SMALLINT     NOT NULL,
    item_code              SMALLINT     NOT NULL,
    item                   VARCHAR(255) NOT NULL,
    gross_production_value NUMERIC(20,8),
    CONSTRAINT pk_production_value
        PRIMARY KEY (area_code, year_code, item_code)
);

ALTER TABLE production_value OWNER to postgres;



-- Create a table for crop production index data and set ownership to postgres
CREATE TABLE production_index (
    area_code              SMALLINT     NOT NULL,
    area                   VARCHAR(255) NOT NULL,
    year_code              SMALLINT     NOT NULL,
    year                   SMALLINT     NOT NULL,
    item_code              SMALLINT     NOT NULL,
    item                   VARCHAR(255) NOT NULL,
    gross_production_index NUMERIC(20,8),
    CONSTRAINT pk_production_index
        PRIMARY KEY (area_code, year_code, item_code)
);

ALTER TABLE production_index OWNER to postgres;



-- Create a table for trade data and set ownership to postgres
CREATE TABLE trade (
    area_code         INTEGER     NOT NULL,
    area              VARCHAR(255) NOT NULL,
    year_code         INTEGER     NOT NULL,
    year              INTEGER     NOT NULL,
    item_code         INTEGER     NOT NULL,
    item              VARCHAR(255) NOT NULL,
    export_quantity   NUMERIC(20,8),
    export_value      NUMERIC(20,8),
    import_quantity   NUMERIC(20,8),
    import_value      NUMERIC(20,8),
    CONSTRAINT pk_trade
        PRIMARY KEY (area_code, year_code, item_code)
);

ALTER TABLE trade OWNER to postgres;



-- Create a table for trade indices data and set ownership to postgres
CREATE TABLE trade_indices (
    area_code               INTEGER     NOT NULL,
    area                    VARCHAR(255) NOT NULL,
    year_code               INTEGER     NOT NULL,
    year                    INTEGER     NOT NULL,
    item_code               INTEGER     NOT NULL,
    item                    VARCHAR(255) NOT NULL,
    export_quantity_index   NUMERIC(20,8),
    export_value_index      NUMERIC(20,8),
    import_quantity_index   NUMERIC(20,8),
    import_value_index      NUMERIC(20,8),
    CONSTRAINT pk_trade_indices
        PRIMARY KEY (area_code, year_code, item_code)
);

ALTER TABLE trade_indices OWNER to postgres;



-- Create a table for trade indicators data and set ownership to postgres
CREATE TABLE trade_indicators (
    area_code                             INTEGER     NOT NULL,
    area                                  VARCHAR(255) NOT NULL,
    year_code                             INTEGER     NOT NULL,
    year                                  INTEGER     NOT NULL,
    item_code                             INTEGER     NOT NULL,
    item                                  VARCHAR(255) NOT NULL,
    export_market_concentration_index     NUMERIC(20,8),
    import_dependency_ratio               NUMERIC(20,8),
    import_market_concentration_index     NUMERIC(20,8),
    revealed_comparative_advantage_index  NUMERIC(20,8),
    self_sufficiency_ratio                NUMERIC(20,8),
    terms_of_trade                        NUMERIC(20,8),
    CONSTRAINT pk_trade_indicators
        PRIMARY KEY (area_code, year_code, item_code)
);

ALTER TABLE trade_indicators OWNER to postgres;



-- Create a table for agri trade indicators data and set ownership to postgres
CREATE TABLE agri_trade_indicators (
    area_code                             SMALLINT     NOT NULL,
    area                                  VARCHAR(255) NOT NULL,
    year_code                             SMALLINT     NOT NULL,
    year                                  SMALLINT     NOT NULL,
    agri_trade_openness_index             NUMERIC(20,8),
    share_of_agri_exports_to_gdp          NUMERIC(20,8),
    CONSTRAINT pk_agri_trade_indicators
        PRIMARY KEY (area_code, year_code)
);

ALTER TABLE agri_trade_indicators OWNER to postgres;



-- Create a table for crop production data and set ownership to postgres
CREATE TABLE crop_production (
    area_code                         SMALLINT     NOT NULL,
    area                              VARCHAR(255) NOT NULL,
    year_code                         SMALLINT     NOT NULL,
    year                              SMALLINT     NOT NULL,
    item_code                         SMALLINT     NOT NULL,
    item                              VARCHAR(255) NOT NULL,
    area_harvested                    NUMERIC(20,8),
    laying                            NUMERIC(20,8),
    milk_animals                      NUMERIC(20,8),
    producing_animals_or_slaughtered  NUMERIC(20,8),
    production                        NUMERIC(20,8),
    yield                             NUMERIC(20,8),
    yield_or_carcass_weight           NUMERIC(20,8),
    CONSTRAINT pk_crop_production
        PRIMARY KEY (area_code, year_code, item_code)
);

ALTER TABLE crop_production OWNER to postgres;



-- Create a table for cropland nutrient balance data and set ownership to postgres
CREATE TABLE cropland_nutrient_balance (
    area_code                             SMALLINT     NOT NULL,
    area                                  VARCHAR(255) NOT NULL,
    year_code                             SMALLINT     NOT NULL,
    year                                  SMALLINT     NOT NULL,
    cropland_nitrogen_per_unit_area       NUMERIC(20,8),
    cropland_nitrogen_use_efficiency      NUMERIC(20,8),
    cropland_phosphorus_per_unit_area     NUMERIC(20,8),
    cropland_phosphorus_use_efficiency    NUMERIC(20,8),
    cropland_potassium_per_unit_area      NUMERIC(20,8),
    cropland_potassium_use_efficiency     NUMERIC(20,8),
    CONSTRAINT pk_cropland_nutrient_balance
        PRIMARY KEY (area_code, year_code)
);

ALTER TABLE cropland_nutrient_balance OWNER to postgres;



-- Create a table for credit to agriculture data and set ownership to postgres
CREATE TABLE credit_to_agri (
    area_code                                    SMALLINT     NOT NULL,
    area                                         VARCHAR(255) NOT NULL,
    year_code                                    SMALLINT     NOT NULL,
    year                                         SMALLINT     NOT NULL,
    credit_to_ag_forest_fish_2015_usd            NUMERIC(20,8),
    credit_to_ag_forest_fish_share_totalCredit   NUMERIC(20,8),
    agri_orientation_index_2015_usd              NUMERIC(20,8),
    CONSTRAINT pk_credit_to_agri
        PRIMARY KEY (area_code, year_code)
);

ALTER TABLE credit_to_agri OWNER to postgres;



-- Create a table for annual population data and set ownership to postgres
CREATE TABLE annual_population (
    area_code          SMALLINT     NOT NULL,
    area               VARCHAR(255) NOT NULL,
    year_code          SMALLINT     NOT NULL,
    year               SMALLINT     NOT NULL,
    rural_population   NUMERIC(20,8),
    urban_population   NUMERIC(20,8),
    total_population   NUMERIC(20,8),
    CONSTRAINT pk_annual_population
        PRIMARY KEY (area_code, year_code)
);

ALTER TABLE annual_population OWNER to postgres;



-- Create a table for economic indicators data and set ownership to postgres
CREATE TABLE economic_indicators (
    area_code                                 SMALLINT     NOT NULL,
    area                                      VARCHAR(255) NOT NULL,
    year_code                                 SMALLINT     NOT NULL,
    year                                      SMALLINT     NOT NULL,
    gross_domestic_product                    NUMERIC(20,8),
    gross_fixed_capital_formation             NUMERIC(20,8),
    value_added_ag_forest_fish                NUMERIC(20,8),
    gdp_annual_growth                         NUMERIC(20,8),
    gfcf_annual_growth                        NUMERIC(20,8),
    value_added_ag_forest_fish_annual_growth  NUMERIC(20,8),
    gfcf_share_in_total_gdp                   NUMERIC(20,8),
    ag_forest_fish_share_in_total_gdp         NUMERIC(20,8),
    CONSTRAINT pk_economic_indicators
        PRIMARY KEY (area_code, year_code)
);

ALTER TABLE economic_indicators OWNER to postgres;



-- Create a table for emission indicators data and set ownership to postgres
CREATE TABLE emission_indicators (
    area_code                                 SMALLINT     NOT NULL,
    area                                      VARCHAR(255) NOT NULL,
    year_code                                 SMALLINT     NOT NULL,
    year                                      SMALLINT     NOT NULL,
    emission_share_farmgate                   NUMERIC(20,8),
    emission_share_land_use_change            NUMERIC(20,8),
    emission_share_pre_and_post_production    NUMERIC(20,8),
    emission_share_end_to_end_agrifood        NUMERIC(20,8),
    emission_share_crops                      NUMERIC(20,8),
    emission_share_livestock                  NUMERIC(20,8),
    emission_share_ipcc_agriculture           NUMERIC(20,8),
    emission_share_energy_use                 NUMERIC(20,8),
    emission_share_agri_waste_mgt             NUMERIC(20,8),
    CONSTRAINT pk_emission_indicators
        PRIMARY KEY (area_code, year_code)
);

ALTER TABLE emission_indicators OWNER to postgres;



-- Create a table for employment indicators data and set ownership to postgres
CREATE TABLE employment_indicators (
    area_code                                   SMALLINT     NOT NULL,
    area                                        VARCHAR(255) NOT NULL,
    year_code                                   SMALLINT     NOT NULL,
    year                                        SMALLINT     NOT NULL,
    value_added_per_worker                      NUMERIC(20,8),
    employment_in_agri                          NUMERIC(20,8),
    agri_employment_share_in_total_employment   NUMERIC(20,8),
    total_employment_afs                        NUMERIC(20,8),
    afs_employment_share_in_total_employment    NUMERIC(20,8),
    CONSTRAINT pk_employment_indicators
        PRIMARY KEY (area_code, year_code)
);

ALTER TABLE employment_indicators OWNER to postgres;



-- Create a table for nitrogen fertilizer data and set ownership to postgres
CREATE TABLE nitrogen_fertilizer (
    area_code                                SMALLINT     NOT NULL,
    area                                     VARCHAR(255) NOT NULL,
    year_code                                SMALLINT     NOT NULL,
    year                                     SMALLINT     NOT NULL,
    nitrogen_agri_use                        NUMERIC(20,8),
    nitrogen_export_quantity                 NUMERIC(20,8),
    nitrogen_import_quantity                 NUMERIC(20,8),
    nitrogen_production                      NUMERIC(20,8),
    nitrogen_use_per_area_of_cropland        NUMERIC(20,8),
    nitrogen_use_per_capita                  NUMERIC(20,8),
    nitrogen_use_per_value_of_ag_production  NUMERIC(20,8),
    CONSTRAINT pk_nitrogen_fertilizer
        PRIMARY KEY (area_code, year_code)
);

ALTER TABLE nitrogen_fertilizer OWNER to postgres;



-- Create a table for phosphorus fertilizer data and set ownership to postgres
CREATE TABLE phosphorus_fertilizer (
    area_code                                SMALLINT     NOT NULL,
    area                                     VARCHAR(255) NOT NULL,
    year_code                                SMALLINT     NOT NULL,
    year                                     SMALLINT     NOT NULL,
    phosphorus_agri_use                        NUMERIC(20,8),
    phosphorus_export_quantity                 NUMERIC(20,8),
    phosphorus_import_quantity                 NUMERIC(20,8),
    phosphorus_production                      NUMERIC(20,8),
    phosphorus_use_per_area_of_cropland        NUMERIC(20,8),
    phosphorus_use_per_capita                  NUMERIC(20,8),
    phosphorus_use_per_value_of_ag_production  NUMERIC(20,8),
    CONSTRAINT pk_phosphorus_fertilizer
        PRIMARY KEY (area_code, year_code)
);

ALTER TABLE phosphorus_fertilizer OWNER to postgres;



-- Create a table for potassium fertilizer data and set ownership to postgres
CREATE TABLE potassium_fertilizer (
    area_code                                SMALLINT     NOT NULL,
    area                                     VARCHAR(255) NOT NULL,
    year_code                                SMALLINT     NOT NULL,
    year                                     SMALLINT     NOT NULL,
    potassium_agri_use                        NUMERIC(20,8),
    potassium_export_quantity                 NUMERIC(20,8),
    potassium_import_quantity                 NUMERIC(20,8),
    potassium_use_per_area_of_cropland        NUMERIC(20,8),
    potassium_use_per_capita                  NUMERIC(20,8),
    potassium_use_per_value_of_ag_production  NUMERIC(20,8),
    CONSTRAINT pk_potassium_fertilizer
        PRIMARY KEY (area_code, year_code)
);

ALTER TABLE potassium_fertilizer OWNER to postgres;



-- Create a table for foreign investment (FDI) data and set ownership to postgres
CREATE TABLE foreign_investment (
    area_code                    SMALLINT     NOT NULL,
    area                         VARCHAR(255) NOT NULL,
    year_code                    SMALLINT     NOT NULL,
    year                         SMALLINT     NOT NULL,
    fdi_ag_forest_fish           NUMERIC(20,8),
    fdi_food_industry            NUMERIC(20,8),
    total_fdi_inflows            NUMERIC(20,8),
    fdi_ag_forest_fish_share     NUMERIC(20,8),
    fdi_food_industry_share      NUMERIC(20,8),
    CONSTRAINT pk_foreign_investment
        PRIMARY KEY (area_code, year_code)
);

ALTER TABLE foreign_investment OWNER to postgres;



-- Create a table for government investment data and set ownership to postgres
CREATE TABLE government_investment (
    area_code                                     SMALLINT     NOT NULL,
    area                                          VARCHAR(255) NOT NULL,
    year_code                                     SMALLINT     NOT NULL,
    year                                          SMALLINT     NOT NULL,
    agri_orientation_index_govt_expenditure       NUMERIC(20,8),
    govt_expenditure_on_ag                        NUMERIC(20,8),
    govt_expenditure_on_ag_forest_fish            NUMERIC(20,8),
    ag_forest_fish_as_share_of_total_expenditure  NUMERIC(20,8),
    CONSTRAINT pk_government_investment
        PRIMARY KEY (area_code, year_code)
);

ALTER TABLE government_investment OWNER to postgres;



-- Create a table for landuse data and set ownership to postgres
CREATE TABLE landuse (
    area_code                  SMALLINT     NOT NULL,
    area                       VARCHAR(255) NOT NULL,
    year_code                  SMALLINT     NOT NULL,
    year                       SMALLINT     NOT NULL,
    area_agri_land             NUMERIC(20,8),
    area_arable_land           NUMERIC(20,8),
    area_cropland              NUMERIC(20,8),
    area_with_irrigation       NUMERIC(20,8),
    area_permanent_crops       NUMERIC(20,8),
    area_temporary_crops       NUMERIC(20,8),
    value_per_unit_agri_land   NUMERIC(20,8),
    cropland_area_per_capita   NUMERIC(20,8),
    CONSTRAINT pk_landuse
        PRIMARY KEY (area_code, year_code)
);

ALTER TABLE landuse OWNER to postgres;



-- Create a table for pesticide trade data and set ownership to postgres
CREATE TABLE pesticide_trade (
    area_code                        INTEGER     NOT NULL,
    area                             VARCHAR(255) NOT NULL,
    year_code                        INTEGER     NOT NULL,
    year                             INTEGER     NOT NULL,
    total_pesticide_export_quantity  NUMERIC(20,8),
    total_pesticide_export_value     NUMERIC(20,8),
    total_pesticide_import_quantity  NUMERIC(20,8),
    total_pesticide_import_value     NUMERIC(20,8),
    CONSTRAINT pk_pesticide_trade
        PRIMARY KEY (area_code, year_code)
);

ALTER TABLE pesticide_trade OWNER to postgres;



-- Create a table for pesticide data and set ownership to postgres
CREATE TABLE pesticide (
    area_code                                          SMALLINT     NOT NULL,
    area                                               VARCHAR(255) NOT NULL,
    year_code                                          SMALLINT     NOT NULL,
    year                                               SMALLINT     NOT NULL,
    total_pesticide_use_for_agriculture                NUMERIC(20,8),
    total_pesticide_use_per_area_of_cropland           NUMERIC(20,8),
    total_pesticide_use_per_capita                     NUMERIC(20,8),
    total_pesticide_use_per_value_of_agri_production   NUMERIC(20,8),
    CONSTRAINT pk_pesticide
        PRIMARY KEY (area_code, year_code)
);

ALTER TABLE pesticide OWNER to postgres;



-- Create a table for temperature change data and set ownership to postgres
CREATE TABLE temperature_change (
    area_code                         SMALLINT     NOT NULL,
    area                              VARCHAR(255) NOT NULL,
    year_code                         SMALLINT     NOT NULL,
    year                              SMALLINT     NOT NULL,
    temp_change_dec_jan_feb           NUMERIC(20,8),
    temp_change_mar_apr_may           NUMERIC(20,8),
    temp_change_jun_jul_aug           NUMERIC(20,8),
    temp_change_sep_oct_nov           NUMERIC(20,8),
    temp_change_meteorological_year   NUMERIC(20,8),
    CONSTRAINT pk_temperature_change
        PRIMARY KEY (area_code, year_code)
);

ALTER TABLE temperature_change OWNER to postgres;